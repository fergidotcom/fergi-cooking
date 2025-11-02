/**
 * Netlify Function: Get all recipes (with optional search)
 * GET /api/recipes?search=query&limit=10&offset=0
 */

const fs = require('fs');
const path = require('path');

// Load recipes data - try multiple paths for different environments
let recipesData = null;

function loadRecipes() {
  if (recipesData) return recipesData;

  const possiblePaths = [
    path.join(__dirname, '../../recipes.json'),           // Local dev
    path.join(process.cwd(), 'recipes.json'),              // Netlify root
    '/var/task/recipes.json',                              // Netlify function root
    path.join(__dirname, '../../../recipes.json'),         // One level up
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
    // Load recipes data
    const recipesData = loadRecipes();

    // Parse query parameters
    const params = event.queryStringParameters || {};
    const search = params.search || '';
    const limit = params.limit ? parseInt(params.limit) : null;
    const offset = params.offset ? parseInt(params.offset) : 0;

    let recipes = recipesData;

    // Apply search filter if provided
    if (search) {
      const searchLower = search.toLowerCase();
      recipes = recipes.filter(recipe => {
        // Search in title, description, ingredients
        const titleMatch = recipe.title && recipe.title.toLowerCase().includes(searchLower);
        const descMatch = recipe.description && recipe.description.toLowerCase().includes(searchLower);
        const ingredientMatch = recipe.ingredients && recipe.ingredients.some(ing =>
          ing.ingredient_name && ing.ingredient_name.toLowerCase().includes(searchLower)
        );
        const instructionMatch = recipe.instructions && recipe.instructions.some(inst =>
          inst.instruction_text && inst.instruction_text.toLowerCase().includes(searchLower)
        );

        return titleMatch || descMatch || ingredientMatch || instructionMatch;
      });
    }

    // Return summary view (not full details)
    const summaryRecipes = recipes.map(r => ({
      id: r.id,
      title: r.title,
      description: r.description,
      cuisine_type: r.cuisine_type,
      meal_type: r.meal_type,
      source_attribution: r.source_attribution,
      rating: r.rating,
      favorite: r.favorite,
      prep_time_minutes: r.prep_time_minutes,
      cook_time_minutes: r.cook_time_minutes,
      total_time_minutes: r.total_time_minutes,
      servings: r.servings,
      calories_per_serving: r.calories_per_serving,
      date_added: r.date_added,
      date_modified: r.date_modified
    }));

    // Apply pagination
    const total = summaryRecipes.length;
    const paginatedRecipes = limit
      ? summaryRecipes.slice(offset, offset + limit)
      : summaryRecipes.slice(offset);

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        count: paginatedRecipes.length,
        total: total,
        recipes: paginatedRecipes
      })
    };
  } catch (error) {
    console.error('Error in get-recipes:', error);
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
