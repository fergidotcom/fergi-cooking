/**
 * Extract text from uploaded files
 * Supports: PDF, Word (DOCX), Images (JPG/PNG via OCR), Plain Text
 */

const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');
const Tesseract = require('tesseract.js');
const multipart = require('lambda-multipart-parser');

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle OPTIONS for CORS
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Method not allowed'
      })
    };
  }

  try {
    // Parse multipart form data
    const result = await multipart.parse(event);

    if (!result.files || result.files.length === 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'No file uploaded'
        })
      };
    }

    const file = result.files[0];
    const filename = file.filename;
    const contentType = file.contentType;
    const buffer = file.content;

    console.log(`Processing file: ${filename}, type: ${contentType}, size: ${buffer.length} bytes`);

    let text = '';

    // PDF files
    if (contentType === 'application/pdf' || filename.toLowerCase().endsWith('.pdf')) {
      console.log('Extracting text from PDF...');
      const pdfData = await pdfParse(buffer);
      text = pdfData.text;
    }

    // Word documents (DOCX)
    else if (contentType === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
             filename.toLowerCase().endsWith('.docx')) {
      console.log('Extracting text from Word document...');
      const result = await mammoth.extractRawText({ buffer });
      text = result.value;
    }

    // Old Word documents (DOC) - not supported by mammoth
    else if (contentType === 'application/msword' ||
             filename.toLowerCase().endsWith('.doc')) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Old .doc format not supported. Please save as .docx or PDF.'
        })
      };
    }

    // Images (JPG/PNG) - Use OCR
    else if (contentType.startsWith('image/') ||
             filename.match(/\.(jpg|jpeg|png)$/i)) {
      console.log('Performing OCR on image... This may take 30-60 seconds');

      const result = await Tesseract.recognize(
        buffer,
        'eng',
        {
          logger: m => console.log(m)  // Log OCR progress
        }
      );

      text = result.data.text;
      console.log('OCR completed successfully');
    }

    // Plain text files
    else if (contentType === 'text/plain' || filename.toLowerCase().endsWith('.txt')) {
      console.log('Reading plain text file...');
      text = buffer.toString('utf8');
    }

    // Unsupported file type
    else {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: `Unsupported file type: ${contentType}. Supported formats: PDF, DOCX, JPG/PNG, TXT`
        })
      };
    }

    // Validate we got text
    if (!text || text.trim().length < 10) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Could not extract meaningful text from file. The file may be empty or corrupted.'
        })
      };
    }

    console.log(`Extracted ${text.length} characters from ${filename}`);

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        text: text.trim(),
        filename: filename,
        length: text.trim().length
      })
    };

  } catch (error) {
    console.error('Error extracting file:', error);
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
