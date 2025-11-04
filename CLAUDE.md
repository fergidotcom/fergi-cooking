# CLAUDE.md - Cooking Project

This file provides guidance to Claude Code (claude.ai/code) when working with the Cooking project.

## Infrastructure

@~/.claude/global-infrastructure.md

## Project Overview

**Cooking Project** - A personal recipe collection and management system for organizing, searching, and managing family recipes and cooking resources.

**Project Location:** `/Users/joeferguson/Library/CloudStorage/Dropbox/Fergi/Cooking`
**Created:** October 30, 2025
**Status:** ✓ Production - Deployed to Netlify (v3.1.6)
**Live URL:** https://fergi-cooking.netlify.app
**Cooking Mode:** https://fergi-cooking.netlify.app/cooking.html?recipe_id=5
**Purpose:** Organize and manage recipe collection, create searchable recipe database, document family recipes, manage cooking events with guest preferences, import recipes with AI formatting, manage contributors, mobile cooking mode for Janet

## 🆕 Recent Updates - November 4, 2025

**v3.1.6 - FEATURE: Needs Review Filter (Nov 4):**
- ✅ Scanned database and flagged 23 incomplete recipes
- ✅ Added "⚠️ Needs Review" button to navigation bar
- ✅ Red warning badge on recipe cards needing review
- ✅ Filter shows recipes missing ingredients (4) or instructions (19)
- ✅ Added needs_review field to recipe schema
- ✅ Console logging for debugging review filter
- ✅ All flagged recipes uploaded to Dropbox

**v3.1.5 - BUGFIX: Contributor Display (Nov 4):**
- ✅ Recipe cards now show contributor name (👤 Janet / 👤 Fergi)
- ✅ Fixed: cards were showing source_attribution instead of contributor
- ✅ Improved contributor filter with better refresh behavior
- ✅ Added debug logging to contributor filter
- ✅ Filter now clears grid before rendering new results

**v3.1.4 - BUGFIX: Contributor Assignments (Nov 4):**
- ✅ Fixed contributor filter returning no results for "Fergi"
- ✅ Assigned contributors to all 122 recipes (89 Janet, 33 Fergi)
- ✅ Renamed "Janet Mason" to "Janet" throughout system
- ✅ Created fix_contributors.py script for bulk assignment
- ✅ Updated contributors.json with new name
- ✅ Uploaded all data to Dropbox (production database)
- ✅ Contributor filter now fully functional

**v3.1.0 - MOBILE COOKING MODE + Auth Backend:**
- ✅ NEW: cooking.html - Mobile-first cooking interface
- ✅ Large text (18-28px) readable from 2 feet away while cooking
- ✅ Big step numbers in colored circles (40px)
- ✅ Ingredient checkboxes to mark off as you use them
- ✅ Wake Lock API - screen stays on automatically!
- ✅ Shareable URLs: cooking.html?recipe_id=X
- ✅ "Cooking Mode" button added to recipe detail modal
- ✅ NEW: send-verification-code.js - Email 6-digit codes
- ✅ NEW: verify-code.js - Validate codes, create sessions
- ✅ Passwordless authentication backend (UI pending - Phase 2)
- ✅ 19 Netlify Functions deployed (was 17)
- ✅ 3 new contributors: Nancy, Lauren, The Cooks
- ✅ Complete Phase 2 & 3 design specification (DESIGN_SPEC_V3.1)
- ✅ Solves Janet's mobile cooking pain point!

**v3.0.0 - MAJOR: Recipe Import System with Contributor Management (Nov 3):**
- ✅ Complete recipe import wizard with 4-step process
- ✅ File upload support: PDF, Word (DOCX), Images (OCR), Plain Text
- ✅ AI-powered recipe formatting using Claude API
- ✅ Contributor management system (public, no authentication)
- ✅ Contributor filter dropdown and statistics
- ✅ Automatic bulk assignment: 85 Janet Mason recipes, 37 Fergi recipes
- ✅ All data migrated to Dropbox for real-time updates (no redeployment needed)
- ✅ Single database architecture: recipes.json in Dropbox (shared with Reference Refinement)
- ✅ Beautiful two-column print layout for recipes
- ✅ 17 Netlify Functions deployed
- ✅ New dependencies: pdf-parse, mammoth, tesseract.js, @anthropic-ai/sdk

**v2.8.1 - Custom Dish Name Fix:**
- ✅ Fixed custom dish name handling for "will_bring" responses
- ✅ Smart detection: user input becomes dish name, not description
- ✅ Improved form labels with clear help text
- ✅ Example: Murray prefers Beef Stroganoff but brings Fish → Shows "You will bring: Fish"

**v2.8.0 - CRITICAL: API Endpoints Fixed:**
- ✅ Fixed broken get-recipe and get-recipes API endpoints
- ✅ Bundled recipes.json with Netlify Functions (added `included_files` config)
- ✅ Recipe names now display correctly throughout system
- ✅ Both single recipe and all recipes endpoints fully functional
- ✅ Dual loading strategy: try get-recipe first, fallback to get-recipes

**v2.7.9 - Enhanced Recipe Loading:**
- ✅ Robust recipe loading with dual strategy and comprehensive error handling
- ✅ Loading screen displays while fetching recipe details
- ✅ Form refuses to display without recipe data (prevents "Recipe #X" errors)
- ✅ Detailed console logging with emojis for debugging

**v2.7.8 - Recipe Name Display Improvements:**
- ✅ Removed all "Recipe #X" fallback text
- ✅ Shows actual recipe names (e.g., "Beef Stroganoff", "Bananas Foster")
- ✅ Context-aware headings (prefer vs. will_bring)

**Documentation:**
- ✅ SESSION_SUMMARY_2025-11-03_RECIPE_DISPLAY_FIXES.md - Comprehensive documentation
- ✅ All fixes, root causes, and solutions documented
- ✅ API testing procedures documented

## Project Structure

```
Cooking/
├── CLAUDE.md                           # This file - Project documentation
├── DEPLOYMENT.md                       # ⭐ Netlify deployment guide
├── DESIGN_SPEC_V3.1_USER_EVENTS_MOBILE.md  # ⭐ NEW v3.1 - Complete 3-phase spec
├── SESSION_SUMMARY_2025-11-03_V3.1_COOKING_MODE.md  # ⭐ NEW v3.1 session
├── cooking.html                        # ⭐ NEW v3.1 - Mobile cooking mode!
├── index.html                          # Recipe browsing interface (deployed)
├── events.html                         # Event management interface (deployed)
├── event-detail.html                   # Event dashboard (deployed)
├── respond.html                        # Guest response page (deployed)
├── add-recipe.html                     # Recipe import wizard (deployed)
├── recipes.json                        # Recipe data (122 recipes, deployed)
├── recipes.db                          # SQLite database (local only)
├── netlify.toml                        # Netlify configuration
├── netlify/functions/                  # Serverless functions (19 total)
│   ├── lib/
│   │   └── dropbox-auth.js            # ⭐ OAuth helper (auto-refresh tokens)
│   ├── get-recipe.js                  # Get/Update single recipe (GET + PUT)
│   ├── get-recipes.js                 # Get all/search recipes
│   ├── save-recipes.js                # Bulk save recipes
│   ├── load-recipes.js                # Load from Dropbox
│   ├── add-recipe.js                  # Add new recipe
│   ├── update-recipe.js               # Update recipe
│   ├── extract-file.js                # Extract text from uploads
│   ├── format-recipe.js               # AI recipe formatting
│   ├── manage-contributors.js         # Contributor CRUD
│   ├── create-event.js                # Create/update events
│   ├── get-events.js                  # Get events
│   ├── save-events.js                 # Save events to Dropbox
│   ├── event-recipes.js               # Add/remove recipes from events
│   ├── record-selection.js            # Record guest responses
│   ├── generate-email.js              # Generate event emails
│   ├── send-verification-code.js      # ⭐ NEW v3.1 - Email codes
│   ├── verify-code.js                 # ⭐ NEW v3.1 - Validate codes
│   └── statistics.js                  # Recipe statistics
├── *.pdf                               # Original recipe PDFs (50+ files)
├── *.pages                             # Original recipe documents
└── Janet Mason/                        # Sub-collection (85 images)
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
- **SESSION_SUMMARY_2025-11-04_CONTRIBUTOR_FIX.md** - ⭐ Latest: Contributor assignment fix
- **SESSION_SUMMARY_2025-11-03_RECIPE_DISPLAY_FIXES.md** - Recipe display and API fixes
- **SESSION_SUMMARY_2025-11-02_DELETE_FIX.md** - Bug fix documentation
- **RECIPE_INSTRUCTION_REFORMATTING_SUMMARY.md** - Recipe instruction updates
- **fix_contributors.py** - Script to fix contributor assignments (NEW v3.1.4)
- **reformat_instructions.py** - Script to reformat recipe instructions
- **recipes.db** - SQLite database (not deployed)
- **recipes.json** - JSON export for web interface (bundled with Netlify Functions)
- **netlify.toml** - Netlify configuration (includes recipes.json bundling)
- **netlify/functions/data/contributors.json** - Contributor list
- **index.html** - Recipe browsing interface (deployed to Netlify)
- **events.html** - Event management interface (deployed to Netlify)
- **event-detail.html** - Event dashboard (deployed to Netlify)
- **respond.html** - Public guest response page (deployed to Netlify)
- **cooking.html** - Mobile cooking mode (deployed to Netlify)

## Notes

The recipe collection represents years of accumulated cooking knowledge and family traditions. The database preserves original recipe metadata while the web interface makes everything searchable and accessible.

**Development Guidelines:**
- Always backup database before bulk updates
- Test locally with `netlify dev` before deploying
- Keep recipes.json in sync with recipes.db
- Preserve original PDF/Pages files for reference
- Document significant changes in session summaries

---

**Last Updated:** November 4, 2025
**Version:** v3.1.6
**Status:** ✓ Production - Live at https://fergi-cooking.netlify.app
**Database:** 122 recipes (89 Janet, 33 Fergi, 23 need review) | **19 Netlify Functions** | **All APIs Working**

**Core Features:**
- Recipe browsing, search, and filtering
- Contributor management (public, no authentication)
- Contributor filter dropdown and statistics
- **NEW: Recipe import wizard (4-step process)**
- **NEW: File upload support (PDF, Word, Images with OCR, Text)**
- **NEW: AI-powered recipe formatting (Claude API)**
- **NEW: Beautiful two-column print layout**
- Janet's Cookbook (89 recipes, properly assigned to Janet contributor)
- Event creation and management
- Recipe-to-event assignment
- Guest preference collection (with actual recipe names!)
- Custom dish name handling (bring something different than selected recipe)
- Volunteer category collection
- Email generation with multiple copy methods
- Public guest responses without login
- Dietary restrictions and own dish tracking
- Context-aware response UI (prefer vs. will_bring)
- Single database architecture (recipes.json in Dropbox, shared with Reference Refinement)
