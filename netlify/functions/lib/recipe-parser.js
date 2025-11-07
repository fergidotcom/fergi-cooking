/**
 * Recipe Parser Library
 * Reusable functions for parsing recipes with AI extraction
 * Used by both batch processing and Add Recipe feature
 */

const Anthropic = require('@anthropic-ai/sdk');

/**
 * Parse recipe text into structured format using Claude API
 * @param {string} text - Raw recipe text
 * @param {object} options - Optional metadata (contributor, filename, etc.)
 * @returns {Promise<object>} Parsed recipe data
 */
async function parseRecipe(text, options = {}) {
  const anthropic = new Anthropic({
    apiKey: process.env.ANTHROPIC_API_KEY
  });

  const { contributor, original_filename, source_type } = options;

  console.log(`Parsing recipe from ${source_type || 'text'}...`);
  console.log(`Text length: ${text.length} characters`);

  const prompt = `You are formatting a recipe for the Ferguson family cookbook. Convert the provided text into the Ferguson standard format.

⭐ CRITICAL REQUIREMENTS:

1. **Ingredients List** (for shopping):
   - Clean, structured list with quantities
   - Format: "2 cups all-purpose flour", "1 cup granulated sugar"
   - Use standard measurements and clear ingredient names

2. **Instructions** (for cooking) - MOST IMPORTANT:
   - Step-by-step instructions
   - **EMBED QUANTITIES IN EACH STEP** (e.g., "Mix 2 cups flour with 1 cup sugar")
   - The cook should NEVER need to refer back to the ingredients list
   - Each step should be completely self-contained with all quantities
   - Example GOOD: "In a large bowl, mix 2 cups all-purpose flour with 1 cup granulated sugar"
   - Example BAD: "Mix the flour with the sugar" (missing quantities!)

3. **Both sections include quantities** - This redundancy is intentional:
   - Ingredients = shopping reference
   - Instructions = cooking reference (with embedded quantities)

4. **Estimates for missing data**:
   - If prep time, cook time, or servings not provided, estimate based on recipe complexity
   - Estimate calories per serving based on ingredients

5. **Metadata**:
   - Add relevant tags for searchability (e.g., "quick", "easy", "vegetarian", "dessert")
   - Infer cuisine type: American, Italian, Mexican, Asian, French, Mediterranean, Indian, Caribbean, Other
   - Classify meal type: breakfast, lunch, dinner, dessert, snack, appetizer, side
   - Determine difficulty: easy, medium, hard

6. **Quality**:
   - Extract actual recipe title (never use filenames like "IMG_8111.JPG")
   - Write 1-3 sentence description that's appetizing and descriptive
   - Clean up OCR errors if present
   - Standardize ingredient names and measurements

INPUT TEXT:
${text}

OUTPUT (respond with ONLY valid JSON, no other text):
{
  "title": "Recipe Name",
  "description": "Brief 1-3 sentence description of the dish",
  "cuisine": "American",
  "meal_type": "dinner",
  "difficulty": "medium",
  "prep_time": 15,
  "cook_time": 30,
  "servings": "4-6",
  "calories_per_serving": 350,
  "ingredients": [
    "2 cups all-purpose flour",
    "1 cup granulated sugar",
    "1/2 cup butter, softened",
    "2 large eggs, beaten",
    "1 tsp vanilla extract"
  ],
  "instructions": [
    "Preheat oven to 350°F (175°C).",
    "In a large bowl, mix 2 cups all-purpose flour with 1 cup granulated sugar.",
    "Add 1/2 cup softened butter and beat until creamy.",
    "Mix in 2 beaten eggs and 1 tsp vanilla extract until well combined.",
    "Spread mixture in greased 9x13 pan and bake for 25-30 minutes until golden brown."
  ],
  "tags": ["quick", "easy", "dessert", "family-favorite"],
  "notes": "Optional cooking tips, serving suggestions, or variations",
  "confidence_score": 0.95,
  "needs_review": false,
  "review_notes": "Flag any uncertainties here"
}

If you're uncertain about any extracted information, set "confidence_score" lower (0.0-1.0) and "needs_review" to true with details in "review_notes".`;

  console.log('Sending request to Claude API...');

  const message = await anthropic.messages.create({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 4000,
    temperature: 0.3, // Lower temperature for more consistent extraction
    messages: [{
      role: 'user',
      content: prompt
    }]
  });

  console.log('Claude API response received');

  const responseText = message.content[0].text;

  // Parse JSON from response
  let recipe;
  try {
    // Try to parse the response directly
    recipe = JSON.parse(responseText);
  } catch (e) {
    // Try to extract JSON if Claude added extra text
    console.log('Direct JSON parse failed, attempting to extract...');
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      recipe = JSON.parse(jsonMatch[0]);
    } else {
      throw new Error('Could not parse recipe JSON from AI response');
    }
  }

  // Validate required fields
  validateRecipe(recipe);

  // Add metadata
  if (contributor) recipe.contributor = contributor;
  if (original_filename) recipe.original_source = original_filename;
  recipe.date_added = new Date().toISOString();
  recipe.import_method = source_type || 'batch_import';

  console.log(`Successfully parsed recipe: ${recipe.title}`);

  return recipe;
}

/**
 * Validate recipe has all required fields
 * @param {object} recipe - Recipe object to validate
 * @throws {Error} If validation fails
 */
function validateRecipe(recipe) {
  const required = ['title', 'ingredients', 'instructions'];
  const missing = required.filter(field => !recipe[field]);

  if (missing.length > 0) {
    throw new Error(`Recipe missing required fields: ${missing.join(', ')}`);
  }

  if (!Array.isArray(recipe.ingredients) || recipe.ingredients.length === 0) {
    throw new Error('Recipe must have at least one ingredient');
  }

  if (!Array.isArray(recipe.instructions) || recipe.instructions.length === 0) {
    throw new Error('Recipe must have at least one instruction step');
  }

  // Check if instructions have embedded quantities
  const hasQuantities = recipe.instructions.some(step =>
    /\d+\s*(cup|tbsp|tsp|oz|lb|g|kg|ml|l|piece|slice|clove|bunch)/i.test(step)
  );

  if (!hasQuantities) {
    console.warn(`⚠️  Recipe "${recipe.title}" instructions may be missing embedded quantities`);
    if (!recipe.needs_review) {
      recipe.needs_review = true;
      recipe.review_notes = (recipe.review_notes || '') + ' Instructions may be missing embedded quantities.';
    }
  }

  return true;
}

/**
 * Estimate missing recipe data
 * @param {object} recipe - Recipe object
 * @returns {object} Recipe with estimated fields
 */
function estimateMissingData(recipe) {
  // Estimate prep time if missing
  if (!recipe.prep_time || recipe.prep_time === 0) {
    const ingredientCount = recipe.ingredients?.length || 0;
    recipe.prep_time = Math.max(5, Math.min(60, ingredientCount * 2));
  }

  // Estimate cook time if missing
  if (!recipe.cook_time || recipe.cook_time === 0) {
    const instructionCount = recipe.instructions?.length || 0;
    recipe.cook_time = Math.max(10, Math.min(120, instructionCount * 5));
  }

  // Estimate servings if missing
  if (!recipe.servings) {
    recipe.servings = '4-6';
  }

  // Estimate calories if missing
  if (!recipe.calories_per_serving || recipe.calories_per_serving === 0) {
    recipe.calories_per_serving = 300; // Conservative default
  }

  return recipe;
}

/**
 * Clean and normalize recipe data
 * @param {object} recipe - Recipe object
 * @returns {object} Cleaned recipe
 */
function normalizeRecipe(recipe) {
  // Clean title
  if (recipe.title) {
    recipe.title = recipe.title.trim();
    // Remove "Recipe" suffix if present
    recipe.title = recipe.title.replace(/\s+Recipe$/i, '');
  }

  // Clean description
  if (recipe.description) {
    recipe.description = recipe.description.trim();
  }

  // Normalize cuisine
  const validCuisines = ['American', 'Italian', 'Mexican', 'Asian', 'French', 'Mediterranean', 'Indian', 'Caribbean', 'Other'];
  if (recipe.cuisine && !validCuisines.includes(recipe.cuisine)) {
    recipe.cuisine = 'Other';
  }

  // Normalize meal_type
  const validMealTypes = ['breakfast', 'lunch', 'dinner', 'dessert', 'snack', 'appetizer', 'side'];
  if (recipe.meal_type && !validMealTypes.includes(recipe.meal_type.toLowerCase())) {
    recipe.meal_type = 'dinner'; // Default
  }

  // Normalize difficulty
  const validDifficulties = ['easy', 'medium', 'hard'];
  if (recipe.difficulty && !validDifficulties.includes(recipe.difficulty.toLowerCase())) {
    recipe.difficulty = 'medium'; // Default
  }

  // Ensure tags is an array
  if (!recipe.tags) {
    recipe.tags = [];
  } else if (!Array.isArray(recipe.tags)) {
    recipe.tags = [recipe.tags];
  }

  // Convert servings to string if it's a number
  if (typeof recipe.servings === 'number') {
    recipe.servings = recipe.servings.toString();
  }

  return recipe;
}

module.exports = {
  parseRecipe,
  validateRecipe,
  estimateMissingData,
  normalizeRecipe
};
