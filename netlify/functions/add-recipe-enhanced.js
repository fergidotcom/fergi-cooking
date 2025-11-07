/**
 * Enhanced Add Recipe Function
 * Supports file uploads with AI-powered recipe extraction
 * Reuses the same parsing logic as batch processing
 */

const pdfParse = require('pdf-parse');
const mammoth = require('mammoth');
const Tesseract = require('tesseract.js');
const multipart = require('lambda-multipart-parser');
const { parseRecipe, estimateMissingData, normalizeRecipe } = require('./lib/recipe-parser');
const { getDropboxClient } = require('./lib/dropbox-auth');

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

    console.log('Received add-recipe-enhanced request');
    console.log('Files:', result.files?.length || 0);
    console.log('Fields:', Object.keys(result).filter(k => k !== 'files'));

    // Two modes: file upload OR manual entry
    let recipe;
    let mode;

    // MODE 1: File Upload with AI Extraction
    if (result.files && result.files.length > 0) {
      mode = 'file_upload';
      const file = result.files[0];
      const filename = file.filename;
      const contentType = file.contentType;
      const buffer = file.content;

      console.log(`Processing uploaded file: ${filename}, type: ${contentType}, size: ${buffer.length} bytes`);

      // Extract text from file
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
        const mammothResult = await mammoth.extractRawText({ buffer });
        text = mammothResult.value;
      }

      // Images (JPG/PNG) - Use OCR
      else if (contentType.startsWith('image/') ||
               filename.match(/\.(jpg|jpeg|png)$/i)) {
        console.log('Performing OCR on image... This may take 30-60 seconds');

        const ocrResult = await Tesseract.recognize(
          buffer,
          'eng',
          {
            logger: m => console.log(m)
          }
        );

        text = ocrResult.data.text;
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

      // Validate extracted text
      if (!text || text.trim().length < 50) {
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

      // Parse with AI
      const contributor = result.contributor || 'Fergi';
      recipe = await parseRecipe(text, {
        contributor,
        original_filename: filename,
        source_type: 'file_upload'
      });

      // Estimate missing data
      estimateMissingData(recipe);

      // Normalize
      normalizeRecipe(recipe);

      console.log(`Successfully parsed recipe: ${recipe.title}`);

      // Return extracted recipe for user review/editing
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          mode: 'extracted',
          recipe,
          message: 'Recipe extracted successfully. Please review and edit before saving.'
        })
      };
    }

    // MODE 2: Manual Entry (recipe data provided directly)
    else if (result.recipe) {
      mode = 'manual_entry';
      recipe = typeof result.recipe === 'string' ? JSON.parse(result.recipe) : result.recipe;

      console.log(`Manual recipe entry: ${recipe.title}`);

      // Validate required fields
      if (!recipe.title || !recipe.ingredients || !recipe.instructions) {
        return {
          statusCode: 400,
          headers,
          body: JSON.stringify({
            success: false,
            error: 'Recipe must have title, ingredients, and instructions'
          })
        };
      }

      // Estimate missing data
      estimateMissingData(recipe);

      // Normalize
      normalizeRecipe(recipe);

      // Save to Dropbox
      const dbx = await getDropboxClient();

      // Download current recipes
      let recipes = [];
      try {
        const response = await dbx.filesDownload({ path: '/recipes.json' });
        recipes = JSON.parse(response.result.fileBinary.toString('utf8'));
        console.log(`Loaded ${recipes.length} existing recipes`);
      } catch (error) {
        if (error.status === 409) {
          console.log('recipes.json not found, creating new file');
          recipes = [];
        } else {
          throw error;
        }
      }

      // Add ID and metadata
      recipe.id = recipes.length > 0 ? Math.max(...recipes.map(r => r.id)) + 1 : 1;
      recipe.date_added = new Date().toISOString();
      recipe.contributor_id = recipe.contributor === 'Janet' ? 2 : 1;

      // Add to array
      recipes.push(recipe);

      // Upload back to Dropbox
      await dbx.filesUpload({
        path: '/recipes.json',
        contents: JSON.stringify(recipes, null, 2),
        mode: { '.tag': 'overwrite' }
      });

      console.log(`✅ Saved recipe #${recipe.id}: ${recipe.title}`);

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          mode: 'saved',
          recipe,
          message: `Recipe "${recipe.title}" saved successfully!`
        })
      };
    }

    // No file and no recipe data
    else {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Please provide either a file upload or recipe data'
        })
      };
    }

  } catch (error) {
    console.error('Error in add-recipe-enhanced:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: error.message,
        details: error.stack
      })
    };
  }
};
