/**
 * Netlify Function: Get all recipes (with optional search and filtering)
 * GET /api/recipes?search=query&limit=10&offset=0&contributor=Name
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
      console.log('Recipes file not found in Dropbox, returning empty array');
      return [];
    }

    const recipesJson = await response.text();
    return JSON.parse(recipesJson);
  } catch (error) {
    console.log('Error loading recipes from Dropbox:', error);
    return [];
  }
}

exports.handler = async (event, context) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS'
  };

  // Handle OPTIONS for CORS
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ success: false, error: 'Method not allowed' })
    };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    // Load recipes data from Dropbox
    let recipesData = await loadRecipesFromDropbox(accessToken);

    // Apply bulk contributor assignment for recipes without contributor
    recipesData = recipesData.map(recipe => {
      if (!recipe.contributor) {
        // Check if it's from Janet Mason's cookbook
        if (recipe.source_attribution === "Janet Mason's Cookbook" ||
            recipe.tags?.includes("Janet Mason") ||
            recipe.tags?.includes("Janet Mason's Cookbook")) {
          recipe.contributor = "Janet Mason";
        } else {
          recipe.contributor = "Fergi";
        }
      }
      return recipe;
    });

    // Parse query parameters
    const params = event.queryStringParameters || {};
    const search = params.search || '';
    const contributor = params.contributor || '';
    const limit = params.limit ? parseInt(params.limit) : null;
    const offset = params.offset ? parseInt(params.offset) : 0;

    let recipes = recipesData;

    // Apply contributor filter if provided
    if (contributor) {
      recipes = recipes.filter(recipe =>
        recipe.contributor && recipe.contributor.toLowerCase() === contributor.toLowerCase()
      );
    }

    // Apply search filter if provided
    if (search) {
      const searchLower = search.toLowerCase();
      recipes = recipes.filter(recipe => {
        // Search in title, description, ingredients, cuisine, meal type, tags
        const titleMatch = recipe.title && recipe.title.toLowerCase().includes(searchLower);
        const descMatch = recipe.description && recipe.description.toLowerCase().includes(searchLower);
        const cuisineMatch = recipe.cuisine_type && recipe.cuisine_type.toLowerCase().includes(searchLower);
        const mealTypeMatch = recipe.meal_type && recipe.meal_type.toLowerCase().includes(searchLower);
        const tagsMatch = recipe.tags && recipe.tags.some(tag =>
          tag.toLowerCase().includes(searchLower)
        );
        const ingredientMatch = recipe.ingredients && recipe.ingredients.some(ing =>
          ing.ingredient_name && ing.ingredient_name.toLowerCase().includes(searchLower)
        );
        const instructionMatch = recipe.instructions && recipe.instructions.some(inst =>
          inst.instruction_text && inst.instruction_text.toLowerCase().includes(searchLower)
        );

        return titleMatch || descMatch || cuisineMatch || mealTypeMatch ||
               tagsMatch || ingredientMatch || instructionMatch;
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
      contributor: r.contributor,
      rating: r.rating,
      favorite: r.favorite,
      prep_time_minutes: r.prep_time_minutes,
      cook_time_minutes: r.cook_time_minutes,
      total_time_minutes: r.total_time_minutes,
      servings: r.servings,
      calories_per_serving: r.calories_per_serving,
      date_added: r.date_added,
      date_modified: r.date_modified,
      tags: r.tags
    }));

    // Apply pagination
    const total = summaryRecipes.length;
    const paginatedRecipes = limit
      ? summaryRecipes.slice(offset, offset + limit)
      : summaryRecipes.slice(offset);

    return {
      statusCode: 200,
      headers,
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
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message
      })
    };
  }
};
