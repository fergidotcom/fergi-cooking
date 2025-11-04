// Fergi Cooking v2.0 - Event Recipes Management (Dropbox storage)

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

async function loadEventsFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({ path: '/Apps/Reference Refinement/events.json' })
      }
    });

    if (!response.ok) {
      console.log('Events file not found in Dropbox, returning empty array');
      return [];
    }

    const eventsJson = await response.text();
    return JSON.parse(eventsJson);
  } catch (error) {
    console.log('Error loading events from Dropbox:', error);
    return [];
  }
}

async function loadRecipesFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({ path: '/Apps/Reference Refinement/recipes.json' })
      }
    });

    if (!response.ok) {
      return [];
    }

    const recipesJson = await response.text();
    return JSON.parse(recipesJson);
  } catch (error) {
    console.log('Error loading recipes from Dropbox:', error);
    return [];
  }
}

async function saveEventsToDropbox(accessToken, events) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/events.json',
        mode: 'overwrite',
        autorename: false
      })
    },
    body: JSON.stringify(events, null, 2)
  });

  if (!response.ok) {
    throw new Error('Failed to save events to Dropbox');
  }

  return response.json();
}

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    const events = await loadEventsFromDropbox(accessToken);
    const recipes = await loadRecipesFromDropbox(accessToken);

    if (event.httpMethod === 'POST') {
      // Add recipe to event
      const data = JSON.parse(event.body);
      const { event_id, recipe_id, course_type } = data;

      const eventIndex = events.findIndex(e => e.id == event_id);
      if (eventIndex === -1) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: 'Event not found' })
        };
      }

      // Find recipe details
      const recipe = recipes.find(r => r.id == recipe_id);
      if (!recipe) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: 'Recipe not found' })
        };
      }

      // Initialize recipes array if needed
      if (!events[eventIndex].recipes) {
        events[eventIndex].recipes = [];
      }

      // Check if recipe already added
      const alreadyAdded = events[eventIndex].recipes.find(r => r.recipe_id == recipe_id);
      if (alreadyAdded) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({ error: 'Recipe already added to this event' })
        };
      }

      // Add recipe with metadata
      events[eventIndex].recipes.push({
        recipe_id: parseInt(recipe_id),
        course_type: course_type || 'main',
        added_at: new Date().toISOString()
      });

      // Update event timestamp
      events[eventIndex].updated_at = new Date().toISOString();

      // Save back to Dropbox
      await saveEventsToDropbox(accessToken, events);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Recipe added to event'
        })
      };

    } else if (event.httpMethod === 'DELETE') {
      // Remove recipe from event
      const eventId = event.queryStringParameters?.event_id;
      const recipeId = event.queryStringParameters?.recipe_id;

      const eventIndex = events.findIndex(e => e.id == eventId);
      if (eventIndex === -1) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: 'Event not found' })
        };
      }

      if (!events[eventIndex].recipes) {
        events[eventIndex].recipes = [];
      }

      // Remove recipe
      events[eventIndex].recipes = events[eventIndex].recipes.filter(r => r.recipe_id != recipeId);
      events[eventIndex].updated_at = new Date().toISOString();

      // Save back to Dropbox
      await saveEventsToDropbox(accessToken, events);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Recipe removed from event'
        })
      };
    }

    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
