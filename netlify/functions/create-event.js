// Fergi Cooking v2.0 - Create/Update Event Function (Dropbox storage)

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Content-Type': 'application/json'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    // Only parse body for POST and PUT requests
    let data = null;
    if (event.httpMethod === 'POST' || event.httpMethod === 'PUT') {
      data = JSON.parse(event.body);
    }

    // Load existing events from Dropbox
    let events = [];
    try {
      const response = await fetch('https://content.dropboxapi.com/2/files/download', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Dropbox-API-Arg': JSON.stringify({ path: '/Apps/Reference Refinement/events.json' })
        }
      });

      if (response.ok) {
        const eventsJson = await response.text();
        events = JSON.parse(eventsJson);
      }
    } catch (err) {
      console.log('No existing events file, starting fresh');
    }

    if (event.httpMethod === 'POST') {
      // Create new event
      const { name, event_date, event_time, location, description, collect_volunteers, guest_list } = data;

      const newEvent = {
        id: Date.now(), // Simple ID generation
        name,
        event_date,
        event_time,
        location,
        description,
        collect_volunteers: collect_volunteers || false,
        guest_list: guest_list || [],
        recipes: [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      };

      events.push(newEvent);

      // Save back to Dropbox
      const saveResponse = await fetch('https://content.dropboxapi.com/2/files/upload', {
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

      if (!saveResponse.ok) {
        const errorText = await saveResponse.text();
        console.error('Dropbox save error (create):', errorText);
        throw new Error(`Failed to save events: ${errorText}`);
      }

      return {
        statusCode: 201,
        headers,
        body: JSON.stringify({
          success: true,
          eventId: newEvent.id,
          message: 'Event created successfully'
        })
      };

    } else if (event.httpMethod === 'PUT') {
      // Update existing event
      const { id, name, event_date, event_time, location, description, collect_volunteers, guest_list } = data;

      const eventIndex = events.findIndex(e => e.id == id);
      if (eventIndex === -1) {
        return {
          statusCode: 404,
          headers,
          body: JSON.stringify({ error: 'Event not found' })
        };
      }

      events[eventIndex] = {
        ...events[eventIndex],
        name,
        event_date,
        event_time,
        location,
        description,
        collect_volunteers: collect_volunteers !== undefined ? collect_volunteers : events[eventIndex].collect_volunteers,
        guest_list: guest_list !== undefined ? guest_list : (events[eventIndex].guest_list || []),
        updated_at: new Date().toISOString()
      };

      // Save back to Dropbox
      const saveResponse = await fetch('https://content.dropboxapi.com/2/files/upload', {
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

      if (!saveResponse.ok) {
        const errorText = await saveResponse.text();
        console.error('Dropbox save error (update):', errorText);
        throw new Error(`Failed to save events: ${errorText}`);
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Event updated successfully'
        })
      };

    } else if (event.httpMethod === 'DELETE') {
      // Delete event
      const eventId = event.queryStringParameters?.id;

      events = events.filter(e => e.id != eventId);

      // Save back to Dropbox
      const saveResponse = await fetch('https://content.dropboxapi.com/2/files/upload', {
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

      if (!saveResponse.ok) {
        const errorText = await saveResponse.text();
        console.error('Dropbox save error (delete):', errorText);
        throw new Error(`Failed to save events: ${errorText}`);
      }

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          message: 'Event deleted successfully'
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
