# Recipe Database Regeneration System

Complete system for regenerating the Fergi Cooking recipe database from 131 source files using AI-powered extraction.

## 📋 Quick Start

```bash
# 1. Set up API key
export ANTHROPIC_API_KEY=your-key-here

# 2. Test the pipeline (IMPORTANT!)
node test-extraction.js

# 3. Run full batch processing
node regenerate-database.js

# 4. Deploy results
netlify deploy --prod
```

## 📁 What's Included

### Core System Files

| File | Purpose |
|------|---------|
| **`netlify/functions/lib/recipe-parser.js`** | ⭐ Reusable AI recipe parsing library |
| **`regenerate-database.js`** | Main batch processing script (131 recipes) |
| **`test-extraction.js`** | Test script (3 sample recipes) |
| **`netlify/functions/add-recipe-enhanced.js`** | Enhanced Add Recipe API endpoint |

### Documentation

| File | Content |
|------|---------|
| **`BATCH_PROCESSING_GUIDE.md`** | Complete guide for batch processing |
| **`ADD_RECIPE_INTEGRATION.md`** | Enhanced Add Recipe system documentation |
| **`README_REGENERATION.md`** | This file - system overview |

### Generated Files (After Running)

| File | Description |
|------|-------------|
| **`recipes.db`** | SQLite database with all recipes |
| **`recipes.json`** | JSON export for Netlify deployment |
| **`extraction_log.json`** | Detailed processing log |
| **`recipes_needing_review.json`** | Flagged recipes for manual review |
| **`extraction_summary.md`** | Human-readable summary report |
| **`test-recipes.json`** | Test results from test-extraction.js |

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Recipe Sources (GitHub)                  │
│  • 46 Fergi Recipes (40 PDFs, 6 Pages)                      │
│  • 85 Janet Recipes (JPG images)                             │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   Extraction Pipeline                        │
│  1. Download from GitHub                                     │
│  2. Extract text (PDF parser, OCR for images)               │
│  3. Parse with AI (recipe-parser.js)                        │
│  4. Validate and normalize                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation                         │
│  • recipes.db (SQLite)                                       │
│  • recipes.json (Netlify deployment)                         │
│  • Logs and reports                                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                      Deployment                              │
│  • Upload to Dropbox                                         │
│  • OR Deploy to Netlify                                      │
│  • Live at https://fergi-cooking.netlify.app                │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Key Features

### 1. AI-Powered Recipe Parsing

The `recipe-parser.js` library uses Claude API to:
- ✅ Extract recipe title from images (not filenames!)
- ✅ Structure ingredients with quantities
- ✅ Format instructions with **embedded quantities** (critical!)
- ✅ Estimate missing data (times, servings, calories)
- ✅ Classify cuisine, meal type, difficulty
- ✅ Generate searchable tags
- ✅ Flag low-confidence recipes for review

**Example:**

**Input (raw text):**
```
Bananas Foster
Ingredients: butter, sugar, bananas, rum
Instructions: Melt butter. Add sugar. Cook bananas. Add rum and flambe.
```

**Output (structured):**
```json
{
  "title": "Bananas Foster",
  "description": "Classic New Orleans dessert with caramelized bananas and rum sauce",
  "ingredients": [
    "4 tablespoons butter",
    "1/2 cup brown sugar",
    "4 ripe bananas, sliced lengthwise",
    "1/4 cup dark rum"
  ],
  "instructions": [
    "In a large skillet, melt 4 tablespoons butter over medium heat.",
    "Add 1/2 cup brown sugar and stir until dissolved.",
    "Add 4 sliced bananas and cook for 2-3 minutes until tender.",
    "Carefully add 1/4 cup dark rum and flambe. Serve immediately over ice cream."
  ],
  "prep_time": 5,
  "cook_time": 10,
  "servings": "4",
  "calories_per_serving": 280,
  "cuisine": "American",
  "meal_type": "dessert",
  "difficulty": "medium",
  "tags": ["dessert", "quick", "new-orleans", "classic"]
}
```

### 2. Batch Processing

Process all 131 recipes automatically:
- Downloads files from GitHub
- Handles multiple formats (PDF, images)
- Processes in batches to avoid rate limits
- Generates comprehensive logs and reports
- Creates production-ready database

**Runtime:** ~2.5-4 hours (OCR is slow)

### 3. Enhanced Add Recipe Feature

Users can upload files through the web interface:
- Same AI parsing as batch processing
- Preview and edit before saving
- Immediate visibility (no redeploy needed)
- Supports PDF, DOCX, images, text

**Already implemented** in current add-recipe.html!

### 4. Quality Assurance

Built-in validation ensures:
- All required fields present
- Instructions have embedded quantities
- No generic filenames as titles
- Consistent formatting across all recipes
- Recipes flagged for manual review when needed

## 🚀 Usage

### Test First (Important!)

Always test before running full batch processing:

```bash
node test-extraction.js
```

This tests with 3 sample files:
- `Bananas Foster Recipe | Epicurious.pdf` (Fergi)
- `Joes Meatloaf.pdf` (Fergi)
- `IMG_8111.JPG` (Janet)

**Expected output:**
```
🧪 RECIPE EXTRACTION PIPELINE TEST
==========================================================

✅ Successfully parsed recipe!
   Title: Bananas Foster
   Ingredients: 8 items
   Instructions: 5 steps
   ✅ Instructions have embedded quantities

📊 TEST SUMMARY
==========================================================
✅ Successful: 3/3
✅ ALL TESTS PASSED!
   Ready to run full batch processing
```

### Run Full Batch Processing

Once tests pass:

```bash
node regenerate-database.js
```

**Progress monitoring:**
```
🟦 FERGI RECIPES - PDFs (40 files)

📦 BATCH 1/4 - 10 files
📥 Downloading: Bananas Foster Recipe | Epicurious.pdf
📄 Extracting text from PDF...
🤖 Parsing recipe with AI...
✅ Successfully processed: Bananas Foster

✅ Batch 1 complete: 10/10 successful
⏸️  Pausing 2000ms before next batch...
```

**Generated files:**
```
recipes.db                      ← SQLite database
recipes.json                    ← JSON for deployment
extraction_log.json             ← Processing details
recipes_needing_review.json     ← Flagged recipes
extraction_summary.md           ← Summary report
```

### Review Results

Check the summary:

```bash
cat extraction_summary.md
```

Review flagged recipes:

```bash
cat recipes_needing_review.json | jq '.'
```

Inspect database:

```bash
npm install -g sql.js-cli  # If not already installed
sqlite3 recipes.db "SELECT title, cuisine, needs_review FROM recipes LIMIT 10;"
```

### Deploy

Deploy to production:

```bash
netlify deploy --prod --message="Regenerated recipe database (131 recipes)"
```

Or just upload recipes.json to Dropbox manually:
- Upload to: `/Apps/Reference Refinement/recipes.json`
- Changes are immediately visible on live site

## 📊 What Gets Extracted

For each of the 131 recipes:

### Required Fields ✅

| Field | Description | Example |
|-------|-------------|---------|
| **title** | Recipe name (NOT filename!) | "Beef Bourguignon" |
| **description** | 1-3 sentence summary | "Classic French beef stew..." |
| **ingredients** | List with quantities | ["2 lbs beef chuck", ...] |
| **instructions** | Steps with embedded quantities | ["Brown 2 lbs beef cubes..."] |
| **prep_time** | Integer minutes | 30 |
| **cook_time** | Integer minutes | 180 |
| **servings** | String or number | "6-8" |
| **calories_per_serving** | Integer estimate | 450 |
| **contributor_id** | 1=Fergi, 2=Janet | 1 |

### Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| **cuisine** | Type of cuisine | "French" |
| **meal_type** | When to eat it | "dinner" |
| **difficulty** | How hard to make | "medium" |
| **tags** | Searchable keywords | ["comfort-food", "french"] |
| **source_attribution** | Original source | "Epicurious" |
| **confidence_score** | AI confidence (0-1) | 0.95 |
| **needs_review** | Flagged for review | false |

## ⚠️ Critical Requirement: Embedded Quantities

**Most important feature:** Instructions MUST include ingredient quantities.

❌ **Bad (generic):**
```
1. Preheat oven.
2. Mix the flour and sugar.
3. Add the butter.
4. Bake until golden.
```

✅ **Good (specific):**
```
1. Preheat oven to 350°F (175°C).
2. In a large bowl, mix 2 cups all-purpose flour with 1 cup granulated sugar.
3. Add 1/2 cup softened butter and beat until creamy.
4. Spread in greased 9x13 pan and bake for 25-30 minutes until golden brown.
```

**Why:** The cook should never need to refer back to the ingredients list while cooking.

## 🔧 Troubleshooting

### Common Issues

| Problem | Solution |
|---------|----------|
| `ANTHROPIC_API_KEY not set` | Run `export ANTHROPIC_API_KEY=your-key` |
| Script hangs on OCR | OCR is slow (30-60s per image), be patient |
| "Cannot find module" | Run `npm install` |
| Low quality recipes | Adjust AI prompt in recipe-parser.js |
| Network timeout | Re-run script, add delays between batches |

### Getting Help

1. Check `extraction_log.json` for detailed errors
2. Review `BATCH_PROCESSING_GUIDE.md` for full troubleshooting
3. Inspect the code in `regenerate-database.js` and `recipe-parser.js`

## 📖 Detailed Documentation

For more information, see:

- **[BATCH_PROCESSING_GUIDE.md](./BATCH_PROCESSING_GUIDE.md)** - Complete batch processing guide
  - Prerequisites and setup
  - Running the batch process
  - Quality assurance
  - Deployment
  - Advanced usage

- **[ADD_RECIPE_INTEGRATION.md](./ADD_RECIPE_INTEGRATION.md)** - Enhanced Add Recipe system
  - Architecture overview
  - Current vs. enhanced workflow
  - Recipe parser library details
  - Testing and deployment
  - Troubleshooting

## 🎓 Technical Details

### Dependencies

```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.68.0",      // Claude API
    "pdf-parse": "^2.4.5",               // PDF text extraction
    "tesseract.js": "^6.0.1",            // OCR for images
    "mammoth": "^1.11.0",                // DOCX parsing
    "node-fetch": "^2.7.0",              // HTTP requests
    "lambda-multipart-parser": "^1.0.1"  // File uploads
  },
  "devDependencies": {
    "better-sqlite3": "^11.0.0"          // SQLite database
  }
}
```

### Database Schema

```sql
CREATE TABLE recipes (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  cuisine TEXT,
  meal_type TEXT,
  difficulty TEXT,
  prep_time INTEGER,
  cook_time INTEGER,
  servings TEXT,
  calories_per_serving INTEGER,
  contributor_id INTEGER,
  needs_review BOOLEAN,
  confidence_score REAL,
  date_added DATETIME,
  FOREIGN KEY (contributor_id) REFERENCES contributors(id)
);

CREATE TABLE ingredients (
  id INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL,
  ingredient TEXT NOT NULL,
  display_order INTEGER,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

CREATE TABLE instructions (
  id INTEGER PRIMARY KEY,
  recipe_id INTEGER NOT NULL,
  step_number INTEGER NOT NULL,
  instruction TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

CREATE TABLE recipe_tags (
  recipe_id INTEGER NOT NULL,
  tag TEXT NOT NULL,
  PRIMARY KEY (recipe_id, tag),
  FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
```

### API Costs

Claude API pricing (approximate):
- **Model:** claude-sonnet-4-20250514
- **Cost per recipe:** ~$0.003
- **Total for 131 recipes:** ~$0.40-0.50

For cheaper processing, use claude-haiku (~$0.0005 per recipe).

### Performance

- **PDF extraction:** 1-3 seconds
- **OCR (images):** 30-60 seconds per image
- **AI parsing:** 3-5 seconds
- **Total batch time:** 2.5-4 hours for all 131 recipes

## 📝 Example Workflow

### Complete end-to-end example:

```bash
# 1. Clone repo and install
git clone https://github.com/fergidotcom/fergi-cooking.git
cd fergi-cooking
npm install

# 2. Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Test extraction
node test-extraction.js
# ✅ ALL TESTS PASSED!

# 4. Run full batch processing
node regenerate-database.js
# Processing... (2-4 hours)
# ✅ DATABASE REGENERATION COMPLETE!

# 5. Review results
cat extraction_summary.md
# Total Recipes Processed: 131
# Successful: 125
# Needs Review: 6

# 6. Check database
sqlite3 recipes.db "SELECT COUNT(*) FROM recipes;"
# 125

# 7. Inspect flagged recipes
cat recipes_needing_review.json

# 8. Deploy to production
netlify deploy --prod

# 9. Visit site
open https://fergi-cooking.netlify.app

# 10. Test Add Recipe feature
open https://fergi-cooking.netlify.app/add-recipe.html
```

## 🎯 Success Criteria

The regeneration is successful when:

- ✅ All 131 recipes processed (or acceptable number with explanations for failures)
- ✅ All recipes have required fields
- ✅ No recipes titled "IMG_8XXX.JPG" (Janet recipes have real titles)
- ✅ Instructions have embedded ingredient quantities
- ✅ Database schema is correct
- ✅ recipes.json is valid
- ✅ No duplicate recipes
- ✅ All contributors correctly assigned (Fergi=1, Janet=2)
- ✅ Flagged recipes reviewed and fixed as needed

## 🚢 Deployment Checklist

Before deploying to production:

- [ ] Run test-extraction.js and verify all tests pass
- [ ] Run regenerate-database.js and verify completion
- [ ] Review extraction_summary.md
- [ ] Check recipes_needing_review.json and fix flagged recipes
- [ ] Validate database: `sqlite3 recipes.db .schema`
- [ ] Validate JSON: `cat recipes.json | jq '.' > /dev/null`
- [ ] Test locally: `netlify dev`
- [ ] Commit changes to git
- [ ] Deploy: `netlify deploy --prod`
- [ ] Verify on live site
- [ ] Update CLAUDE.md with new statistics

## 📞 Support

**Issues or questions?**

1. Check the detailed guides:
   - BATCH_PROCESSING_GUIDE.md
   - ADD_RECIPE_INTEGRATION.md

2. Review the code:
   - `regenerate-database.js` - Batch processing
   - `netlify/functions/lib/recipe-parser.js` - AI parsing
   - `test-extraction.js` - Testing

3. Check logs:
   - `extraction_log.json` - Processing details
   - `extraction_summary.md` - Summary report

## 🏁 Quick Command Reference

```bash
# Test pipeline
node test-extraction.js

# Full batch processing
node regenerate-database.js

# Inspect database
sqlite3 recipes.db
> SELECT COUNT(*) FROM recipes;
> SELECT title, needs_review FROM recipes WHERE needs_review = 1;

# Deploy
netlify deploy --prod --message="Regenerated recipe database"

# Local testing
netlify dev
```

## 📜 License

Part of the Fergi Cooking project.
For personal use.

---

**Ready to begin?** Start with `node test-extraction.js`! 🚀
