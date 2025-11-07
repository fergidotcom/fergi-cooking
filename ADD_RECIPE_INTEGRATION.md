# Enhanced Add Recipe System - Integration Guide

This document explains the enhanced Add Recipe feature that uses AI-powered extraction to automatically format recipes from uploaded files.

## Overview

The enhanced Add Recipe system allows users to:
- Upload recipe files (PDF, DOCX, images, text)
- Automatically extract and structure recipe data using AI
- Preview and edit extracted recipes before saving
- Maintain the same quality standards as batch processing

## Architecture

### System Components

```
User uploads file
       ↓
[extract-file.js] → Extract text from file (PDF, DOCX, OCR)
       ↓
[format-recipe.js] → Parse with AI using recipe-parser library
       ↓
Preview in UI → User reviews and edits
       ↓
[add-recipe.js] → Save to Dropbox recipes.json
       ↓
Live on website (no redeploy needed!)
```

### Key Files

1. **`netlify/functions/lib/recipe-parser.js`**
   - Reusable recipe parsing library
   - Used by BOTH batch processing AND Add Recipe feature
   - Ensures consistent formatting across all recipes

2. **`netlify/functions/extract-file.js`**
   - Extracts text from uploaded files
   - Supports: PDF, DOCX, JPG/PNG (OCR), TXT
   - Returns plain text for AI parsing

3. **`netlify/functions/format-recipe.js`**
   - Parses recipe text using Claude API
   - Uses recipe-parser library
   - Returns structured recipe JSON

4. **`netlify/functions/add-recipe.js`**
   - Saves recipe to Dropbox
   - Assigns recipe ID
   - Updates recipes.json

5. **`netlify/functions/add-recipe-enhanced.js`** (Optional)
   - All-in-one endpoint combining extraction + parsing
   - More efficient (single API call instead of two)
   - Can replace current multi-step workflow

6. **`add-recipe.html`**
   - User interface for recipe import
   - 4-step wizard process
   - File upload and preview

## Current Workflow (Already Implemented!)

The current system already has full AI-powered recipe extraction:

### Step 1: Upload or Paste Recipe

Users can:
- Upload a file (PDF, DOCX, JPG/PNG, TXT)
- Paste recipe text directly
- Enter recipe manually

```javascript
// File upload handled by extract-file.js
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('/extract-file', {
  method: 'POST',
  body: formData
});

const { text } = await response.json();
```

### Step 2: Select Contributor

Choose who contributed the recipe:
- Fergi (contributor_id: 1)
- Janet (contributor_id: 2)
- Or add new contributor

### Step 3: Format with AI

The extracted text is sent to Claude API for parsing:

```javascript
const response = await fetch('/format-recipe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: extractedText,
    contributor: 'Fergi',
    original_filename: 'recipe.pdf'
  })
});

const { recipe } = await response.json();
```

The AI formats the recipe to Ferguson family standards:
- Structured ingredients list
- **Instructions with embedded quantities** (critical!)
- Estimated prep/cook times if missing
- Cuisine and meal type classification
- Tags for searchability

### Step 4: Review and Edit

User can review and edit all fields:
- Title
- Description
- Ingredients (line-by-line)
- Instructions (step-by-step)
- Times, servings, calories
- Tags and metadata

### Step 5: Save

Final recipe is saved to Dropbox:

```javascript
const response = await fetch('/add-recipe', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ recipe })
});

// Recipe is immediately visible on website!
```

## Enhanced Workflow (Optional - add-recipe-enhanced.js)

The `add-recipe-enhanced.js` function combines extraction + parsing into a single call:

### Two Modes

**Mode 1: File Upload with AI Extraction**

```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('contributor', 'Fergi');

const response = await fetch('/add-recipe-enhanced', {
  method: 'POST',
  body: formData
});

const { recipe, mode } = await response.json();
// mode === 'extracted'
// recipe contains fully parsed data
// User reviews and edits, then saves
```

**Mode 2: Direct Save (Manual Entry)**

```javascript
const response = await fetch('/add-recipe-enhanced', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ recipe: manuallyEnteredRecipe })
});

const { recipe, mode } = await response.json();
// mode === 'saved'
// Recipe already saved to Dropbox
```

### Benefits of Enhanced Endpoint

✅ Fewer API calls (1 instead of 3)
✅ Simpler frontend code
✅ Same parsing logic as batch processing
✅ Built-in validation

### Migration to Enhanced Endpoint

To switch from current system to enhanced endpoint:

1. **Update add-recipe.html to call add-recipe-enhanced:**

```javascript
// Instead of:
// 1. Call /extract-file
// 2. Call /format-recipe
// 3. Call /add-recipe

// Do:
const formData = new FormData();
formData.append('file', file);
formData.append('contributor', contributor);

const response = await fetch('/.netlify/functions/add-recipe-enhanced', {
  method: 'POST',
  body: formData
});

const { recipe, mode } = await response.json();

if (mode === 'extracted') {
  // Show preview, let user edit
  showPreview(recipe);
} else if (mode === 'saved') {
  // Already saved, show success
  showSuccess(recipe);
}
```

2. **Keep existing endpoints for backward compatibility**

3. **Test thoroughly before deploying**

## Recipe Parser Library Details

The `recipe-parser.js` library is the core of the AI extraction system.

### Main Function: parseRecipe()

```javascript
const { parseRecipe } = require('./lib/recipe-parser');

const recipe = await parseRecipe(text, {
  contributor: 'Fergi',
  original_filename: 'recipe.pdf',
  source_type: 'file_upload'
});
```

**Returns:**
```javascript
{
  title: "Beef Bourguignon",
  description: "Classic French beef stew...",
  ingredients: [
    "2 lbs beef chuck, cut into 2-inch cubes",
    "4 slices bacon, chopped",
    ...
  ],
  instructions: [
    "Preheat oven to 325°F (165°C).",
    "In a large Dutch oven, cook 4 slices of chopped bacon...",
    "Brown 2 lbs of beef chuck cubes on all sides...",
    ...
  ],
  prep_time: 30,
  cook_time: 180,
  servings: "6-8",
  calories_per_serving: 450,
  cuisine: "French",
  meal_type: "dinner",
  difficulty: "medium",
  tags: ["comfort-food", "french", "slow-cooked"],
  confidence_score: 0.95,
  needs_review: false
}
```

### Helper Functions

**validateRecipe(recipe)**
- Checks all required fields present
- Validates arrays have items
- Warns if instructions missing quantities

**estimateMissingData(recipe)**
- Estimates prep_time from ingredient count
- Estimates cook_time from instruction count
- Sets default servings and calories

**normalizeRecipe(recipe)**
- Cleans title and description
- Validates cuisine and meal_type
- Ensures tags is an array
- Converts servings to string

## AI Prompting Strategy

The recipe parser uses a detailed prompt to ensure high-quality extraction:

### Critical Requirements

1. **Ingredients List (for shopping):**
   - Clean, structured format
   - Quantities included
   - "2 cups flour", "1 cup sugar"

2. **Instructions (for cooking):**
   - **MOST IMPORTANT**: Embed quantities in each step
   - "Mix 2 cups flour with 1 cup sugar"
   - NOT: "Mix the flour with the sugar"
   - Cook should never refer back to ingredients

3. **Both sections include quantities:**
   - Redundancy is intentional
   - Ingredients = shopping reference
   - Instructions = cooking reference

### Prompt Excerpt

```
⭐ CRITICAL REQUIREMENTS:

1. **Ingredients List** (for shopping):
   - Clean, structured list with quantities
   - Format: "2 cups all-purpose flour", "1 cup granulated sugar"

2. **Instructions** (for cooking) - MOST IMPORTANT:
   - Step-by-step instructions
   - **EMBED QUANTITIES IN EACH STEP**
   - Example GOOD: "In a large bowl, mix 2 cups all-purpose flour with 1 cup granulated sugar"
   - Example BAD: "Mix the flour with the sugar" (missing quantities!)
```

### Model Configuration

```javascript
const message = await anthropic.messages.create({
  model: 'claude-sonnet-4-20250514',  // High quality
  max_tokens: 4000,                    // Enough for long recipes
  temperature: 0.3,                    // Low = more consistent
  messages: [{ role: 'user', content: prompt }]
});
```

## Quality Standards

All recipes processed through the Add Recipe system must meet the same standards as batch processing:

### Required Fields ✅

- title (never filename like IMG_8111.JPG)
- description (1-3 sentences)
- ingredients (array of strings)
- instructions (array of strings)
- prep_time (integer minutes)
- cook_time (integer minutes)
- servings (string or number)
- calories_per_serving (integer)

### Best Practices ✅

- Instructions have embedded ingredient quantities
- Cuisine is classified (American, Italian, French, etc.)
- Meal type is specified (breakfast, lunch, dinner, etc.)
- Difficulty is set (easy, medium, hard)
- Tags are relevant and searchable
- Source attribution is preserved

### Review Flags ⚠️

Recipes are flagged for review if:
- confidence_score < 0.8
- Instructions missing embedded quantities
- Very short (< 3 ingredients or instructions)
- OCR quality is poor
- Missing critical metadata

## Testing the Enhanced System

### Unit Testing

Test the recipe parser directly:

```javascript
const { parseRecipe } = require('./netlify/functions/lib/recipe-parser');

const sampleText = `
Chocolate Chip Cookies

Ingredients:
- 2 cups flour
- 1 cup sugar
- 1 cup chocolate chips

Instructions:
1. Mix ingredients
2. Bake at 350F for 12 minutes
`;

const recipe = await parseRecipe(sampleText);
console.log(recipe);
```

### Integration Testing

Test the full workflow:

```bash
# 1. Start local dev server
netlify dev

# 2. Open http://localhost:8888/add-recipe.html

# 3. Upload a test PDF or image

# 4. Verify extraction and formatting

# 5. Save and check recipes.json
```

### End-to-End Testing

Test with real files from GitHub:

```bash
# Run the test extraction script
node test-extraction.js

# Check output
cat test-recipes.json | jq '.[0] | {title, ingredients, instructions}'
```

## Deployment

### Deploy New Functions

```bash
# Deploy with new/updated functions
netlify deploy --prod --message="Enhanced Add Recipe with AI parsing"
```

### Verify Deployment

1. Check function logs:
   ```bash
   netlify functions:list
   netlify logs:function extract-file
   netlify logs:function format-recipe
   ```

2. Test on production:
   - Go to https://fergi-cooking.netlify.app/add-recipe.html
   - Upload a test recipe
   - Verify it appears correctly

## Troubleshooting

### Issue: AI Returns Unparseable JSON

**Symptom:** "Could not parse recipe JSON from AI response"

**Solution:**
- Check the AI response in logs
- May have included markdown or extra text
- The parser tries to extract JSON, but may fail
- Increase temperature or adjust prompt

### Issue: Instructions Missing Quantities

**Symptom:** Recipe flagged with needs_review=true

**Solution:**
- The AI prompt emphasizes this, but may still miss
- Add more examples to the prompt
- Review and manually add quantities
- Consider increasing max_tokens

### Issue: OCR Fails on Image

**Symptom:** "Could not extract meaningful text"

**Solution:**
- Image may be too blurry or low resolution
- Try converting image to PDF first
- Manually type the recipe
- Use a better quality scan

### Issue: File Upload Times Out

**Symptom:** Request timeout on large PDFs

**Solution:**
- Netlify functions have 10-second timeout (26s for paid plans)
- Large files or OCR may exceed this
- Consider splitting into chunks
- Or process files locally first

## Performance Considerations

### API Costs

Claude API costs for recipe formatting:
- ~2000-3000 tokens per recipe
- ~$0.003 per recipe with Sonnet
- ~$0.0005 per recipe with Haiku (cheaper, lower quality)

### Processing Time

- PDF extraction: 1-3 seconds
- OCR (images): 30-60 seconds
- AI parsing: 3-5 seconds
- **Total**: 5-70 seconds depending on file type

### Optimization Tips

1. **Cache results:** Don't re-process the same file
2. **Use Haiku for simple recipes:** Cheaper and faster
3. **Batch processing:** Use regenerate-database.js for many files
4. **Preprocess images:** Convert to text manually if possible

## Future Enhancements

### Potential Improvements

1. **Smart duplicate detection:**
   - Compare title/ingredients before saving
   - Warn user if recipe already exists

2. **Recipe suggestions:**
   - Suggest similar recipes
   - Auto-tag based on existing recipes

3. **Batch upload:**
   - Upload multiple files at once
   - Process in background
   - Email when complete

4. **Recipe variations:**
   - Link related recipes
   - Track modifications over time

5. **Nutrition analysis:**
   - Calculate accurate nutritional info
   - Integration with nutrition APIs

6. **Multi-language support:**
   - Detect recipe language
   - Translate ingredients/instructions

## Code Examples

### Using recipe-parser in Custom Scripts

```javascript
const { parseRecipe, validateRecipe, normalizeRecipe } = require('./netlify/functions/lib/recipe-parser');

async function processCustomRecipe(text) {
  try {
    // Parse with AI
    const recipe = await parseRecipe(text, {
      contributor: 'Custom',
      source_type: 'custom_script'
    });

    // Validate
    validateRecipe(recipe);

    // Normalize
    normalizeRecipe(recipe);

    // Do something with recipe
    console.log(`Processed: ${recipe.title}`);
    return recipe;

  } catch (error) {
    console.error('Error processing recipe:', error);
    throw error;
  }
}
```

### Customizing the AI Prompt

Edit `netlify/functions/lib/recipe-parser.js`:

```javascript
const prompt = `You are formatting a recipe for the Ferguson family cookbook.

CUSTOM REQUIREMENT: Always include "family-favorite" tag.

CUSTOM REQUIREMENT: Estimate cooking for high altitude (add 10% to times).

... rest of prompt ...
`;
```

### Adding Custom Validation

```javascript
function validateRecipe(recipe) {
  // Existing validation...

  // Custom validation
  if (recipe.cuisine === 'Italian' && !recipe.tags.includes('pasta')) {
    console.warn(`Italian recipe "${recipe.title}" should probably have 'pasta' tag`);
  }

  return true;
}
```

## Summary

The enhanced Add Recipe system provides:

✅ AI-powered recipe extraction from files
✅ Same quality standards as batch processing
✅ User review and editing before saving
✅ Immediate visibility (Dropbox integration)
✅ Reusable recipe-parser library
✅ Comprehensive error handling and validation

**Key Files:**
- `netlify/functions/lib/recipe-parser.js` - Core parsing logic
- `netlify/functions/add-recipe-enhanced.js` - Optional all-in-one endpoint
- `add-recipe.html` - User interface (already functional!)
- `BATCH_PROCESSING_GUIDE.md` - For bulk recipe processing

**Next Steps:**
1. Test the current system at https://fergi-cooking.netlify.app/add-recipe.html
2. Optionally migrate to add-recipe-enhanced.js for simpler architecture
3. Run batch processing to add 131 recipes from GitHub
4. Monitor and review recipes flagged for manual review

---

**Questions?** Check the code in `recipe-parser.js` for implementation details.
