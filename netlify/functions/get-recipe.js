/**
 * Netlify Function: Get or Update single recipe by ID
 * GET /api/recipes/:id - Get recipe
 * PUT /api/recipes/:id - Update recipe
 */

const fs = require('fs');
const path = require('path');
const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

// Load recipes data - try multiple paths for different environments
let recipesData = null;

function loadRecipes() {
  if (recipesData) return recipesData;

  const possiblePaths = [
    path.join(__dirname, '../../recipes.json'),
    path.join(process.cwd(), 'recipes.json'),
    '/var/task/recipes.json',
    path.join(__dirname, '../../../recipes.json'),
  ];

  for (const filepath of possiblePaths) {
    try {
      recipesData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      console.log(`Loaded recipes from: ${filepath}`);
      return recipesData;
    } catch (e) {
      console.log(`Failed to load from ${filepath}: ${e.message}`);
    }
  }

  throw new Error('Could not find recipes.json in any known location');
}

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, PUT, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Extract recipe ID from path
  const pathParts = event.path.split('/');
  const recipeId = parseInt(pathParts[pathParts.length - 1]);

  console.log(`${event.httpMethod} request for recipe ID:`, recipeId, 'Path:', event.path);

  if (!recipeId || isNaN(recipeId)) {
    return {
      statusCode: 400,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Invalid recipe ID'
      })
    };
  }

  // === GET: Return single recipe ===
  if (event.httpMethod === 'GET') {
    try {
      const recipesData = loadRecipes();
      const recipe = recipesData.find(r => r.id === recipeId);

      if (!recipe) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Recipe not found'
          })
        };
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          recipe: recipe
        })
      };
    } catch (error) {
      console.error('Error getting recipe:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          success: false,
          error: error.message
        })
      };
    }
  }

  // === PUT: Update recipe ===
  if (event.httpMethod === 'PUT') {
    try {
      // Parse the updated recipe data from request body
      const updatedRecipe = JSON.parse(event.body);
      console.log('Update recipe - Data received:', JSON.stringify(updatedRecipe, null, 2));

      // Get a valid access token (auto-refreshes if needed)
      const accessToken = await getValidAccessToken();
      console.log('Got valid access token for recipe update');

      // Load current recipes from Dropbox
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

        let errorData;
        try {
          errorData = JSON.parse(errorText);
        } catch (e) {
          errorData = { error: errorText };
        }

        // Check for expired token
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

      // Save updated recipes back to Dropbox
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
          stack: error.stack
        })
      };
    }
  }

  // If not GET or PUT, return method not allowed
  return {
    statusCode: 405,
    headers,
    body: JSON.stringify({ success: false, error: 'Method not allowed' })
  };
};
