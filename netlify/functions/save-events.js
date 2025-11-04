// Save events.json to Dropbox (writable storage)
const fetch = require('node-fetch');

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
    const body = JSON.parse(event.body);
    const { events } = body;

    // Use token from body if provided, otherwise use app token
    let accessToken = body.accessToken;

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

    if (!events) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Events data required' })
      };
    }

    // Upload to Dropbox
    const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/octet-stream',
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/events.json',
          mode: 'overwrite',
          autorename: false,
          mute: false
        })
      },
      body: JSON.stringify(events, null, 2)
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
        message: 'Events saved to Dropbox',
        result
      })
    };

  } catch (error) {
    console.error('Error saving events:', error);
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
