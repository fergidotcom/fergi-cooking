/**
 * Add a new recipe to the collection
 * Loads recipes from Dropbox, adds new recipe, saves back to Dropbox
 */

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

async function loadRecipesFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/recipes.json'
        })
      }
    });

    if (!response.ok) {
      console.log('Recipes file not found in Dropbox, starting with empty array');
      return [];
    }

    const recipesJson = await response.text();
    return JSON.parse(recipesJson);
  } catch (error) {
    console.log('Error loading recipes from Dropbox:', error);
    return [];
  }
}

async function saveRecipesToDropbox(accessToken, recipes) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/recipes.json',
        mode: 'overwrite',
        autorename: false,
        mute: false
      })
    },
    body: JSON.stringify(recipes, null, 2)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Dropbox API error: ${errorText}`);
  }

  return await response.json();
}

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
    const { recipe } = JSON.parse(event.body);

    // Validate required fields
    if (!recipe || !recipe.title) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Recipe with title is required'
        })
      };
    }

    if (!recipe.ingredients || recipe.ingredients.length === 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Recipe must have ingredients'
        })
      };
    }

    if (!recipe.instructions || recipe.instructions.length === 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Recipe must have instructions'
        })
      };
    }

    console.log(`Adding recipe: ${recipe.title}`);
    console.log(`Contributor: ${recipe.contributor}`);

    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    // Load existing recipes
    const recipes = await loadRecipesFromDropbox(accessToken);

    console.log(`Loaded ${recipes.length} existing recipes`);

    // Generate new ID
    const maxId = recipes.reduce((max, r) => Math.max(max, r.id || 0), 0);
    recipe.id = maxId + 1;

    console.log(`Assigned recipe ID: ${recipe.id}`);

    // Add current timestamp if not already set
    if (!recipe.date_added) {
      recipe.date_added = new Date().toISOString();
    }

    // Set date_modified
    recipe.date_modified = new Date().toISOString();

    // Add default values
    if (recipe.favorite === undefined) recipe.favorite = 0;
    if (recipe.rating === undefined) recipe.rating = null;
    if (!recipe.source_attribution) recipe.source_attribution = recipe.original_source || 'Manual Entry';

    // Add to array
    recipes.push(recipe);

    console.log(`Total recipes after add: ${recipes.length}`);

    // Save back to Dropbox
    await saveRecipesToDropbox(accessToken, recipes);

    console.log('✅ Recipe saved successfully to Dropbox');

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        recipe_id: recipe.id,
        message: `Recipe "${recipe.title}" saved successfully! Changes are immediately visible.`,
        total_recipes: recipes.length
      })
    };

  } catch (error) {
    console.error('Error adding recipe:', error);
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
