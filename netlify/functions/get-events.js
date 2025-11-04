// Fergi Cooking v2.0 - Get Events Function (Dropbox-based)

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

async function loadEventsFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/events.json'
        })
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

async function loadSelectionsFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/guest-selections.json'
        })
      }
    });

    if (!response.ok) {
      return [];
    }

    const selectionsJson = await response.text();
    return JSON.parse(selectionsJson);
  } catch (error) {
    console.log('Error loading selections from Dropbox:', error);
    return [];
  }
}

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
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    const events = await loadEventsFromDropbox(accessToken);
    const selections = await loadSelectionsFromDropbox(accessToken);
    const recipes = await loadRecipesFromDropbox(accessToken);
    const eventId = event.queryStringParameters?.id;

    if (eventId) {
      // Get single event
      const eventData = events.find(e => e.id == eventId);

      if (!eventData) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: 'Event not found' })
        };
      }

      // Add guest count and recipe count
      eventData.guest_count = selections.filter(s => s.event_id == eventId && s.guest_email)
        .map(s => s.guest_email)
        .filter((email, index, self) => self.indexOf(email) === index)
        .length;

      eventData.recipe_count = eventData.recipes ? eventData.recipes.length : 0;

      // Enhance recipes with full details
      if (eventData.recipes) {
        eventData.recipes = eventData.recipes.map(er => {
          const recipe = recipes.find(r => r.id == er.recipe_id);
          return recipe ? { ...recipe, ...er } : er;
        });
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(eventData)
      };

    } else {
      // Get all events with counts
      const enrichedEvents = events.map(evt => {
        const guestCount = selections.filter(s => s.event_id == evt.id && s.guest_email)
          .map(s => s.guest_email)
          .filter((email, index, self) => self.indexOf(email) === index)
          .length;

        const recipeCount = evt.recipes ? evt.recipes.length : 0;

        return {
          ...evt,
          guest_count: guestCount,
          recipe_count: recipeCount
        };
      });

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(enrichedEvents)
      };
    }

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};
