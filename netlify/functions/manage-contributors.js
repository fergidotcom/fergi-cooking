/**
 * Manage Contributors - Dropbox-based storage
 * GET: Return current contributors
 * POST: Add new contributor
 * PUT: Replace entire contributor list
 * DELETE: Remove contributor (only if no recipes associated)
 */

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

async function loadContributorsFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/contributors.json'
        })
      }
    });

    if (!response.ok) {
      console.log('Contributors file not found in Dropbox, returning defaults');
      return {
        contributors: ["Janet Mason", "Fergi"],
        last_updated: new Date().toISOString()
      };
    }

    const contributorsJson = await response.text();
    return JSON.parse(contributorsJson);
  } catch (error) {
    console.log('Error loading contributors from Dropbox:', error);
    return {
      contributors: ["Janet Mason", "Fergi"],
      last_updated: new Date().toISOString()
    };
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

async function saveContributorsToDropbox(accessToken, contributorsData) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/contributors.json',
        mode: 'overwrite',
        autorename: false,
        mute: false
      })
    },
    body: JSON.stringify(contributorsData, null, 2)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Dropbox API error: ${errorText}`);
  }

  return await response.json();
}

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    // Load contributors
    let contributorsData = await loadContributorsFromDropbox(accessToken);

    // GET - Return current contributors
    if (event.httpMethod === 'GET') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          contributors: contributorsData.contributors,
          count: contributorsData.contributors.length
        })
      };
    }

    // POST - Add new contributor
    if (event.httpMethod === 'POST') {
      const { contributor } = JSON.parse(event.body);

      if (!contributor || typeof contributor !== 'string' || !contributor.trim()) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Contributor name is required and must be a non-empty string'
          })
        };
      }

      const trimmedContributor = contributor.trim();

      // Check if already exists (case-insensitive)
      if (contributorsData.contributors.some(c => c.toLowerCase() === trimmedContributor.toLowerCase())) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Contributor already exists'
          })
        };
      }

      // Add to list
      contributorsData.contributors.push(trimmedContributor);
      contributorsData.last_updated = new Date().toISOString();

      // Save to Dropbox
      await saveContributorsToDropbox(accessToken, contributorsData);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          contributors: contributorsData.contributors,
          message: `Contributor "${trimmedContributor}" added successfully`
        })
      };
    }

    // PUT - Replace entire contributor list
    if (event.httpMethod === 'PUT') {
      const { contributors } = JSON.parse(event.body);

      if (!Array.isArray(contributors)) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Contributors must be an array'
          })
        };
      }

      // Validate all contributors are non-empty strings
      for (const contributor of contributors) {
        if (!contributor || typeof contributor !== 'string' || !contributor.trim()) {
          return {
            statusCode: 400,
            headers,
            body: JSON.stringify({
              success: false,
              error: 'All contributors must be non-empty strings'
            })
          };
        }
      }

      // Check for duplicates
      const uniqueContributors = [...new Set(contributors.map(c => c.trim()))];
      if (uniqueContributors.length !== contributors.length) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Duplicate contributors found'
          })
        };
      }

      // Update
      contributorsData.contributors = uniqueContributors;
      contributorsData.last_updated = new Date().toISOString();

      // Save to Dropbox
      await saveContributorsToDropbox(accessToken, contributorsData);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          contributors: contributorsData.contributors,
          message: 'Contributors updated successfully'
        })
      };
    }

    // DELETE - Remove contributor (only if no recipes associated)
    if (event.httpMethod === 'DELETE') {
      const { contributor } = JSON.parse(event.body);

      if (!contributor || typeof contributor !== 'string') {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Contributor name is required'
          })
        };
      }

      // Check if contributor exists
      const index = contributorsData.contributors.findIndex(
        c => c.toLowerCase() === contributor.toLowerCase()
      );

      if (index === -1) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Contributor not found'
          })
        };
      }

      // Check if contributor has recipes
      const recipes = await loadRecipesFromDropbox(accessToken);

      const contributorRecipes = recipes.filter(
        r => r.contributor && r.contributor.toLowerCase() === contributor.toLowerCase()
      );

      if (contributorRecipes.length > 0) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: `Cannot remove contributor "${contributor}" because they have ${contributorRecipes.length} recipe(s). Please reassign their recipes first.`,
            recipe_count: contributorRecipes.length
          })
        };
      }

      // Remove from list
      contributorsData.contributors.splice(index, 1);
      contributorsData.last_updated = new Date().toISOString();

      // Save to Dropbox
      await saveContributorsToDropbox(accessToken, contributorsData);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          contributors: contributorsData.contributors,
          message: `Contributor "${contributor}" removed successfully`
        })
      };
    }

    // Unsupported method
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Method not allowed'
      })
    };

  } catch (error) {
    console.error('Error in manage-contributors:', error);
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
