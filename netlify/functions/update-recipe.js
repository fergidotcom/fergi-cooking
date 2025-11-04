/**
 * Netlify Function: Update a single recipe
 * PUT /api/recipes/:id
 */

const fetch = require('node-fetch');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'PUT, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only allow PUT requests
  if (event.httpMethod !== 'PUT') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Extract recipe ID from path
    const pathParts = event.path.split('/');
    const recipeId = parseInt(pathParts[pathParts.length - 1]);

    console.log('Update recipe - ID:', recipeId, 'Path:', event.path);

    if (!recipeId || isNaN(recipeId)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, error: 'Invalid recipe ID' })
      };
    }

    // Parse the updated recipe data from request body
    const updatedRecipe = JSON.parse(event.body);
    console.log('Update recipe - Data received:', JSON.stringify(updatedRecipe, null, 2));

    // Get access token from user or use app token
    let accessToken = updatedRecipe.accessToken;
    if (!accessToken) {
      accessToken = process.env.DROPBOX_ACCESS_TOKEN;
    }

    if (!accessToken) {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({ error: 'Access token required' })
      };
    }

    // First, load the current recipes.json from Dropbox
    console.log('Loading recipes from Dropbox...');
    const downloadResponse = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/recipes.json'
        })
      }
    });

    if (!downloadResponse.ok) {
      const errorText = await downloadResponse.text();
      console.error('Failed to load recipes from Dropbox:', errorText);

      // Check for expired token
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { error: errorText };
      }

      if (errorData.error &&
          (errorData.error['.tag'] === 'expired_access_token' ||
           errorData.error_summary?.includes('expired_access_token'))) {
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Token expired',
            expired: true
          })
        };
      }

      // Return the actual Dropbox error message to help debug
      return {
        statusCode: downloadResponse.status,
        headers,
        body: JSON.stringify({
          success: false,
          error: `Failed to load recipes: ${errorText}`,
          dropboxError: errorData
        })
      };
    }

    const recipesText = await downloadResponse.text();
    const recipes = JSON.parse(recipesText);

    // Find and update the specific recipe
    const recipeIndex = recipes.findIndex(r => r.id === recipeId);

    if (recipeIndex === -1) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ success: false, error: 'Recipe not found' })
      };
    }

    // Update the recipe, preserving id and any fields not in the update
    recipes[recipeIndex] = {
      ...recipes[recipeIndex],
      ...updatedRecipe,
      id: recipeId  // Ensure ID doesn't change
    };

    console.log(`Updated recipe ${recipeId}`);

    // Save the updated recipes back to Dropbox
    console.log('Saving updated recipes to Dropbox...');
    const uploadResponse = await fetch('https://content.dropboxapi.com/2/files/upload', {
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

    if (!uploadResponse.ok) {
      const errorText = await uploadResponse.text();
      console.error('Failed to save recipes to Dropbox:', errorText);

      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { error: errorText };
      }

      return {
        statusCode: uploadResponse.status,
        headers,
        body: JSON.stringify({
          success: false,
          error: `Failed to save recipes: ${errorText}`,
          dropboxError: errorData
        })
      };
    }

    const result = await uploadResponse.json();

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Recipe updated successfully',
        recipe: recipes[recipeIndex],
        result
      })
    };

  } catch (error) {
    console.error('Error updating recipe:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message,
        stack: error.stack,
        details: 'Check function logs for more information'
      })
    };
  }
};
