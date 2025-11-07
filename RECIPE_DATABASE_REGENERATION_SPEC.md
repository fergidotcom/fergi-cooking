# Recipe Database Regeneration Specification

**Project**: Fergi Cooking App - Complete Database Rebuild
**Date**: November 7, 2025
**Purpose**: Generate a fresh, clean recipe database from source files using AI-powered extraction
**Target**: Claude Code Web session for batch AI processing

---

## Executive Summary

Regenerate the entire recipe database from scratch using source recipe files in various formats. All recipes will be extracted, analyzed, enhanced, and formatted using AI to create a consistent, high-quality database with proper contributor attribution.

---

## Source Files Inventory

### Fergi Recipes (46 files)
- **Location**: `Fergi Recipes/` directory
- **Formats**:
  - 40 PDF files (from NYT Cooking, Epicurious, various websites)
  - 6 Apple Pages documents (custom Fergi recipes)
- **Contributor**: All recipes → "Fergi"
- **Examples**:
  - Beef Bourguignon Joe's Recipe.pages
  - Chicken Piccata PDF
  - Various Epicurious PDFs

### Janet Recipes (85 files)
- **Location**: `Janet Recipes/` directory
- **Formats**: 85 JPG images (IMG_8111.JPG through IMG_8195.JPG)
- **Contributor**: All recipes → "Janet"
- **Note**: Sequential, meaningless filenames - recipe titles must be extracted from image content via OCR

---

## Required Data Extraction

For **each recipe**, extract or generate the following fields:

### 1. Title (REQUIRED)
- **Source**:
  - Fergi: May be in filename, but MUST be confirmed by file contents
  - Janet: Extract from JPG image via OCR
- **Format**: Clear, concise recipe name
- **Examples**: "Beef Bourguignon", "Chicken Piccata", "Banana Foster"

### 2. Description (REQUIRED)
- **Source**:
  - First try: Extract from recipe if included
  - Fallback: AI-generate based on title and recipe contents
- **Format**: 1-3 sentences describing the dish
- **Quality**: Appetizing, informative, accurate to the recipe

### 3. Ingredients for Shopping (REQUIRED)
- **Format**: Structured list with quantities
- **Example**:
  ```json
  [
    "2 lbs beef chuck, cut into 2-inch cubes",
    "4 slices bacon, chopped",
    "1 large onion, diced",
    "3 cloves garlic, minced"
  ]
  ```
- **Note**: Clean, standardized format for shopping lists

### 4. Cooking Instructions (REQUIRED - SPECIAL FORMAT)
- **Format**: Step-by-step with ingredients embedded
- **Critical Requirement**: Include quantities and ingredients in each step that uses them
- **Purpose**: Cook without referring back to ingredients list
- **Example**:
  ```json
  [
    "Preheat oven to 325°F (165°C).",
    "In a large Dutch oven, cook 4 slices of chopped bacon over medium heat until crispy. Remove and set aside.",
    "In the same pot with bacon fat, brown 2 lbs of beef chuck cubes on all sides. Remove and set aside.",
    "Add 1 large diced onion and 3 minced garlic cloves to the pot. Sauté until softened, about 5 minutes."
  ]
  ```

### 5. Prep Time (REQUIRED)
- **Source**: Extract from recipe or AI-estimate based on instructions
- **Format**: Integer (minutes)
- **Examples**: 15, 30, 45

### 6. Cook Time (REQUIRED)
- **Source**: Extract from recipe or AI-estimate based on instructions
- **Format**: Integer (minutes)
- **Examples**: 30, 60, 120

### 7. Servings (REQUIRED)
- **Source**: Extract from recipe or AI-estimate
- **Format**: Integer or range
- **Examples**: 4, 6, "4-6"

### 8. Calories per Serving (REQUIRED)
- **Source**: Extract from recipe or AI-estimate
- **Format**: Integer
- **Examples**: 450, 680, 320

### 9. Contributor (REQUIRED - AUTO-ASSIGNED)
- **Fergi Recipes** → contributor_id: 1 ("Fergi")
- **Janet Recipes** → contributor_id: 2 ("Janet")

### 10. Additional Metadata (OPTIONAL but recommended)
- **cuisine**: Italian, French, American, etc.
- **meal_type**: dinner, lunch, breakfast, dessert
- **difficulty**: easy, medium, hard
- **dietary_tags**: vegetarian, gluten-free, dairy-free, etc.
- **source_attribution**: Original source (NYT Cooking, Epicurious, etc.)

---

## Technical Requirements

### File Access via GitHub
All recipe source files must be committed to GitHub repository:
- **Repository**: https://github.com/fergidotcom/fergi-cooking.git
- **Branches**: Use `main` branch or create `recipe-sources` branch
- **Web Access**: Claude Code Web can access files via GitHub raw URLs

### AI Processing Requirements
- **OCR**: Required for all 85 Janet Recipe JPG images
- **Text Extraction**: Required for all PDF and Pages files
- **AI Analysis**: Use Claude API to:
  - Parse and understand recipe structure
  - Generate missing descriptions
  - Estimate missing times, servings, calories
  - Format instructions with embedded ingredients
  - Standardize ingredient lists
  - Extract or infer metadata

### Output Format
- **Database**: SQLite (`recipes.db`)
- **JSON Export**: `recipes.json` for Netlify Functions
- **Schema**: Use existing Cooking app schema (see below)

---

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
```

### Contributors (Pre-populate)
```sql
INSERT INTO contributors (id, name, display_name) VALUES
(1, 'Fergi', 'Fergi'),
(2, 'Janet', 'Janet');
```

---

## Processing Workflow

### Phase 1: Setup & File Access
1. Commit `Fergi Recipes/` and `Janet Recipes/` folders to GitHub
2. Verify files are accessible via GitHub raw URLs
3. Create processing script in Web session

### Phase 2: Extract Fergi Recipes (46 files)
1. For each PDF file:
   - Extract text using pdf-parse or similar
   - Parse with Claude API
   - Structure data
2. For each Pages file:
   - Extract text using mammoth or similar
   - Parse with Claude API
   - Structure data
3. Validate all required fields present
4. Assign contributor_id = 1

### Phase 3: Extract Janet Recipes (85 JPG files)
1. For each JPG image:
   - Perform OCR using tesseract.js or Claude Vision
   - Parse extracted text with Claude API
   - Extract recipe title from image (critical!)
   - Structure data
2. Validate all required fields present
3. Assign contributor_id = 2

### Phase 4: AI Enhancement
For recipes missing data:
1. Generate descriptions if missing
2. Estimate prep/cook times if missing
3. Estimate servings if missing
4. Estimate calories if missing
5. Infer cuisine, meal_type, difficulty

### Phase 5: Database Generation
1. Create new `recipes.db` from scratch
2. Insert all recipes with proper relationships
3. Generate `recipes.json` for Netlify deployment
4. Validate data integrity

### Phase 6: Quality Assurance
1. Verify all 131 recipes extracted (46 Fergi + 85 Janet)
2. Check for missing required fields
3. Validate contributor assignments
4. Test search and filtering
5. Flag any recipes needing manual review

---

## Integration with Cooking App

The extraction logic and standards developed for this regeneration should be incorporated into the **Add Recipe** feature:

### Enhanced Add Recipe Function
1. **File Upload Support**:
   - PDF documents
   - Word documents (DOCX)
   - Images (JPG, PNG) with OCR
   - Plain text
   - Apple Pages (if convertible)

2. **AI-Powered Parsing**:
   - Automatic structure detection
   - Ingredient extraction
   - Instruction formatting with embedded ingredients
   - Metadata inference

3. **Quality Standards**:
   - Same data requirements as regeneration
   - Consistent formatting
   - Automatic contributor assignment
   - Validation before save

4. **User Interface**:
   - Preview extracted data
   - Edit/refine before saving
   - Mark as "needs review" if uncertain
   - Batch upload support

---

## Success Criteria

- [ ] All 46 Fergi recipes extracted and formatted
- [ ] All 85 Janet recipes extracted with correct titles
- [ ] 100% of recipes have all required fields
- [ ] Cooking instructions include ingredient quantities in each step
- [ ] Contributors properly assigned (Fergi vs Janet)
- [ ] Database schema matches existing app
- [ ] recipes.json generated and valid
- [ ] Enhanced Add Recipe function deployed
- [ ] Quality assurance completed
- [ ] Documentation updated

---

## File Deliverables

1. **recipes.db** - New clean SQLite database
2. **recipes.json** - JSON export for Netlify
3. **extraction_log.json** - Processing log with any errors/warnings
4. **recipes_needing_review.json** - List of recipes flagged for review
5. **extraction_script.py** - Reusable extraction script
6. **add_recipe_enhanced.js** - Updated Netlify function
7. **REGENERATION_SUMMARY.md** - Final report

---

## Notes for Web Session

- **Primary Tool**: Claude API for all AI analysis and enhancement
- **OCR Tool**: Tesseract.js or Claude Vision API
- **Text Extraction**: pdf-parse (PDFs), mammoth (DOCX)
- **Processing**: Batch process in groups to manage API limits
- **Error Handling**: Log all issues, flag uncertain extractions
- **Validation**: Strict validation of all required fields before database insert

---

## Repository Info

- **GitHub Repo**: https://github.com/fergidotcom/fergi-cooking.git
- **Live App**: https://fergi-cooking.netlify.app
- **Branch**: main (or create recipe-sources branch)
- **Source Files**: `Fergi Recipes/` and `Janet Recipes/` directories

---

**Ready for Web Session Processing**
