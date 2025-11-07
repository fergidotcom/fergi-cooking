# Recipe Database Regeneration - Batch Processing Guide

This guide explains how to regenerate the recipe database from 131 source files on GitHub.

## Overview

The batch processing system will:
- Download 131 recipe files from GitHub (46 Fergi recipes, 85 Janet recipes)
- Extract text from PDFs and images (with OCR)
- Parse recipes using AI (Claude API)
- Format instructions with embedded ingredient quantities
- Generate SQLite database and JSON export
- Create processing logs and reports

## Files Created

The batch processing system consists of:

- **`netlify/functions/lib/recipe-parser.js`** - Reusable recipe parsing library
- **`regenerate-database.js`** - Main batch processing script
- **`test-extraction.js`** - Test script to validate pipeline

## Prerequisites

### 1. Environment Setup

Make sure you have Node.js installed and all dependencies:

```bash
npm install
```

### 2. API Key

You need a Claude API key from Anthropic:

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

To make this permanent, add to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export ANTHROPIC_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

### 3. Verify Dependencies

Check that all required packages are installed:

```bash
npm list better-sqlite3 pdf-parse tesseract.js @anthropic-ai/sdk node-fetch
```

If any are missing:

```bash
npm install better-sqlite3 --save-dev
```

## Testing the Pipeline

**IMPORTANT**: Always run the test script first to validate everything works!

```bash
node test-extraction.js
```

This will:
- Test extraction from 3 sample files (2 PDFs, 1 image)
- Validate OCR, PDF parsing, and AI recipe parsing
- Show sample output for each recipe
- Create `test-recipes.json` with results

Expected output:
```
🧪 RECIPE EXTRACTION PIPELINE TEST
==========================================================

Testing: Bananas Foster Recipe | Epicurious.pdf
==========================================================
📥 Downloading: https://raw.githubusercontent.com/...
✅ Downloaded (52341 bytes)
📄 Extracting text from PDF: Bananas Foster Recipe | Epicurious.pdf
   Extracted 1234 characters
✅ Extracted text (1234 characters)

📝 Sample text: "Bananas Foster Recipe..."

🤖 Parsing with AI...

✅ Successfully parsed recipe!
   Title: Bananas Foster
   Description: Classic New Orleans dessert with caramelized bananas...
   Ingredients: 8 items
   Instructions: 5 steps
   Prep time: 10 mins
   Cook time: 15 mins
   ...
```

If all tests pass, you're ready for full batch processing!

## Running the Full Batch Processing

### Basic Usage

```bash
node regenerate-database.js
```

This will process all 131 recipes. Expected runtime:
- **Fergi PDFs (40 files)**: ~30-45 minutes
- **Janet images (85 files)**: ~2-3 hours (OCR is slow)
- **Total**: ~2.5-4 hours

### Processing Details

The script processes recipes in batches:
- **Batch size**: 10 recipes at a time
- **Delay between batches**: 2 seconds
- **Delay between files**: 500ms

This prevents rate limiting and makes the process more stable.

### Progress Monitoring

The script provides real-time progress:

```
🟦 FERGI RECIPES - PDFs (40 files)

==========================================================
📦 BATCH 1/4 - 10 files
==========================================================

📥 Downloading: Bananas Foster Recipe | Epicurious.pdf
📄 Extracting text from PDF...
🤖 Parsing recipe with AI...
✅ Successfully processed: Bananas Foster

...

✅ Batch 1 complete: 10/10 successful

⏸️  Pausing 2000ms before next batch...
```

### Output Files

After completion, the following files are generated:

1. **`recipes.db`** - SQLite database with all 131 recipes
   - Ready to use locally
   - Contains full schema with ingredients, instructions, tags

2. **`recipes.json`** - JSON export for Netlify deployment
   - Can be uploaded to Dropbox manually
   - Or deploy with `netlify deploy --prod`

3. **`extraction_log.json`** - Detailed processing log
   - Success/error status for each file
   - Extracted text length
   - Confidence scores
   - Processing timestamps

4. **`recipes_needing_review.json`** - Flagged recipes (if any)
   - Recipes with low confidence scores
   - Missing embedded quantities in instructions
   - Requires manual review

5. **`extraction_summary.md`** - Human-readable report
   - Statistics (success rate, errors, etc.)
   - Breakdown by contributor
   - Recipes needing review
   - Next steps

### Example Summary Report

```markdown
# Recipe Database Regeneration Summary

**Generated:** 2025-11-07T12:00:00Z

## Statistics

- **Total Recipes Processed:** 131
- **Successful:** 125
- **Errors:** 6
- **Needs Review:** 12

## Breakdown by Contributor

- **Fergi Recipes:** 40
- **Janet Recipes:** 85

## Recipes Needing Review (12)

- **Joe's Meatloaf** (Joes Meatloaf.pdf): Instructions may be missing embedded quantities.
- **Scrambled Eggs Masala** (IMG_8145.JPG): Low OCR confidence (0.72)
...
```

## Handling Errors

### Common Issues

**1. API Key Not Set**
```
❌ Error: ANTHROPIC_API_KEY environment variable not set
```

**Solution:**
```bash
export ANTHROPIC_API_KEY=your-key-here
```

**2. Network Timeout**
```
❌ Error processing IMG_8123.JPG: Failed to download: timeout
```

**Solution:** Re-run the script. It will skip already-processed recipes (if database exists).

**3. OCR Failed**
```
❌ OCR failed for IMG_8145.JPG: Could not recognize text
```

**Solution:** The image may be blurry or unreadable. Manually review this recipe later.

**4. AI Parsing Error**
```
❌ Could not parse recipe JSON from AI response
```

**Solution:** Check the extraction_log.json for details. May need to adjust AI prompt.

### Resuming After Errors

If the script crashes partway through:

1. **Check what was completed:**
   ```bash
   sqlite3 recipes.db "SELECT COUNT(*) FROM recipes;"
   ```

2. **Review the log:**
   ```bash
   cat extraction_log.json | jq '.errors'
   ```

3. **Re-run the script:**
   - The script will start fresh (it doesn't resume)
   - Consider manually processing failed files or skipping them

### Skipping Problem Files

To skip specific files, edit `regenerate-database.js` and remove them from the arrays:

```javascript
const FERGI_PDFS = [
  // 'Problem-file.pdf',  // Skip this one
  'Bananas Foster Recipe | Epicurious.pdf',
  ...
];
```

## Quality Assurance

### Validation Checklist

After batch processing completes, verify:

- [ ] All 131 recipes processed (or acceptable number)
- [ ] No recipes titled "IMG_8XXX.JPG" (Janet recipes should have real titles)
- [ ] Instructions have embedded quantities (check sample recipes)
- [ ] Database schema is correct
- [ ] recipes.json is valid JSON
- [ ] No duplicate recipes

### Manual Review Process

1. **Check recipes flagged for review:**
   ```bash
   cat recipes_needing_review.json | jq '.[] | {title, reason}'
   ```

2. **Inspect specific recipes in database:**
   ```bash
   sqlite3 recipes.db
   > SELECT title, needs_review FROM recipes WHERE needs_review = 1;
   > SELECT * FROM recipes WHERE id = 42;
   ```

3. **Review instructions for embedded quantities:**
   ```bash
   sqlite3 recipes.db
   > SELECT instruction FROM instructions WHERE recipe_id = 42;
   ```

4. **Fix recipes if needed:**
   - Use `update-recipe.js` Netlify function
   - Or edit `recipes.json` directly and re-upload

### Sample Validation Queries

```sql
-- Count recipes by contributor
SELECT contributor_id, COUNT(*) FROM recipes GROUP BY contributor_id;

-- Find recipes without descriptions
SELECT id, title FROM recipes WHERE description IS NULL OR description = '';

-- Find recipes with very short instructions
SELECT r.id, r.title, COUNT(i.id) as step_count
FROM recipes r
LEFT JOIN instructions i ON r.id = i.recipe_id
GROUP BY r.id
HAVING step_count < 3;

-- Find instructions without quantities
SELECT r.title, i.instruction
FROM recipes r
JOIN instructions i ON r.id = i.recipe_id
WHERE i.instruction NOT LIKE '%cup%'
  AND i.instruction NOT LIKE '%tbsp%'
  AND i.instruction NOT LIKE '%tsp%'
  AND i.instruction NOT LIKE '%oz%'
LIMIT 20;
```

## Deploying the Results

### Option 1: Deploy with Netlify

```bash
# Deploy entire site with new recipes
netlify deploy --prod --message="Regenerated recipe database (131 recipes)"
```

### Option 2: Upload to Dropbox Only

If you just want to update the recipe data without deploying:

```bash
# Use the Dropbox API or web interface
# Upload recipes.json to: /Apps/Reference Refinement/recipes.json
```

### Option 3: Test Locally First

```bash
# Start local dev server
netlify dev

# Open http://localhost:8888
# Verify all recipes display correctly
```

## Performance Optimization

### Faster Processing

To speed up batch processing:

**1. Increase batch size:**
```javascript
const BATCH_SIZE = 20; // Instead of 10
```

**2. Reduce delays:**
```javascript
const DELAY_BETWEEN_BATCHES = 1000; // Instead of 2000
```

**3. Skip Pages files (require manual conversion):**
```javascript
// Comment out Pages files in FERGI_PAGES array
const FERGI_PAGES = [];
```

**4. Parallel processing (advanced):**
- Modify script to process multiple files concurrently
- Be careful with rate limits!

### Cost Optimization

Claude API costs:
- **Model**: claude-sonnet-4-20250514
- **Average tokens per recipe**: ~2000-3000
- **Cost**: ~$0.003 per recipe
- **Total for 131 recipes**: ~$0.40-0.50

To reduce costs:
- Use a cheaper model (e.g., claude-haiku)
- Reduce max_tokens in recipe-parser.js
- Cache results and avoid re-processing

## Troubleshooting

### Issue: Script hangs on OCR

**Symptom:** Script stuck at "Performing OCR..." for >5 minutes

**Solution:**
- OCR can be very slow for large/complex images
- Check system resources (CPU, memory)
- Consider manually converting problem images to text
- Skip the image and process manually later

### Issue: "Cannot find module 'better-sqlite3'"

**Solution:**
```bash
npm install better-sqlite3 --save-dev
npm rebuild better-sqlite3
```

### Issue: Recipes have poor quality

**Solution:**
- Check the AI prompt in `recipe-parser.js`
- Adjust temperature (lower = more consistent)
- Increase max_tokens if responses are cut off
- Review extraction_log.json for low confidence scores

### Issue: Database is too large

**Solution:**
- SQLite handles large databases well (100k+ recipes)
- If needed, optimize with indexes:
  ```sql
  CREATE INDEX idx_recipes_title ON recipes(title);
  CREATE INDEX idx_recipes_contributor ON recipes(contributor_id);
  ```

## Advanced Usage

### Custom AI Prompts

Edit `netlify/functions/lib/recipe-parser.js` to customize the AI prompt:

```javascript
const prompt = `You are formatting a recipe...
[Your custom instructions here]
`;
```

### Database Schema Modifications

To add new fields to the database:

1. Edit `initializeDatabase()` in `regenerate-database.js`
2. Add new columns to CREATE TABLE statements
3. Update `insertRecipe()` to include new fields
4. Re-run batch processing

### Exporting to Other Formats

After generating recipes.db, export to other formats:

```bash
# Export to CSV
sqlite3 recipes.db -header -csv "SELECT * FROM recipes;" > recipes.csv

# Export specific recipes
sqlite3 recipes.db -json "SELECT * FROM recipes WHERE cuisine = 'Italian';" > italian-recipes.json
```

## Next Steps

After successful batch processing:

1. ✅ Review `extraction_summary.md`
2. ✅ Check `recipes_needing_review.json`
3. ✅ Test locally with `netlify dev`
4. ✅ Deploy to production
5. ✅ Update CLAUDE.md with new statistics
6. ✅ Commit changes to git

---

**Questions or issues?** Check extraction_log.json for detailed error messages.

**Need help?** Review the code in regenerate-database.js and recipe-parser.js.
