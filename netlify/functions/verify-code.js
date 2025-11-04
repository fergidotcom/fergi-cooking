/**
 * Verify Code
 * POST: Verify 6-digit code and create session
 */

const fetch = require('node-fetch');
const crypto = require('crypto');
const { getValidAccessToken } = require('./lib/dropbox-auth');

// Load verification codes from Dropbox
async function loadCodesFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/verification-codes.json'
        })
      }
    });

    if (!response.ok) {
      return { codes: [] };
    }

    const data = await response.text();
    return JSON.parse(data);
  } catch (error) {
    console.log('Error loading codes:', error);
    return { codes: [] };
  }
}

// Save verification codes to Dropbox
async function saveCodesToDropbox(accessToken, codesData) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/verification-codes.json',
        mode: 'overwrite',
        autorename: false,
        mute: false
      })
    },
    body: JSON.stringify(codesData, null, 2)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Dropbox API error: ${errorText}`);
  }

  return await response.json();
}

// Load or create users.json
async function loadUsersFromDropbox(accessToken) {
  try {
    const response = await fetch('https://content.dropboxapi.com/2/files/download', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Dropbox-API-Arg': JSON.stringify({
          path: '/Apps/Reference Refinement/users.json'
        })
      }
    });

    if (!response.ok) {
      return { users: [] };
    }

    const data = await response.text();
    return JSON.parse(data);
  } catch (error) {
    console.log('Error loading users:', error);
    return { users: [] };
  }
}

// Save users to Dropbox
async function saveUsersToDropbox(accessToken, usersData) {
  const response = await fetch('https://content.dropboxapi.com/2/files/upload', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/octet-stream',
      'Dropbox-API-Arg': JSON.stringify({
        path: '/Apps/Reference Refinement/users.json',
        mode: 'overwrite',
        autorename: false,
        mute: false
      })
    },
    body: JSON.stringify(usersData, null, 2)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Dropbox API error: ${errorText}`);
  }

  return await response.json();
}

// Generate session token
function generateSessionToken() {
  return crypto.randomBytes(32).toString('hex');
}

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ success: false, error: 'Method not allowed' })
    };
  }

  try {
    const { email, code, name } = JSON.parse(event.body);

    if (!email || !code) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, error: 'Email and code are required' })
      };
    }

    const normalizedEmail = email.toLowerCase();

    // Get Dropbox access token
    const accessToken = await getValidAccessToken();

    // Load codes
    const codesData = await loadCodesFromDropbox(accessToken);

    // Find matching code
    const now = new Date();
    const matchingCode = codesData.codes.find(c =>
      c.email === normalizedEmail &&
      c.code === code &&
      !c.verified &&
      new Date(c.expires_at) > now
    );

    if (!matchingCode) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Invalid or expired verification code'
        })
      };
    }

    // Mark code as verified
    matchingCode.verified = true;
    await saveCodesToDropbox(accessToken, codesData);

    // Load or create user
    const usersData = await loadUsersFromDropbox(accessToken);
    let user = usersData.users.find(u => u.email === normalizedEmail);

    const sessionToken = generateSessionToken();

    if (!user) {
      // New user
      user = {
        email: normalizedEmail,
        name: name || normalizedEmail.split('@')[0],
        created_at: now.toISOString(),
        last_login: now.toISOString(),
        session_token: sessionToken
      };
      usersData.users.push(user);
    } else {
      // Existing user - update session
      user.last_login = now.toISOString();
      user.session_token = sessionToken;
      if (name) {
        user.name = name;
      }
    }

    // Save users
    await saveUsersToDropbox(accessToken, usersData);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        user: {
          email: user.email,
          name: user.name,
          session_token: user.session_token
        }
      })
    };

  } catch (error) {
    console.error('Error verifying code:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to verify code'
      })
    };
  }
};
