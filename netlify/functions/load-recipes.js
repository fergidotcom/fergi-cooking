// Load recipes.json from Dropbox (writable storage)
const fetch = require('node-fetch');
const { getValidAccessToken, handleDropboxResponse } = require('./lib/dropbox-auth');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // Get valid access token from server (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();
    console.log('✅ Got valid server-side access token for recipe loading');

    // Download from Dropbox
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
      const errorText = await response.text();
      console.error('Dropbox API error:', errorText);
      throw new Error(`Dropbox API error: ${errorText}`);
    }

    const recipesJson = await response.text();
    const recipes = JSON.parse(recipesJson);
    console.log(`✅ Loaded ${recipes.length} recipes from Dropbox`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        recipes
      })
    };

  } catch (error) {
    console.error('Error loading recipes:', error);
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
