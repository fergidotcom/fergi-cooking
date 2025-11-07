/**
 * Recipe Parser Library
 * AI-powered recipe extraction and formatting
 * Used by both batch processing and Add Recipe feature
 */

const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

/**
 * Parse recipe text with AI to structure recipe data
 * @param {string} recipeText - Extracted text from recipe file
 * @param {string} filename - Original filename for context
 * @returns {Promise<Object>} Structured recipe data
 */
async function parseRecipeWithAI(recipeText, filename = '') {
  const prompt = `You are a recipe parsing expert. Extract and structure the following recipe text into a clean, well-formatted recipe.

CRITICAL REQUIREMENTS:
1. **Instructions with Embedded Ingredients**: Each cooking step that uses ingredients MUST include the specific quantities in the step itself. The cook should NEVER need to refer back to the ingredients list while cooking.

Example of GOOD instructions:
- "In a large Dutch oven, cook 4 slices of chopped bacon over medium heat until crispy. Remove and set aside."
- "Add 1 large diced onion and 3 minced garlic cloves to the pot. Sauté until softened, about 5 minutes."

Example of BAD instructions (DO NOT DO THIS):
- "Cook the bacon until crispy."
- "Add onion and garlic, sauté until softened."

2. Generate missing data if not present in the recipe:
   - Description: 1-3 sentences describing the dish
   - Prep time: Realistic estimate in minutes
   - Cook time: Realistic estimate in minutes
   - Servings: Based on ingredient quantities
   - Calories per serving: Reasonable estimate
   - Cuisine type (Italian, French, American, etc.)
   - Meal type (dinner, lunch, breakfast, dessert)
   - Difficulty (easy, medium, hard)

3. Extract or infer source attribution if mentioned

Recipe Text:
${recipeText}

${filename ? `Filename: ${filename}` : ''}

Respond with a JSON object in this exact format:
{
  "title": "Recipe Name",
  "description": "1-3 sentence description",
  "ingredients": [
    "2 lbs beef chuck, cut into 2-inch cubes",
    "4 slices bacon, chopped"
  ],
  "instructions": [
    "Step 1 with quantities included...",
    "Step 2 with quantities included..."
  ],
  "prep_time": 30,
  "cook_time": 180,
  "servings": "6",
  "calories_per_serving": 520,
  "cuisine": "French",
  "meal_type": "dinner",
  "difficulty": "medium",
  "source_attribution": "Source name if mentioned",
  "needs_review": false,
  "extraction_notes": "Any uncertainties or issues"
}

If you're uncertain about any data, set needs_review to true and explain in extraction_notes.
Return ONLY valid JSON, no markdown or explanations.`;

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4000,
      messages: [{
        role: 'user',
        content: prompt
      }]
    });

    const responseText = message.content[0].text;

    // Extract JSON from response (handle markdown code blocks)
    let jsonText = responseText.trim();
    if (jsonText.startsWith('```json')) {
      jsonText = jsonText.replace(/```json\n?/g, '').replace(/```\n?/g, '');
    } else if (jsonText.startsWith('```')) {
      jsonText = jsonText.replace(/```\n?/g, '');
    }

    const recipe = JSON.parse(jsonText);

    // Validate required fields
    const requiredFields = ['title', 'ingredients', 'instructions'];
    const missingFields = requiredFields.filter(field => !recipe[field]);

    if (missingFields.length > 0) {
      throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
    }

    // Ensure arrays
    if (!Array.isArray(recipe.ingredients)) {
      recipe.ingredients = [recipe.ingredients];
    }
    if (!Array.isArray(recipe.instructions)) {
      recipe.instructions = [recipe.instructions];
    }

    return recipe;

  } catch (error) {
    console.error('AI parsing error:', error);
    throw new Error(`Failed to parse recipe with AI: ${error.message}`);
  }
}

/**
 * Validate that instructions have embedded ingredient quantities
 * @param {Array<string>} instructions - Recipe instructions
 * @returns {Object} Validation result with issues
 */
function validateEmbeddedIngredients(instructions) {
  const issues = [];

  instructions.forEach((instruction, index) => {
    // Check if instruction mentions ingredients but lacks quantities
    const hasIngredientWords = /\b(add|stir|mix|combine|cook|brown|sauté|heat)\b/i.test(instruction);
    const hasQuantity = /\d+\s*(cup|tablespoon|teaspoon|lb|oz|slice|piece|clove|g|ml|inch)/i.test(instruction);
    const hasIngredientName = /\b(beef|chicken|bacon|onion|garlic|butter|flour|sugar|salt|pepper|oil)\b/i.test(instruction);

    if (hasIngredientWords && hasIngredientName && !hasQuantity) {
      issues.push({
        step: index + 1,
        text: instruction,
        issue: 'Mentions ingredients but lacks specific quantities'
      });
    }
  });

  return {
    valid: issues.length === 0,
    issues: issues
  };
}

/**
 * Complete recipe data structure
 * Ensures all required fields are present with defaults
 * @param {Object} recipe - Partial recipe data
 * @param {number} contributorId - Contributor ID (1=Fergi, 2=Janet)
 * @returns {Object} Complete recipe data
 */
function completeRecipeData(recipe, contributorId = null) {
  const defaults = {
    description: recipe.description || '',
    prep_time: recipe.prep_time || null,
    cook_time: recipe.cook_time || null,
    servings: recipe.servings || null,
    difficulty: recipe.difficulty || null,
    cuisine: recipe.cuisine || null,
    meal_type: recipe.meal_type || null,
    source_attribution: recipe.source_attribution || null,
    contributor_id: contributorId || recipe.contributor_id || null,
    needs_review: recipe.needs_review || false,
    calories_per_serving: recipe.calories_per_serving || null,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  };

  return {
    ...defaults,
    ...recipe,
    // Ensure these are always present
    title: recipe.title,
    ingredients: recipe.ingredients || [],
    instructions: recipe.instructions || []
  };
}

/**
 * Estimate missing recipe data using AI
 * @param {Object} recipe - Recipe with some missing fields
 * @returns {Promise<Object>} Recipe with estimated fields
 */
async function estimateMissingData(recipe) {
  const missingFields = [];
  if (!recipe.prep_time) missingFields.push('prep_time');
  if (!recipe.cook_time) missingFields.push('cook_time');
  if (!recipe.servings) missingFields.push('servings');
  if (!recipe.calories_per_serving) missingFields.push('calories_per_serving');
  if (!recipe.description) missingFields.push('description');

  if (missingFields.length === 0) {
    return recipe;
  }

  const prompt = `Given this recipe, estimate the missing fields: ${missingFields.join(', ')}

Recipe: ${recipe.title}
Ingredients: ${recipe.ingredients.join(', ')}
Instructions: ${recipe.instructions.slice(0, 3).join(' ')}

Return JSON with only the missing fields:
{
  ${missingFields.includes('prep_time') ? '"prep_time": 30,' : ''}
  ${missingFields.includes('cook_time') ? '"cook_time": 60,' : ''}
  ${missingFields.includes('servings') ? '"servings": "4-6",' : ''}
  ${missingFields.includes('calories_per_serving') ? '"calories_per_serving": 450,' : ''}
  ${missingFields.includes('description') ? '"description": "Description here"' : ''}
}`;

  try {
    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 1000,
      messages: [{ role: 'user', content: prompt }]
    });

    let jsonText = message.content[0].text.trim();
    if (jsonText.startsWith('```')) {
      jsonText = jsonText.replace(/```json\n?/g, '').replace(/```\n?/g, '');
    }

    const estimates = JSON.parse(jsonText);
    return { ...recipe, ...estimates };

  } catch (error) {
    console.error('Estimation error:', error);
    return recipe; // Return original if estimation fails
  }
}

module.exports = {
  parseRecipeWithAI,
  validateEmbeddedIngredients,
  completeRecipeData,
  estimateMissingData
};
