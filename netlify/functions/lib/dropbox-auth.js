/**
 * Dropbox Token Management
 *
 * Handles automatic token refresh using OAuth refresh tokens.
 * All functions should use getValidAccessToken() instead of directly accessing env vars.
 */

const fetch = require('node-fetch');

// In-memory token cache (survives for duration of function execution)
let cachedAccessToken = null;
let tokenExpiresAt = null;

/**
 * Get a valid access token, refreshing if necessary
 * @returns {Promise<string>} Valid access token
 */
async function getValidAccessToken() {
  // If we have a cached token that's still valid, use it
  if (cachedAccessToken && tokenExpiresAt && Date.now() < tokenExpiresAt - 60000) {
    return cachedAccessToken;
  }

  // Check if we have refresh token (new method) or static token (old method)
  const refreshToken = process.env.DROPBOX_REFRESH_TOKEN;
  const staticToken = process.env.DROPBOX_ACCESS_TOKEN;

  if (refreshToken) {
    // New method: Use refresh token to get fresh access token
    return await refreshAccessToken();
  } else if (staticToken) {
    // Old method: Use static token (will expire eventually)
    console.warn('Using static DROPBOX_ACCESS_TOKEN - this will expire. Use refresh token instead.');
    return staticToken;
  } else {
    throw new Error('No Dropbox authentication configured. Set DROPBOX_REFRESH_TOKEN or DROPBOX_ACCESS_TOKEN');
  }
}

/**
 * Refresh the access token using the refresh token
 * @returns {Promise<string>} New access token
 */
async function refreshAccessToken() {
  const appKey = process.env.DROPBOX_APP_KEY;
  const appSecret = process.env.DROPBOX_APP_SECRET;
  const refreshToken = process.env.DROPBOX_REFRESH_TOKEN;

  if (!appKey || !appSecret || !refreshToken) {
    throw new Error('Missing Dropbox credentials: DROPBOX_APP_KEY, DROPBOX_APP_SECRET, or DROPBOX_REFRESH_TOKEN');
  }

  try {
    const tokenData = new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: appKey,
      client_secret: appSecret
    });

    const response = await fetch('https://api.dropboxapi.com/oauth2/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: tokenData.toString()
    });

    if (!response.ok) {
      const error = await response.text();
      console.error('Token refresh failed:', error);
      throw new Error(`Failed to refresh Dropbox token: ${error}`);
    }

    const tokens = await response.json();

    // Cache the new token
    cachedAccessToken = tokens.access_token;
    // Tokens expire in 4 hours (14400 seconds), cache for slightly less
    tokenExpiresAt = Date.now() + (tokens.expires_in || 14400) * 1000;

    console.log('✅ Refreshed Dropbox access token');
    return cachedAccessToken;

  } catch (error) {
    console.error('Error refreshing token:', error);
    throw error;
  }
}

/**
 * Handle Dropbox API errors, checking for expired tokens
 * @param {Response} response - Fetch response from Dropbox API
 * @returns {Promise<Object>} Parsed response or throws error
 */
async function handleDropboxResponse(response) {
  if (response.ok) {
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      return await response.json();
    }
    return await response.text();
  }

  // Check for expired token error
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

    // Clear cache and try to refresh
    cachedAccessToken = null;
    tokenExpiresAt = null;

    throw new Error('EXPIRED_TOKEN');
  }

  throw new Error(`Dropbox API error: ${errorText}`);
}

module.exports = {
  getValidAccessToken,
  handleDropboxResponse,
  refreshAccessToken
};
