// Fergi Cooking v2.0 - Record Guest Selection Function (Dropbox storage)

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

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
      console.log('Selections file not found in Dropbox, returning empty array');
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

async function saveSelectionsToDropbox(accessToken, selections) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/guest-selections.json',
        mode: 'overwrite',
        autorename: false,
        mute: false
      })
    },
    body: JSON.stringify(selections, null, 2)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Failed to save selections: ${errorText}`);
  }

  return await response.json();
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

    if (event.httpMethod === 'GET') {
      // Get selections
      const selections = await loadSelectionsFromDropbox(accessToken);
      const recipes = await loadRecipesFromDropbox(accessToken);
      const event_id = event.queryStringParameters?.event_id;
      const guest_email = event.queryStringParameters?.guest_email;

      let filtered = selections;

      if (event_id) {
        filtered = filtered.filter(s => s.event_id == event_id);
      }

      if (guest_email) {
        filtered = filtered.filter(s => s.guest_email === guest_email);
      }

      // Enrich selections with recipe details
      const enriched = filtered.map(sel => {
        if (sel.recipe_id) {
          const recipe = recipes.find(r => r.id == sel.recipe_id);
          if (recipe) {
            return {
              ...sel,
              recipe_title: recipe.title,
              recipe_description: recipe.description
            };
          }
        }
        return sel;
      });

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify(enriched)
      };

    } else if (event.httpMethod === 'POST') {
      // Record selection
      const data = JSON.parse(event.body);
      const { event_id, guest_email, guest_name, recipe_id, variant_id, selection_type, notes, bringing_own_dish_name, bringing_own_dish_description } = data;

      // Load existing selections
      const selections = await loadSelectionsFromDropbox(accessToken);

      // Create new selection
      const newSelection = {
        id: Date.now(),
        event_id,
        guest_email,
        guest_name: guest_name || null,
        recipe_id: recipe_id || null,
        variant_id: variant_id || null,
        selection_type,
        notes: notes || null,
        bringing_own_dish_name: bringing_own_dish_name || null,
        bringing_own_dish_description: bringing_own_dish_description || null,
        created_at: new Date().toISOString()
      };

      // Check for duplicates (same guest, same recipe/type for same event)
      const existingIndex = selections.findIndex(s =>
        s.event_id == event_id &&
        s.guest_email === guest_email &&
        s.recipe_id == recipe_id &&
        s.selection_type === selection_type
      );

      if (existingIndex !== -1) {
        // Update existing selection
        selections[existingIndex] = { ...selections[existingIndex], ...newSelection, id: selections[existingIndex].id };
      } else {
        // Add new selection
        selections.push(newSelection);
      }

      // Save back to Dropbox
      await saveSelectionsToDropbox(accessToken, selections);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Selection recorded successfully'
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
