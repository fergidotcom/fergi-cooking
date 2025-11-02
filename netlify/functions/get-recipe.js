/**
 * Netlify Function: Get single recipe by ID
 * GET /api/recipe/:id
 */

const fs = require('fs');
const path = require('path');

exports.handler = async (event, context) => {
  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      body: JSON.stringify({ success: false, error: 'Method not allowed' })
    };
  }

  try {
    // Extract recipe ID from path
    // Path will be like: /.netlify/functions/get-recipe/123
    const pathParts = event.path.split('/');
    const recipeId = parseInt(pathParts[pathParts.length - 1]);

    if (!recipeId || isNaN(recipeId)) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          success: false,
          error: 'Invalid recipe ID'
        })
      };
    }

    // Read recipes from JSON file
    // In Netlify, files are in the root directory relative to the function
    let recipesData;
    try {
      // Try relative to function directory (development)
      const devPath = path.join(__dirname, '../../recipes.json');
      recipesData = JSON.parse(fs.readFileSync(devPath, 'utf8'));
    } catch (e) {
      // Try from root (Netlify production)
      const prodPath = path.join(process.cwd(), 'recipes.json');
      recipesData = JSON.parse(fs.readFileSync(prodPath, 'utf8'));
    }

    // Find recipe by ID
    const recipe = recipesData.find(r => r.id === recipeId);

    if (!recipe) {
      return {
        statusCode: 404,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({
          success: false,
          error: 'Recipe not found'
        })
      };
    }

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        recipe: recipe
      })
    };
  } catch (error) {
    console.error('Error in get-recipe:', error);
    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
