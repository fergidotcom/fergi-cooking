# CLAUDE.md - Cooking Project

This file provides guidance to Claude Code (claude.ai/code) when working with the Cooking project.

## Project Overview

**Cooking Project** - A personal recipe collection and management system for organizing, searching, and managing family recipes and cooking resources.

**Project Location:** `/Users/joeferguson/Library/CloudStorage/Dropbox/Fergi/Cooking`
**Created:** October 30, 2025
**Status:** ✓ Production - Deployed to Netlify
**Live URL:** https://fergi-cooking.netlify.app
**Purpose:** Organize and manage recipe collection, create searchable recipe database, document family recipes

## Project Structure

```
Cooking/
├── CLAUDE.md                           # This file - Project documentation
├── DEPLOYMENT.md                       # ⭐ Netlify deployment guide
├── index.html                          # Web interface (deployed to Netlify)
├── recipes.json                        # Recipe data for web interface
├── recipes.db                          # SQLite database (122 recipes)
├── netlify.toml                        # Netlify configuration
├── netlify/functions/                  # Serverless functions
│   ├── get-recipe.js                  # Get single recipe
│   ├── get-recipes.js                 # Get all/search recipes
│   └── statistics.js                  # Recipe statistics
├── *.pdf                               # Recipe PDFs (50+ files)
├── *.pages                             # Recipe documents (Pages format)
└── Janet Mason/                        # Sub-collection of recipes (85 images)
```

## Current Contents

The project contains 50+ recipe files including:

**Recipe Categories:**
- Main Dishes: Beef Bourguignon, Beef Stroganoff, Chicken Piccata, Meatloaf variants
- Vegetarian: Vegetable Korma, Eggplant Parmesan, Portabello Mushroom Stroganoff
- Pasta: Fettuccine Alfredo, Lasagna, Pasta Primavera
- Specialty: Jerk Chicken, Curries, French Onion Soup
- Breakfast: Breakfast Casseroles, Italian Baked Eggs

**File Formats:**
- PDF recipes (from web sources like NYT Cooking, Epicurious)
- Pages documents (custom recipes and modifications)
- Recipe collections (Adrienne Cookbook, NancyBernRecipes, etc.)

## Current Features (Implemented)

### ✓ Recipe Database
- SQLite database with 122 recipes
- Structured schema with ingredients, instructions, tags
- Full-text search capability
- Recipe metadata (prep time, servings, difficulty, cuisine)
- Recipe images and cooking logs

### ✓ Web Interface
- Live at https://fergi-cooking.netlify.app
- Browse all recipes with cards
- Search and filter recipes
- View recipe details with formatted ingredients and instructions
- Janet Mason's Cookbook section
- Recipe statistics dashboard
- Responsive design

### ✓ Recipe Search
- Full-text search across recipes
- Filter by source, cuisine, meal type
- Search in ingredients and instructions
- Tag-based filtering

### ✓ Serverless Backend
- Netlify Functions for API
- Get all recipes endpoint
- Get single recipe by ID
- Recipe statistics endpoint
- Search functionality

### ✓ Recipe Management
- Instructions reformatted with explicit ingredients (Nov 2, 2025)
- Import from Janet Mason's cookbook (85 recipes extracted from images)
- Recipe extraction from PDFs

## Future Enhancements

### Potential Features to Add:
- Recipe scaling calculator
- Meal planning tool
- Grocery list generator
- Cooking timer integration
- User notes and ratings (currently read-only)
- Recipe modifications tracking
- Nutritional information calculator
- Import from recipe websites
- Export to PDF/Markdown

## Development Notes

**File Access:**
- All files are in Dropbox, synced across devices
- PDF files can be read directly
- Pages documents may need conversion to extract text
- Some recipes have both .pages and .pdf versions

**Recipe Organization:**
- Many recipes from popular sources (NYT Cooking, Epicurious)
- Some custom family recipes (Joe's Meatloaf, Beef Bourguignon variants)
- Special collections (Adrienne Cookbook, Janet Mason subfolder)
- Recipes span multiple cuisines (American, Italian, Indian, Caribbean)

## Deployment to Netlify

**⭐ See DEPLOYMENT.md for complete deployment guide**

### Quick Deploy Command:
```bash
netlify deploy --prod --dir="." --message="Your deploy message"
```

### Key Information:
- **Live URL:** https://fergi-cooking.netlify.app
- **Admin:** https://app.netlify.com/projects/fergi-cooking
- **Account:** fergidotcom@gmail.com
- **Functions:** Automatically deployed from `netlify/functions/`
- **Data:** `recipes.json` is included in function bundle

### When to Deploy:
- After updating recipes in database (regenerate recipes.json first)
- After UI changes to index.html
- After function changes in netlify/functions/
- After reformatting instructions

### Testing Locally:
```bash
netlify dev
# Opens at http://localhost:8888
```

## Common Tasks

### Adding New Recipes
1. Add recipe to database (via SQL or import script)
2. Regenerate recipes.json: `python3 export_to_json.py`
3. Deploy to Netlify: `netlify deploy --prod --dir="." --message="Added new recipe"`
4. Original files can be saved to Cooking folder for reference

### Finding Recipes
- **Web Interface:** https://fergi-cooking.netlify.app
- **Search:** Use search bar in web interface
- **Database:** Query recipes.db directly with SQL
- **Local Files:** Original PDFs/Pages docs in Cooking folder

### Updating Recipe Instructions
When you need to reformat or fix recipe instructions:
1. Update in recipes.db database
2. Regenerate recipes.json
3. Deploy to Netlify
4. See `reformat_instructions.py` for bulk updates

### Recipe Database Management
```bash
# View database schema
sqlite3 recipes.db ".schema"

# Count recipes
sqlite3 recipes.db "SELECT COUNT(*) FROM recipes;"

# Search recipes
sqlite3 recipes.db "SELECT title FROM recipes WHERE title LIKE '%beef%';"

# Export to JSON
python3 export_to_json.py
```

### Deploying Changes
```bash
# Quick deploy
netlify deploy --prod --dir="." --message="Description"

# Test locally first
netlify dev

# Check status
netlify status
```

## Related Projects

**Reference Refinement** (`~/Library/CloudStorage/Dropbox/Fergi/AI Wrangling/References`)
- Similar document management and search challenges
- Could share search/indexing technology
- Both deal with organizing large document collections

**Ferguson Family Archive** (`~/Library/CloudStorage/Dropbox/Fergi/Ferguson Family Archive`)
- Family history and documentation
- Could include historical family recipes
- Recipe collection is part of family heritage

## Database Schema

The SQLite database (`recipes.db`) includes:
- **recipes** - Recipe metadata and details
- **ingredients** - Recipe ingredients with quantities
- **instructions** - Step-by-step cooking instructions
- **tags** - Recipe tags and categories
- **cooking_log** - Cooking history and notes
- **recipe_images** - Recipe images
- **recipes_fts** - Full-text search index

See database schema: `sqlite3 recipes.db ".schema"`

## Important Files

- **DEPLOYMENT.md** - Complete Netlify deployment guide
- **RECIPE_INSTRUCTION_REFORMATTING_SUMMARY.md** - Recent instruction updates
- **reformat_instructions.py** - Script to reformat recipe instructions
- **recipes.db** - SQLite database (not deployed)
- **recipes.json** - JSON export for web interface (deployed)
- **index.html** - Web interface (deployed to Netlify)

## Notes

The recipe collection represents years of accumulated cooking knowledge and family traditions. The database preserves original recipe metadata while the web interface makes everything searchable and accessible.

**Development Guidelines:**
- Always backup database before bulk updates
- Test locally with `netlify dev` before deploying
- Keep recipes.json in sync with recipes.db
- Preserve original PDF/Pages files for reference
- Document significant changes in session summaries

---

**Last Updated:** November 2, 2025
**Status:** ✓ Production - Live at https://fergi-cooking.netlify.app
**Database:** 122 recipes | **Web Interface:** Deployed to Netlify | **Features:** Search, Browse, Janet's Cookbook
