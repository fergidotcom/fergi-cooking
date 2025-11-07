/**
 * Parse Recipe - AI-Powered Recipe Extraction
 * Combines extract-file and recipe parsing into single endpoint
 * Used by enhanced Add Recipe UI
 */

const { parseRecipeWithAI, validateEmbeddedIngredients, completeRecipeData, estimateMissingData } = require('./lib/recipe-parser');

exports.handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only allow POST
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { extractedText, filename, contributorId } = JSON.parse(event.body);

    if (!extractedText) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'No extracted text provided' })
      };
    }

    console.log('Parsing recipe with AI...', { filename, textLength: extractedText.length });

    // Step 1: Parse recipe with AI
    let recipe = await parseRecipeWithAI(extractedText, filename);

    console.log('Initial parse complete:', recipe.title);

    // Step 2: Estimate missing data if needed
    const missingFields = [];
    if (!recipe.prep_time) missingFields.push('prep_time');
    if (!recipe.cook_time) missingFields.push('cook_time');
    if (!recipe.servings) missingFields.push('servings');
    if (!recipe.calories_per_serving) missingFields.push('calories_per_serving');

    if (missingFields.length > 0) {
      console.log('Estimating missing fields:', missingFields);
      recipe = await estimateMissingData(recipe);
    }

    // Step 3: Validate embedded ingredients in instructions
    const validation = validateEmbeddedIngredients(recipe.instructions);
    if (!validation.valid) {
      console.warn('Instructions validation issues:', validation.issues);
      recipe.needs_review = true;
      recipe.validation_issues = validation.issues;
    }

    // Step 4: Complete recipe data structure
    recipe = completeRecipeData(recipe, contributorId);

    console.log('Recipe parsing complete:', {
      title: recipe.title,
      ingredients: recipe.ingredients.length,
      instructions: recipe.instructions.length,
      needs_review: recipe.needs_review
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        recipe: recipe,
        validation: validation,
        message: recipe.needs_review
          ? 'Recipe extracted but needs review'
          : 'Recipe extracted successfully'
      })
    };

  } catch (error) {
    console.error('Parse recipe error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        error: 'Failed to parse recipe',
        details: error.message
      })
    };
  }
};
