// Fergi Cooking v2.0 - Generate Event Email Function (Dropbox storage)

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

exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'text/html'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  try {
    // Get a valid access token (auto-refreshes if needed)
    const accessToken = await getValidAccessToken();

    const eventId = event.queryStringParameters?.id;
    const guestEmail = event.queryStringParameters?.email || '{GUEST_EMAIL}';

    if (!eventId) {
      return {
        statusCode: 400,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Event ID required' })
      };
    }

    const events = await loadEventsFromDropbox(accessToken);
    const eventData = events.find(e => e.id == eventId);

    if (!eventData) {
      return {
        statusCode: 404,
        headers: { ...headers, 'Content-Type': 'application/json' },
        body: JSON.stringify({ error: 'Event not found' })
      };
    }

    const recipes = await loadRecipesFromDropbox(accessToken);
    const eventRecipes = (eventData.recipes || []).map(er => {
      const recipe = recipes.find(r => r.id == er.recipe_id);
      return recipe ? { ...recipe, ...er } : null;
    }).filter(r => r !== null);

    const html = generateEmailHTML(eventData, eventRecipes, guestEmail);

    return {
      statusCode: 200,
      headers,
      body: html
    };

  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: error.message })
    };
  }
};

function generateEmailHTML(event, recipes, guestEmail) {
  const formatDate = (dateStr) => {
    if (!dateStr) return '';
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
  };

  const baseUrl = 'https://fergi-cooking.netlify.app';

  let recipeCards = '';
  const courseOrder = { appetizer: 1, salad: 2, main: 3, side: 4, dessert: 5, beverage: 6, other: 7 };
  const groupedRecipes = {};

  // Group recipes by course
  recipes.forEach(recipe => {
    const course = recipe.course_type || 'other';
    if (!groupedRecipes[course]) groupedRecipes[course] = [];
    groupedRecipes[course].push(recipe);
  });

  // Sort courses
  const sortedCourses = Object.keys(groupedRecipes).sort((a, b) => {
    return (courseOrder[a] || 99) - (courseOrder[b] || 99);
  });

  sortedCourses.forEach(course => {
    const courseTitle = course.charAt(0).toUpperCase() + course.slice(1) + 's';
    recipeCards += `<h2 style="color: #2c3e50; margin-top: 30px; padding-bottom: 10px; border-bottom: 2px solid #4CAF50;">${courseTitle}</h2>`;

    groupedRecipes[course].forEach(recipe => {
      recipeCards += `
      <div style="border: 2px solid #e0e0e0; margin: 20px 0; padding: 20px; border-radius: 12px; background: #ffffff;">
        <h3 style="color: #2c3e50; margin-top: 0;">${recipe.title}</h3>
        <p style="color: #555; line-height: 1.6;">${recipe.description || ''}</p>

        <div style="margin: 15px 0;">
          <a href="${baseUrl}/respond.html?event=${event.id}&recipe=${recipe.id}&type=prefer&guest=${guestEmail}"
             style="display: inline-block; padding: 12px 24px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white; text-decoration: none; border-radius: 8px; font-weight: bold;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            ❤️ I prefer this
          </a>
        </div>
        ${recipe.has_variants ? `<p style="font-size: 0.85rem; color: #666; margin-top: 5px;">Note: This recipe has variants available</p>` : ''}
      </div>
      `;
    });
  });

  return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${event.name}</title>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; background: #f5f5f5;">
  <div style="max-width: 600px; margin: 0 auto; background: white;">
    <!-- Header -->
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 40px 20px; text-align: center;">
      <h1 style="margin: 0 0 10px 0; font-size: 32px;">🎉 You're Invited!</h1>
      <h2 style="margin: 0 0 20px 0; font-weight: 300; font-size: 28px;">${event.name}</h2>
      ${event.event_date ? `<p style="margin: 5px 0; font-size: 18px; opacity: 0.95;">📅 ${formatDate(event.event_date)}</p>` : ''}
      ${event.event_time ? `<p style="margin: 5px 0; font-size: 18px; opacity: 0.95;">🕐 ${event.event_time}</p>` : ''}
      ${event.location ? `<p style="margin: 5px 0; font-size: 18px; opacity: 0.95;">📍 ${event.location}</p>` : ''}
    </div>

    <!-- Content -->
    <div style="padding: 30px 20px;">
      ${event.description ? `<p style="color: #555; font-size: 16px; line-height: 1.6; margin-bottom: 30px;">${event.description}</p>` : ''}

      <p style="color: #2c3e50; font-size: 16px; line-height: 1.6;">
        We're planning the menu and would love your input! Please select your preferences below by clicking the buttons.
      </p>

      ${recipeCards}

      ${event.collect_volunteers ? `
      <!-- Volunteer to Bring Categories -->
      <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin-top: 0;">🤝 Volunteer to Bring a Category</h3>
        <p style="color: white; opacity: 0.95; margin-bottom: 20px;">Can you bring something from one of these categories? Click to volunteer!</p>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=appetizer&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🥗</span>
            <span style="font-size: 0.9rem;">Appetizer</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=salad&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🥬</span>
            <span style="font-size: 0.9rem;">Salad</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=main&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🍖</span>
            <span style="font-size: 0.9rem;">Main Course</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=side&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🥔</span>
            <span style="font-size: 0.9rem;">Side Dish</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=dessert&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🍰</span>
            <span style="font-size: 0.9rem;">Dessert</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=volunteer&category=beverage&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #38f9d7;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🍷</span>
            <span style="font-size: 0.9rem;">Beverage</span>
          </a>
        </div>
        <p style="color: white; font-size: 0.85rem; margin-top: 15px; opacity: 0.9;">You can volunteer for multiple categories!</p>
      </div>
      ` : ''}

      <!-- Dietary Restrictions -->
      <div style="margin-top: 40px; padding: 20px; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 12px; text-align: center;">
        <h3 style="color: white; margin-top: 0;">🥗 Dietary Restrictions?</h3>
        <p style="color: white; opacity: 0.95; margin-bottom: 20px;">Let us know if you have any dietary restrictions or allergies:</p>
        <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">
          <a href="${baseUrl}/respond.html?event=${event.id}&type=dietary&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #f5576c;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🌾</span>
            <span style="font-size: 0.9rem;">Gluten Free</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=dietary&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #f5576c;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🥛</span>
            <span style="font-size: 0.9rem;">Lactose Free</span>
          </a>
          <a href="${baseUrl}/respond.html?event=${event.id}&type=dietary&guest=${guestEmail}"
             style="display: inline-flex; flex-direction: column; align-items: center; padding: 20px 25px; background: white; color: #f5576c;
                    text-decoration: none; border-radius: 12px; font-weight: bold; min-width: 120px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <span style="font-size: 3rem; margin-bottom: 5px;">🥗</span>
            <span style="font-size: 0.9rem;">Other</span>
          </a>
        </div>
        <p style="color: white; font-size: 0.85rem; margin-top: 15px; opacity: 0.9;">Click any option to specify your dietary needs</p>
      </div>
    </div>

    <!-- Footer -->
    <div style="padding: 20px; text-align: center; background: #f8f9fa; color: #777; font-size: 14px;">
      <p style="margin: 5px 0;">Fergi Cooking System v2.9.0</p>
      <p style="margin: 5px 0;">You can change your selections at any time by clicking the links again.</p>
    </div>
  </div>
</body>
</html>
  `;
}
