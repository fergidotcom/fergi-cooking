/**
 * Send Verification Code
 * POST: Send 6-digit verification code to email
 * Uses Resend.com for email delivery
 */

const fetch = require('node-fetch');
const { getValidAccessToken } = require('./lib/dropbox-auth');

// Generate 6-digit random code
function generateCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

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

// Send email via Resend.com
async function sendEmail(email, code) {
  const resendApiKey = process.env.RESEND_API_KEY;

  if (!resendApiKey) {
    throw new Error('RESEND_API_KEY not configured');
  }

  const emailData = {
    from: 'Fergi Cooking <noreply@fergi.com>',
    to: [email],
    subject: 'Your Fergi Cooking verification code',
    html: `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; }
          .container { max-width: 600px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
          .content { background: #f8f9fa; padding: 30px; border-radius: 0 0 10px 10px; }
          .code { font-size: 36px; font-weight: bold; color: #e74c3c; text-align: center; letter-spacing: 8px; margin: 30px 0; padding: 20px; background: white; border-radius: 10px; border: 3px solid #e74c3c; }
          .footer { text-align: center; margin-top: 20px; color: #999; font-size: 14px; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1 style="margin: 0;">👨‍🍳 Fergi Cooking</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.9;">Your Recipe Collection</p>
          </div>
          <div class="content">
            <h2>Welcome!</h2>
            <p>Your verification code is:</p>
            <div class="code">${code}</div>
            <p>This code expires in <strong>10 minutes</strong>.</p>
            <p>If you didn't request this code, you can safely ignore this email.</p>
          </div>
          <div class="footer">
            <p>Happy Cooking! 🍳</p>
            <p>Fergi Cooking - Your Personal Recipe Collection</p>
          </div>
        </div>
      </body>
      </html>
    `
  };

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${resendApiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(emailData)
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Resend API error: ${error}`);
  }

  return await response.json();
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
    const { email } = JSON.parse(event.body);

    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ success: false, error: 'Invalid email address' })
      };
    }

    // Get Dropbox access token
    const accessToken = await getValidAccessToken();

    // Load existing codes
    const codesData = await loadCodesFromDropbox(accessToken);

    // Remove any expired codes
    const now = new Date();
    codesData.codes = codesData.codes.filter(c => new Date(c.expires_at) > now);

    // Generate new code
    const code = generateCode();
    const expiresAt = new Date(now.getTime() + 10 * 60 * 1000); // 10 minutes

    // Add new code
    codesData.codes.push({
      email: email.toLowerCase(),
      code: code,
      created_at: now.toISOString(),
      expires_at: expiresAt.toISOString(),
      verified: false
    });

    // Save to Dropbox
    await saveCodesToDropbox(accessToken, codesData);

    // Send email
    await sendEmail(email, code);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Verification code sent',
        email: email.toLowerCase()
      })
    };

  } catch (error) {
    console.error('Error sending verification code:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message || 'Failed to send verification code'
      })
    };
  }
};
