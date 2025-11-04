/**
 * Save recipes.json to Dropbox (writable storage)
 * POST with { recipes: [...] } to save entire recipes array
 */

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { recipes } = JSON.parse(event.body);

    if (!recipes || !Array.isArray(recipes)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Recipes array required' })
      };
    }

    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    // Upload to Dropbox
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
      let errorData;
      try {
        errorData = JSON.parse(errorText);
      } catch (e) {
        errorData = { error: errorText };
      }

      // Check if token is expired
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

      throw new Error(`Dropbox API error: ${errorText}`);
    }

    const result = await response.json();

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Recipes saved to Dropbox',
        count: recipes.length,
        result
      })
    };

  } catch (error) {
    console.error('Error saving recipes:', error);
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
