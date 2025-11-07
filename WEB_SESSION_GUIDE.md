# Web Session Guide: Recipe Database Regeneration

**Project**: Fergi Cooking App - AI-Powered Recipe Extraction
**Date**: November 7, 2025
**Purpose**: Guide for Claude Code Web session to process 131 recipe sources

---

## Quick Start

1. **Read the specification**: `RECIPE_DATABASE_REGENERATION_SPEC.md`
2. **Access recipe sources via GitHub**:
   - Repository: https://github.com/fergidotcom/fergi-cooking
   - Fergi Recipes: https://github.com/fergidotcom/fergi-cooking/tree/main/Fergi%20Recipes
   - Janet Recipes: https://github.com/fergidotcom/fergi-cooking/tree/main/Janet%20Recipes
3. **Process all 131 recipes** using AI extraction
4. **Generate clean database** with proper formatting and contributor attribution
5. **Enhance Add Recipe function** with extraction logic

---

## File Access Pattern

All recipe files are accessible via GitHub raw URLs:

### Fergi Recipes (40 PDFs, 6 Pages)
```
https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Fergi%20Recipes/{filename}
```

**Examples**:
- `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Fergi%20Recipes/Beef%20Bourguignon%20Recipe%20%7C%20Epicurious.pdf`
- `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Fergi%20Recipes/Joes%20Meatloaf.pages`

### Janet Recipes (85 JPG images)
```
https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Janet%20Recipes/IMG_{number}.JPG
```

**Examples**:
- `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Janet%20Recipes/IMG_8111.JPG`
- `https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Janet%20Recipes/IMG_8195.JPG`

---

## Processing Strategy

### Recommended Approach

**Use Claude API for all AI tasks** - Web can access Claude API endpoints:
1. Extract text from files (OCR for images, text extraction for PDFs)
2. Parse recipe structure
3. Generate missing data (descriptions, estimates)
4. Format with embedded ingredients in instructions
5. Validate and structure data

### Batch Processing
- Process in groups of 10-20 recipes at a time
- Log progress to `extraction_progress.json`
- Handle errors gracefully
- Flag uncertain extractions for review

---

## Critical Requirements

### 1. Instructions with Embedded Ingredients ⭐ MOST IMPORTANT
Each cooking instruction step that uses ingredients MUST include the quantities:

**BAD** ❌:
```
"Add the bacon to the pot and cook until crispy."
"Brown the beef on all sides."
```

**GOOD** ✅:
```
"Add 4 slices of chopped bacon to the pot and cook until crispy."
"Brown 2 lbs of beef chuck cubes on all sides."
```

### 2. Recipe Titles from Janet Images
- Janet recipe JPGs have meaningless filenames (IMG_8111.JPG, etc.)
- **MUST extract actual recipe title from image via OCR**
- Do NOT use filename as title

### 3. Contributor Assignment
- **Fergi Recipes** → contributor_id: 1 ("Fergi")
- **Janet Recipes** → contributor_id: 2 ("Janet")

### 4. Required Fields
All recipes must have:
- title, description, ingredients, instructions
- prep_time, cook_time, servings
- calories_per_serving
- contributor_id

---

## Example Recipe Output

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
    "2 cups beef broth",
    "2 tablespoons tomato paste",
    "1 lb pearl onions, peeled",
    "8 oz mushrooms, quartered",
    "2 tablespoons butter",
    "2 tablespoons flour",
    "2 bay leaves",
    "1 teaspoon thyme",
    "Salt and pepper to taste"
  ],
  "instructions": [
    "Preheat oven to 325°F (165°C).",
    "In a large Dutch oven, cook 4 slices of chopped bacon over medium heat until crispy. Remove and set aside.",
    "In the same pot with bacon fat, brown 2 lbs of beef chuck cubes on all sides, working in batches. Remove and set aside.",
    "Add 1 large diced onion and 3 minced garlic cloves to the pot. Sauté until softened, about 5 minutes.",
    "Stir in 2 tablespoons of tomato paste and cook for 1 minute.",
    "Add 2 tablespoons of flour and stir to coat the vegetables.",
    "Pour in 2 cups of red wine and 2 cups of beef broth, scraping up any browned bits from the bottom.",
    "Return the beef and bacon to the pot. Add 2 bay leaves and 1 teaspoon of thyme.",
    "Cover and transfer to the oven. Braise for 2.5 hours until beef is tender.",
    "Meanwhile, in a skillet, melt 2 tablespoons of butter. Add 1 lb of pearl onions and 8 oz of quartered mushrooms. Sauté until golden, about 10 minutes.",
    "Add the sautéed onions and mushrooms to the stew during the last 30 minutes of cooking.",
    "Season with salt and pepper to taste before serving."
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

---

## Database Schema

See `RECIPE_DATABASE_REGENERATION_SPEC.md` for complete schema.

**Key tables**:
- `recipes` - Main recipe metadata
- `ingredients` - Structured ingredient list
- `instructions` - Numbered cooking steps
- `contributors` - Recipe contributors (Fergi, Janet)

---

## Output Files

Generate these files:

1. **recipes.db** - SQLite database with all 131 recipes
2. **recipes.json** - JSON export for Netlify deployment
3. **extraction_log.json** - Processing log
4. **recipes_needing_review.json** - Recipes flagged for manual review
5. **extraction_summary.md** - Final report with statistics

---

## Testing Recipe Access

Before full processing, test file access:

```javascript
// Test Fergi Recipe PDF
const fergiUrl = 'https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Fergi%20Recipes/Beef%20Bourguignon%20Recipe%20%7C%20Epicurious.pdf';

// Test Janet Recipe Image
const janetUrl = 'https://raw.githubusercontent.com/fergidotcom/fergi-cooking/main/Janet%20Recipes/IMG_8111.JPG';

// Both should be accessible via fetch or similar
```

---

## AI Enhancement Guidelines

When generating or estimating data:

**Descriptions**:
- 1-3 sentences
- Mention key flavors, ingredients, or characteristics
- Appetizing and accurate

**Prep/Cook Times**:
- Based on instruction complexity
- Realistic estimates
- Round to nearest 5 minutes

**Servings**:
- Based on ingredient quantities
- Common ranges: 2, 4, 6, 8

**Calories**:
- Reasonable estimates based on ingredients
- Consider portion sizes
- Accuracy within 10-20%

---

## Quality Assurance Checklist

- [ ] All 46 Fergi recipes processed
- [ ] All 85 Janet recipes processed
- [ ] All recipes have valid titles (not IMG_8XXX.JPG)
- [ ] All instructions have embedded ingredient quantities
- [ ] All required fields populated
- [ ] Contributors correctly assigned
- [ ] No duplicate recipes
- [ ] Database schema matches spec
- [ ] recipes.json valid and deployable

---

## Integration with Add Recipe Function

After successful extraction, update `netlify/functions/add-recipe.js` to incorporate:

1. **Text extraction logic** (PDF, DOCX, images)
2. **AI parsing patterns** for recipe structure
3. **Instruction formatting** with embedded ingredients
4. **Validation rules** for required fields
5. **Estimation algorithms** for missing data

---

## Contact & Support

- **GitHub Repo**: https://github.com/fergidotcom/fergi-cooking
- **Live App**: https://fergi-cooking.netlify.app
- **Spec Document**: `RECIPE_DATABASE_REGENERATION_SPEC.md`

---

## Ready to Start?

1. Clone or access the GitHub repository
2. Read the full specification
3. Test file access for both Fergi and Janet recipes
4. Begin batch processing with AI extraction
5. Generate clean database
6. Deploy to production

**Good luck with the extraction!**
