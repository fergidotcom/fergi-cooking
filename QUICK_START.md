# Quick Start Guide - Recipe Database Regeneration

Follow these steps to regenerate the recipe database from 131 source files on GitHub.

## Prerequisites

1. **Node.js and npm installed**
2. **Claude API key from Anthropic**
3. **All dependencies installed:**
   ```bash
   npm install
   ```

## Step 1: Set API Key

```bash
export ANTHROPIC_API_KEY=your-api-key-here
```

**Make it permanent (optional):**
```bash
echo 'export ANTHROPIC_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

## Step 2: Test the Pipeline

**IMPORTANT:** Always test first!

```bash
node test-extraction.js
```

**What it does:**
- Tests with 3 sample files (2 PDFs, 1 image)
- Validates extraction, OCR, and AI parsing
- Takes ~3-5 minutes

**Expected output:**
```
🧪 RECIPE EXTRACTION PIPELINE TEST
✅ Successfully parsed recipe!
✅ ALL TESTS PASSED!
   Ready to run full batch processing
```

**If tests fail:**
- Check API key is set correctly
- Check internet connection
- Review error messages in output

## Step 3: Run Full Batch Processing

```bash
node regenerate-database.js
```

**What it does:**
- Processes all 131 recipes from GitHub
- Downloads PDFs and images
- Extracts text (including OCR for 85 images)
- Parses with AI
- Creates database and JSON files

**Runtime:** ~2.5-4 hours (OCR is slow)

**You can:**
- Let it run in the background
- Monitor progress in real-time
- Stop and restart if needed (will start fresh)

## Step 4: Review Results

```bash
# View summary
cat extraction_summary.md

# Check for recipes needing review
cat recipes_needing_review.json

# Count recipes in database
sqlite3 recipes.db "SELECT COUNT(*) FROM recipes;"
```

## Step 5: Deploy

```bash
netlify deploy --prod --message="Regenerated recipe database (131 recipes)"
```

**Or upload to Dropbox:**
- Upload `recipes.json` to `/Apps/Reference Refinement/recipes.json`
- Changes are immediately visible on live site

## Generated Files

After running, you'll have:

- ✅ `recipes.db` - SQLite database
- ✅ `recipes.json` - JSON for deployment
- ✅ `extraction_log.json` - Processing log
- ✅ `recipes_needing_review.json` - Flagged recipes (if any)
- ✅ `extraction_summary.md` - Summary report
- ✅ `test-recipes.json` - Test results

## Troubleshooting

### Problem: "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY=your-key-here
```

### Problem: "Cannot find module"
```bash
npm install
```

### Problem: Script hangs on OCR
- OCR takes 30-60 seconds per image
- Be patient, it will complete
- 85 images = ~1-2 hours total for Janet recipes

### Problem: Network errors
- Re-run the script
- Will download files again but should work

## Need More Help?

See detailed documentation:
- **README_REGENERATION.md** - System overview
- **BATCH_PROCESSING_GUIDE.md** - Complete guide
- **ADD_RECIPE_INTEGRATION.md** - Enhanced Add Recipe feature

## Quick Commands

```bash
# Test
node test-extraction.js

# Process all recipes
node regenerate-database.js

# Check database
sqlite3 recipes.db "SELECT COUNT(*) FROM recipes;"

# Deploy
netlify deploy --prod
```

---

**Ready?** Start with `node test-extraction.js`! 🚀
