/**
 * Format recipe using Claude API to Ferguson family standards
 * Takes raw recipe text and returns formatted recipe JSON
 */

const Anthropic = require('@anthropic-ai/sdk');

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY
});

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle OPTIONS for CORS
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Method not allowed'
      })
    };
  }

  try {
    const { text, contributor, original_filename } = JSON.parse(event.body);

    if (!text) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Recipe text is required'
        })
      };
    }

    console.log(`Formatting recipe for contributor: ${contributor}`);
    console.log(`Recipe text length: ${text.length} characters`);

    const prompt = `You are formatting a recipe for the Ferguson family cookbook. Convert the provided text into the Ferguson standard format.

CRITICAL REQUIREMENTS:
1. **Ingredients list**: Clean quantities for shopping reference (e.g., "2 cups all-purpose flour", "1 cup granulated sugar")
2. **Instructions**: Step-by-step with quantities embedded in each step (e.g., "Mix 2 cups flour with 1 cup sugar")
3. **BOTH sections must include quantities** - this redundancy is intentional (ingredients for shopping, instructions for cooking)
4. If prep time, cook time, or servings are not provided, make reasonable estimates based on the recipe
5. Add relevant tags for searchability (e.g., "quick", "easy", "vegetarian", "dessert", "family-favorite")
6. Infer cuisine type (American, Italian, Mexican, Asian, French, Mediterranean, Indian, Other)
7. Classify meal type (breakfast, lunch, dinner, dessert, snack, appetizer)

INPUT TEXT:
${text}

OUTPUT (respond with ONLY valid JSON, no other text):
{
  "title": "Recipe Name",
  "description": "Brief 1-2 sentence description of the dish",
  "cuisine": "American",
  "meal_type": "dinner",
  "prep_time": 15,
  "cook_time": 30,
  "servings": "4-6 servings",
  "ingredients": [
    "2 cups all-purpose flour",
    "1 cup granulated sugar",
    "1/2 cup butter, softened",
    "2 eggs, beaten",
    "1 tsp vanilla extract"
  ],
  "instructions": [
    "Preheat oven to 350°F.",
    "In a large bowl, mix 2 cups all-purpose flour with 1 cup granulated sugar.",
    "Add 1/2 cup softened butter and beat until creamy.",
    "Mix in 2 beaten eggs and 1 tsp vanilla extract until well combined.",
    "Spread mixture in greased 9x13 pan and bake for 25-30 minutes until golden brown."
  ],
  "tags": ["quick", "easy", "dessert", "family-favorite"],
  "notes": "Optional cooking tips, serving suggestions, or variations"
}`;

    console.log('Sending request to Claude API...');

    const message = await anthropic.messages.create({
      model: 'claude-sonnet-4-20250514',
      max_tokens: 4000,
      temperature: 0.7,
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
    if (!recipe.title) {
      throw new Error('Recipe must have a title');
    }
    if (!recipe.ingredients || !Array.isArray(recipe.ingredients) || recipe.ingredients.length === 0) {
      throw new Error('Recipe must have ingredients');
    }
    if (!recipe.instructions || !Array.isArray(recipe.instructions) || recipe.instructions.length === 0) {
      throw new Error('Recipe must have instructions');
    }

    // Add metadata
    recipe.contributor = contributor;
    recipe.date_added = new Date().toISOString();
    recipe.import_method = original_filename ? 'file_upload' : 'text_paste';
    recipe.original_source = original_filename || 'Manual Entry';

    console.log(`Successfully formatted recipe: ${recipe.title}`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        recipe
      })
    };

  } catch (error) {
    console.error('Error formatting recipe:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
