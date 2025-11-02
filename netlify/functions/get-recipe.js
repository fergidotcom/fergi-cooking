/**
 * Netlify Function: Get single recipe by ID
 * GET /api/recipe/:id
 */

const fs = require('fs');
const path = require('path');

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

    // Load recipes data
    const recipesData = loadRecipes();

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
