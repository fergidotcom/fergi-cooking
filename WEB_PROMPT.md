# Web Prompt: AI-Powered Recipe Database Regeneration

Copy and paste this entire prompt into Claude Code Web:

---

I need you to regenerate the recipe database for the Fergi Cooking App by extracting and processing 131 recipe source files from GitHub using AI.

## Project Repository
https://github.com/fergidotcom/fergi-cooking

## Documentation (Read These First)
1. **RECIPE_DATABASE_REGENERATION_SPEC.md** - Complete technical specification
2. **WEB_SESSION_GUIDE.md** - Quick start guide with file access patterns

## Recipe Sources to Process

### Fergi Recipes (46 files)
- **Location**: `Fergi Recipes/` folder in repo
- **Formats**: 40 PDFs, 6 Apple Pages documents
- **Contributor**: All → "Fergi" (contributor_id: 1)
- **Access Pattern**: `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Fergi%20Recipes/{filename}`

### Janet Recipes (85 files)
- **Location**: `Janet Recipes/` folder in repo
- **Formats**: 85 JPG images (IMG_8111.JPG through IMG_8195.JPG)
- **Contributor**: All → "Janet" (contributor_id: 2)
- **Access Pattern**: `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Janet%20Recipes/IMG_{number}.JPG`
- **CRITICAL**: Recipe titles are IN the images, NOT the filenames. Use OCR to extract actual recipe names.

## Required Data Extraction (Per Recipe)

**Required Fields:**
1. **title** - Recipe name (MUST extract from Janet images, not use IMG_XXXX.JPG)
2. **description** - 1-3 sentences (extract or AI-generate)
3. **ingredients** - Structured list with quantities for shopping
4. **instructions** - Step-by-step with ingredients embedded (see critical requirement below)
5. **prep_time** - Integer (minutes)
6. **cook_time** - Integer (minutes)
7. **servings** - Integer or range (e.g., "4-6")
8. **calories_per_serving** - Integer estimate
9. **contributor_id** - 1 for Fergi, 2 for Janet

**Optional but Recommended:**
- cuisine, meal_type, difficulty, dietary_tags, source_attribution

## ⭐ CRITICAL REQUIREMENT: Instructions with Embedded Ingredients

Each cooking instruction step that uses ingredients MUST include the quantities in the step itself.

**Example - BAD ❌:**
```
"Preheat oven to 325°F."
"Cook the bacon until crispy."
"Brown the beef on all sides."
"Add onion and garlic, sauté until softened."
```

**Example - GOOD ✅:**
```
"Preheat oven to 325°F (165°C)."
"In a large Dutch oven, cook 4 slices of chopped bacon over medium heat until crispy. Remove and set aside."
"In the same pot with bacon fat, brown 2 lbs of beef chuck cubes on all sides, working in batches. Remove and set aside."
"Add 1 large diced onion and 3 minced garlic cloves to the pot. Sauté until softened, about 5 minutes."
```

**Why**: The cook should never need to refer back to the ingredients list while cooking.

## Processing Strategy

1. **Access the repository** and read both documentation files
2. **Test file access** with a few sample files (1 PDF, 1 Pages, 1 JPG)
3. **Extract text** from files:
   - PDFs: Use text extraction or Claude file reading
   - Pages: Convert or extract text
   - JPGs: Use OCR (Claude Vision or similar)
4. **Parse with AI** (Claude API) to structure recipe data
5. **Generate missing data** using AI (descriptions, estimates)
6. **Format instructions** with embedded ingredients
7. **Validate** all required fields present
8. **Process in batches** (10-20 recipes at a time)
9. **Log progress** to track completion

## Output Files

Generate these files:

### Database Files
1. **recipes.db** - SQLite database with all 131 recipes
2. **recipes.json** - JSON export for Netlify deployment
3. **extraction_log.json** - Processing log with any warnings
4. **recipes_needing_review.json** - Recipes flagged for manual review
5. **extraction_summary.md** - Final report with statistics

### Enhanced Add Recipe Function (CRITICAL)
6. **add-recipe-enhanced.js** - Updated Netlify function with AI extraction
7. **recipe-parser.js** - Reusable library for parsing recipes with AI
8. **ADD_RECIPE_INTEGRATION.md** - Documentation for the enhanced Add Recipe feature

**The enhanced Add Recipe function must:**
- Accept file uploads (PDF, DOCX, JPG/PNG images, text)
- Extract text using the same methods as batch processing
- Parse with AI to structure recipe data
- Format instructions with embedded ingredients (same as batch)
- Generate missing data (descriptions, estimates)
- Validate all required fields
- Allow user to preview and edit before saving
- Use the same quality standards as the batch regeneration

## Database Schema

```sql
CREATE TABLE recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    prep_time INTEGER,
    cook_time INTEGER,
    servings TEXT,
    difficulty TEXT,
    cuisine TEXT,
    meal_type TEXT,
    source_attribution TEXT,
    contributor_id INTEGER,
    needs_review INTEGER DEFAULT 0,
    calories_per_serving INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (contributor_id) REFERENCES contributors(id)
);

CREATE TABLE ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_text TEXT NOT NULL,
    quantity REAL,
    unit TEXT,
    ingredient_name TEXT,
    display_order INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction_text TEXT NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

CREATE TABLE contributors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    display_name TEXT,
    bio TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Pre-populate contributors
INSERT INTO contributors (id, name, display_name) VALUES
(1, 'Fergi', 'Fergi'),
(2, 'Janet', 'Janet');
```

## Example Recipe Output (JSON)

```json
{
  "title": "Beef Bourguignon",
  "description": "A classic French beef stew braised in red wine with pearl onions, mushrooms, and bacon. Rich, hearty, and perfect for cold weather.",
  "ingredients": [
    "2 lbs beef chuck, cut into 2-inch cubes",
    "4 slices bacon, chopped",
    "1 large onion, diced",
    "3 cloves garlic, minced",
    "2 cups red wine",
    "2 cups beef broth"
  ],
  "instructions": [
    "Preheat oven to 325°F (165°C).",
    "In a large Dutch oven, cook 4 slices of chopped bacon over medium heat until crispy. Remove and set aside.",
    "In the same pot with bacon fat, brown 2 lbs of beef chuck cubes on all sides, working in batches. Remove and set aside.",
    "Add 1 large diced onion and 3 minced garlic cloves to the pot. Sauté until softened, about 5 minutes.",
    "Pour in 2 cups of red wine and 2 cups of beef broth, scraping up any browned bits.",
    "Return the beef and bacon to the pot. Cover and transfer to the oven.",
    "Braise for 2.5 hours until beef is tender."
  ],
  "prep_time": 30,
  "cook_time": 180,
  "servings": "6",
  "calories_per_serving": 520,
  "contributor_id": 1,
  "cuisine": "French",
  "meal_type": "dinner",
  "difficulty": "medium",
  "source_attribution": "Epicurious"
}
```

## Quality Assurance Checklist

Before finalizing:
- [ ] All 46 Fergi recipes processed
- [ ] All 85 Janet recipes processed
- [ ] All recipes have valid titles (not IMG_8XXX.JPG)
- [ ] All instructions have embedded ingredient quantities
- [ ] All required fields populated
- [ ] Contributors correctly assigned (Fergi=1, Janet=2)
- [ ] No duplicate recipes
- [ ] Database schema matches specification
- [ ] recipes.json is valid and ready for deployment

## Success Criteria

- 131 total recipes extracted
- 100% have all required fields
- 100% have properly formatted instructions with embedded ingredients
- All Janet recipes have actual recipe names (extracted from images)
- Database ready for immediate deployment

## Enhanced Add Recipe Integration

After completing the batch regeneration, you MUST create an enhanced Add Recipe system that uses the same AI extraction logic.

### Requirements:

**1. Recipe Parser Library (`recipe-parser.js`)**
- Reusable JavaScript module with AI recipe parsing functions
- Extract text from various file formats (PDF, DOCX, images)
- Parse recipe structure with Claude API
- Format instructions with embedded ingredients
- Estimate missing data (times, servings, calories)
- Validate recipe completeness

**2. Enhanced Netlify Function (`add-recipe-enhanced.js`)**
- Replace or enhance existing `netlify/functions/add-recipe.js`
- Accept multipart/form-data file uploads
- Support multiple file formats:
  - PDF documents
  - Word documents (DOCX)
  - Images (JPG, PNG) with OCR
  - Plain text files
  - Apple Pages (if possible)
- Process uploaded file using recipe-parser library
- Return structured recipe data for preview
- Allow user edits before final save
- Save to Dropbox (recipes.json)

**3. Frontend Integration**
- Update `add-recipe.html` UI to support file upload
- Show AI extraction progress/status
- Display extracted recipe for review/editing
- Allow manual correction of any field
- Highlight uncertain extractions
- Preview formatted recipe before saving

**4. API Flow:**
```
User uploads file →
extract-file.js (text extraction) →
add-recipe-enhanced.js (AI parsing) →
Return structured data →
User reviews/edits →
Save to database
```

**5. Quality Standards:**
- Same instruction formatting as batch (embedded ingredients)
- Same validation as batch (all required fields)
- Same AI prompting for consistency
- Flag uncertain extractions for user review

### Code Deliverables:

1. `netlify/functions/lib/recipe-parser.js` - Core parsing library
2. `netlify/functions/add-recipe-enhanced.js` - Enhanced function
3. `add-recipe.html` - Updated UI (or create `add-recipe-v2.html`)
4. `ADD_RECIPE_INTEGRATION.md` - Integration documentation
5. Example AI prompts used for parsing
6. Test cases showing the flow

### Integration Notes:

- Reuse existing `extract-file.js` for text extraction
- Reuse existing `format-recipe.js` patterns for AI formatting
- Maintain backward compatibility with manual recipe entry
- Make file upload optional (keep manual entry option)
- Store extraction confidence scores with recipes
- Allow "needs_review" flag for low-confidence extractions

## Notes

- **DO NOT** include recipes from Adrienne_Cookbook (already excluded from repo)
- **Flag for review** any recipes where extraction is uncertain
- **Estimate conservatively** for missing data (times, calories)
- **Be consistent** with formatting and structure across all recipes
- **CRITICAL**: Build the enhanced Add Recipe system using the same extraction logic as the batch processing

---

**Deliverables Summary:**
1. Complete recipe database (131 recipes)
2. Enhanced Add Recipe function with AI extraction
3. Reusable recipe parsing library
4. Full documentation and integration guide

Start by reading the documentation files from GitHub, then begin processing the recipe files. Provide status updates as you progress through batches of recipes, and notify when ready to build the Add Recipe enhancement.
