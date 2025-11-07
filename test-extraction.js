#!/usr/bin/env node

/**
 * Test Recipe Extraction Pipeline
 * Tests the extraction pipeline with a few sample files
 * Run this before the full batch processing to validate everything works
 */

const fs = require('fs');
const fetch = require('node-fetch');
const Database = require('better-sqlite3');
const pdfParse = require('pdf-parse');
const Tesseract = require('tesseract.js');
const { parseRecipe, estimateMissingData, normalizeRecipe } = require('./netlify/functions/lib/recipe-parser');

const GITHUB_BASE_URL = 'https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main';

// Test with just a few files
const TEST_FILES = [
  { folder: 'Fergi Recipes', filename: 'Bananas Foster Recipe | Epicurious.pdf', contributor: 'Fergi', type: 'pdf' },
  { folder: 'Fergi Recipes', filename: 'Joes Meatloaf.pdf', contributor: 'Fergi', type: 'pdf' },
  { folder: 'Janet Recipes', filename: 'IMG_8111.JPG', contributor: 'Janet', type: 'image' }
];

async function downloadFile(folder, filename) {
  const url = `${GITHUB_BASE_URL}/${encodeURIComponent(folder)}/${encodeURIComponent(filename)}`;
  console.log(`📥 Downloading: ${url}`);

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed to download ${filename}: ${response.statusText}`);
  }

  return await response.buffer();
}

async function extractPdfText(buffer, filename) {
  console.log(`📄 Extracting text from PDF: ${filename}`);
  const pdfData = await pdfParse(buffer);
  console.log(`   Extracted ${pdfData.text.length} characters`);
  return pdfData.text;
}

async function extractImageText(buffer, filename) {
  console.log(`🖼️  Performing OCR on image: ${filename}`);
  console.log(`   This may take 30-60 seconds...`);

  const result = await Tesseract.recognize(
    buffer,
    'eng',
    {
      logger: m => {
        if (m.status === 'recognizing text') {
          process.stdout.write(`\r   OCR Progress: ${Math.round(m.progress * 100)}%`);
        }
      }
    }
  );

  console.log(`\n   Extracted ${result.data.text.length} characters`);
  return result.data.text;
}

async function testFile(fileInfo) {
  console.log('\n' + '='.repeat(60));
  console.log(`Testing: ${fileInfo.filename}`);
  console.log('='.repeat(60));

  try {
    // Download
    const buffer = await downloadFile(fileInfo.folder, fileInfo.filename);
    console.log(`✅ Downloaded (${buffer.length} bytes)`);

    // Extract text
    let text;
    if (fileInfo.type === 'pdf') {
      text = await extractPdfText(buffer, fileInfo.filename);
    } else if (fileInfo.type === 'image') {
      text = await extractImageText(buffer, fileInfo.filename);
    }

    console.log(`✅ Extracted text (${text.length} characters)`);

    // Show a sample of extracted text
    const sample = text.slice(0, 200).replace(/\n/g, ' ');
    console.log(`\n📝 Sample text: "${sample}..."`);

    // Parse with AI
    console.log(`\n🤖 Parsing with AI...`);
    const recipe = await parseRecipe(text, {
      contributor: fileInfo.contributor,
      original_filename: fileInfo.filename,
      source_type: 'test_extraction'
    });

    estimateMissingData(recipe);
    normalizeRecipe(recipe);

    console.log(`\n✅ Successfully parsed recipe!`);
    console.log(`   Title: ${recipe.title}`);
    console.log(`   Description: ${recipe.description?.slice(0, 100)}...`);
    console.log(`   Ingredients: ${recipe.ingredients?.length} items`);
    console.log(`   Instructions: ${recipe.instructions?.length} steps`);
    console.log(`   Prep time: ${recipe.prep_time} mins`);
    console.log(`   Cook time: ${recipe.cook_time} mins`);
    console.log(`   Servings: ${recipe.servings}`);
    console.log(`   Calories: ${recipe.calories_per_serving}/serving`);
    console.log(`   Cuisine: ${recipe.cuisine}`);
    console.log(`   Difficulty: ${recipe.difficulty}`);
    console.log(`   Needs review: ${recipe.needs_review || false}`);

    // Check for embedded quantities in instructions
    const hasQuantities = recipe.instructions.some(step =>
      /\d+\s*(cup|tbsp|tsp|oz|lb|g|kg|ml|l|piece|slice|clove|bunch)/i.test(step)
    );

    if (hasQuantities) {
      console.log(`   ✅ Instructions have embedded quantities`);
    } else {
      console.log(`   ⚠️  Instructions may be missing embedded quantities`);
    }

    // Show first instruction as example
    if (recipe.instructions?.length > 0) {
      console.log(`\n   Example instruction:`);
      console.log(`   "${recipe.instructions[0]}"`);
    }

    return { success: true, recipe };

  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    console.error(error.stack);
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('\n' + '='.repeat(60));
  console.log('🧪 RECIPE EXTRACTION PIPELINE TEST');
  console.log('='.repeat(60));
  console.log();

  // Check for API key
  if (!process.env.ANTHROPIC_API_KEY) {
    console.error('❌ Error: ANTHROPIC_API_KEY environment variable not set');
    console.error('   Please set your Claude API key:');
    console.error('   export ANTHROPIC_API_KEY=your-key-here');
    process.exit(1);
  }

  console.log(`Testing ${TEST_FILES.length} sample files...\n`);

  const results = [];

  for (const fileInfo of TEST_FILES) {
    const result = await testFile(fileInfo);
    results.push({ ...fileInfo, ...result });

    // Delay between files to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  // Summary
  console.log('\n' + '='.repeat(60));
  console.log('📊 TEST SUMMARY');
  console.log('='.repeat(60));
  console.log();

  const successful = results.filter(r => r.success);
  const failed = results.filter(r => !r.success);

  console.log(`✅ Successful: ${successful.length}/${TEST_FILES.length}`);
  console.log(`❌ Failed: ${failed.length}/${TEST_FILES.length}`);

  if (successful.length > 0) {
    console.log(`\nSuccessfully processed recipes:`);
    successful.forEach(r => {
      console.log(`  - ${r.recipe.title} (${r.filename})`);
    });
  }

  if (failed.length > 0) {
    console.log(`\n❌ Failed to process:`);
    failed.forEach(r => {
      console.log(`  - ${r.filename}: ${r.error}`);
    });
  }

  // Save test recipes to JSON for inspection
  if (successful.length > 0) {
    const testRecipes = successful.map(r => r.recipe);
    fs.writeFileSync('test-recipes.json', JSON.stringify(testRecipes, null, 2));
    console.log(`\n💾 Saved ${testRecipes.length} test recipes to test-recipes.json`);
  }

  console.log('\n' + '='.repeat(60));
  if (successful.length === TEST_FILES.length) {
    console.log('✅ ALL TESTS PASSED!');
    console.log('   Ready to run full batch processing with:');
    console.log('   node regenerate-database.js');
  } else {
    console.log('⚠️  SOME TESTS FAILED');
    console.log('   Please fix errors before running full batch');
  }
  console.log('='.repeat(60));
  console.log();
}

if (require.main === module) {
  main().catch(error => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { main };
