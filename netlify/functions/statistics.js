/**
 * Netlify Function: Get database statistics
 * GET /api/statistics
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
    // Read recipes from JSON file
    const recipesPath = path.join(__dirname, '../../recipes.json');
    const recipesData = JSON.parse(fs.readFileSync(recipesPath, 'utf8'));

    // Calculate statistics
    const stats = {};

    // Total recipes
    stats.total_recipes = recipesData.length;

    // Recipes by source
    const sourceCount = {};
    recipesData.forEach(recipe => {
      const source = recipe.source_attribution || 'Unknown';
      sourceCount[source] = (sourceCount[source] || 0) + 1;
    });
    stats.by_source = Object.entries(sourceCount)
      .map(([source_attribution, count]) => ({ source_attribution, count }))
      .sort((a, b) => b.count - a.count);

    // Recipes by cuisine
    const cuisineCount = {};
    recipesData.forEach(recipe => {
      if (recipe.cuisine_type) {
        cuisineCount[recipe.cuisine_type] = (cuisineCount[recipe.cuisine_type] || 0) + 1;
      }
    });
    stats.by_cuisine = Object.entries(cuisineCount)
      .map(([cuisine_type, count]) => ({ cuisine_type, count }))
      .sort((a, b) => b.count - a.count);

    // Favorite recipes
    stats.favorites = recipesData.filter(r => r.favorite === 1).length;

    // Janet's recipes count
    stats.janet_recipes = recipesData.filter(r =>
      r.source_attribution && r.source_attribution.includes('Janet')
    ).length;

    // Main recipes count
    stats.main_recipes = recipesData.filter(r =>
      !r.source_attribution || !r.source_attribution.includes('Janet')
    ).length;

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: true,
        statistics: stats
      })
    };
  } catch (error) {
    console.error('Error in statistics:', error);
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
