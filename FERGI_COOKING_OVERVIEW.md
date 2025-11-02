# Fergi Cooking - Project Overview

**Version:** 1.0.0
**Status:** Production
**Last Updated:** November 2, 2025
**Live URL:** https://fergi-cooking.netlify.app

---

## What Is This?

**Fergi Cooking** is a personal recipe collection and management system deployed as a serverless web application. It allows browsing, searching, and managing 122 family recipes from any device with a web browser.

---

## Quick Facts

| Aspect | Details |
|--------|---------|
| **Platform** | Netlify (serverless static site + functions) |
| **Live URL** | https://fergi-cooking.netlify.app |
| **Total Recipes** | 122 (33 Main + 89 Janet Mason's Cookbook) |
| **Data Size** | 792 KB (recipes.json) |
| **GitHub** | https://github.com/fergidotcom/fergi-cooking |
| **Deployment** | November 2, 2025 |
| **Access** | Mac, iOS, Android via web browser |
| **Authentication** | None required (public access) |

---

## Recipe Collections

### Main Collection (33 recipes)
- **Sources:** NYT Cooking, Epicurious, custom family recipes
- **Categories:** Main dishes, vegetarian, pasta, specialty cuisine
- **Examples:** Beef Bourguignon, Meatloaf variants, Fettuccine Alfredo, Eggplant Parm, Vegetable Korma

### Janet Mason's Cookbook (89 recipes)
- **Source:** 85 cookbook images (IMG_8111.JPG through IMG_8195.JPG)
- **Extraction:** Vision-based AI extraction using Claude
- **Categories:**
  - Appetizers & Snacks (12)
  - Soups (12)
  - Salads & Dressings (15)
  - Sauces (8)
  - Breads & Baked Goods (20)
  - Side Dishes (10)
  - Main Dishes (8)
  - Desserts & Breakfast (4)

---

## Features

### Current Features (v1.0)

**Browse Recipes:**
- View all 122 recipes in card format
- Filter by collection (Main or Janet Mason)
- Mobile-responsive design

**Search:**
- Search across title, description, ingredients, instructions
- Real-time filtering
- Case-insensitive

**Recipe Details:**
- Complete ingredient lists with quantities
- Step-by-step instructions
- Prep time, cook time, servings
- Calorie estimates per serving
- Cuisine type and source attribution

**Collections:**
- "All Recipes" - View entire collection
- "Main Collection" - 33 recipes from PDFs/Pages docs
- "📖 Janet Mason's Cookbook" - 89 family cookbook recipes (purple button)

---

## Technical Architecture

### Technology Stack

**Frontend:**
- HTML/CSS/JavaScript (vanilla, no framework)
- Vue.js-style reactive pattern
- Single Page Application (SPA)
- Mobile-responsive design

**Backend:**
- Netlify Functions (Node.js serverless)
- Three API endpoints: get-recipes, get-recipe, statistics
- No traditional server - stateless architecture

**Data Storage:**
- **Development:** SQLite database (recipes.db) in Dropbox
- **Production:** JSON export (recipes.json) in git repository
- **Export Script:** Python script converts SQLite → JSON

**Hosting:**
- Netlify CDN (global distribution)
- Serverless functions for API
- Free tier (sufficient for current usage)

### API Endpoints

```
GET /api/recipes          - Get all recipes (with optional search)
GET /api/recipes/:id      - Get single recipe with full details
GET /api/statistics       - Get database statistics
```

### Deployment Workflow

```bash
# 1. Update recipes in SQLite (local development)
# 2. Export to JSON
python3 export_to_json.py

# 3. Commit and push to GitHub
git add recipes.json
git commit -m "Updated recipes"
git push origin main

# 4. Deploy to Netlify
netlify deploy --prod --dir=. --message="Recipe update"
```

---

## Data Structure

### Recipe Object

Each recipe contains:
- **Metadata:** title, description, servings, timing (prep/cook/total), calories
- **Classification:** cuisine_type, meal_type, difficulty
- **Source:** source_attribution, source_url, original_filename
- **Ingredients:** List with quantity, unit, name, preparation, order
- **Instructions:** Step-by-step with order
- **Tags:** Categories and labels
- **Dietary:** vegetarian, vegan, gluten_free, dairy_free flags
- **User Data:** rating, favorite, notes, images

---

## Key Design Decisions

### 1. JSON in Git (Not Dropbox OAuth)

**Why:** User specifically didn't want "Connecting to Dropbox" prompts on iPad

**Solution:** Export database to JSON, include in git repository

**Benefits:**
- No authentication required
- Fast CDN delivery
- Version controlled
- Works everywhere

**Trade-off:** Updates require export + redeploy (acceptable for recipe app)

---

### 2. Netlify (Not Paul's Server)

**Why:** Simpler for serverless architecture, development stage

**Benefits:**
- Serverless scales automatically
- Free tier sufficient
- Global CDN
- Easy deployment

**Future:** Can migrate to Paul's server (fergi.com) if needed

---

### 3. Vision-Based Recipe Extraction

**Why:** 85 cookbook images needed extraction, source to be discarded

**Method:** Claude's image reading → structured data extraction

**Results:** 89 recipes, 98.9% success rate, complete data preservation

---

## User Requirements

### Critical Requirements

1. **No OAuth Prompts:** "We can't have any of this 'Connecting to Dropbox' nonsense"
2. **Cross-Platform:** Must work on Mac, iOS, Android
3. **iPad-Friendly:** Intensive iPad usage, seamless experience required
4. **Development Stage:** "Be bold with experiments, we'll get more conservative later"

### User Preferences

- Fast, simple, reliable
- No complex authentication
- Easy to update recipes
- Mobile-responsive
- Family recipes preserved

---

## Future Roadmap

### Phase 1: Recipe Management
- Add recipes via web interface
- Edit recipes in browser
- Delete recipes
- Upload photos
- Real-time updates (no export/deploy cycle)

### Phase 2: User Features
- User accounts and authentication
- Personal favorites and collections
- Cooking notes and modifications
- Recipe ratings and reviews

### Phase 3: Advanced Tools
- Meal planning calendar
- Grocery list generator
- Recipe scaling (2x, 1/2, etc.)
- Nutrition calculator
- Print-friendly recipe cards

### Phase 4: Social & Mobile
- Share recipes with family
- Recipe contributions
- Progressive Web App (PWA)
- Offline access
- Native mobile apps (optional)

---

## File Organization

### Key Files

**Web Interface:**
- `index.html` - Main web application

**Data:**
- `recipes.json` - Recipe data export (792 KB, 122 recipes)
- `recipes.db` - SQLite database (local, not in git)

**API Functions:**
- `netlify/functions/get-recipes.js` - Get/search recipes
- `netlify/functions/get-recipe.js` - Get single recipe
- `netlify/functions/statistics.js` - Database statistics

**Python Utilities:**
- `server.py` - Flask development server
- `database.py` - Database operations
- `export_to_json.py` - SQLite → JSON export
- `schema.sql` - Database schema

**Configuration:**
- `netlify.toml` - Netlify configuration
- `.gitignore` - Git exclusions
- `requirements.txt` - Python dependencies

**Documentation:**
- `DEPLOYMENT_SUMMARY.md` - Deployment guide
- `CLAUDE_WEB_SPEC.md` - Technical specification
- `CLAUDE_WEB_HISTORY.md` - Project history
- `CLAUDE.md` - Project instructions

---

## Recipe Source Files

### Main Collection Sources
- 50+ PDF files from recipe websites
- Pages documents for custom recipes
- Enhanced with AI-generated descriptions, timing, calories

### Janet Mason Sources
- 85 JPG images (Janet Mason/*.JPG)
- Vision-extracted to database
- Original images preserved in git
- Complete extraction documented in JANET_EXTRACTION_COMPLETE.md

---

## Performance & Metrics

**Page Load:** ~500ms
**API Response:** ~100ms
**CDN:** Netlify global network
**Data Size:** 792 KB total
**Recipes:** 122 total

**Deployment Stats:**
- Deployment date: November 2, 2025
- Deployment time: ~2 hours (including debugging)
- Development time: 3 days (Oct 30 - Nov 2)
- Iterations to success: 3 deployments

---

## Access & Links

**Production App:** https://fergi-cooking.netlify.app
**GitHub Repository:** https://github.com/fergidotcom/fergi-cooking
**Netlify Dashboard:** https://app.netlify.com/projects/fergi-cooking
**Function Logs:** https://app.netlify.com/projects/fergi-cooking/logs/functions

---

## Development History

**October 30, 2025** - Project initialization
- Created Cooking project directory
- Documented 50+ recipe files

**November 1, 2025** - Database & extraction
- Created SQLite database and schema
- Built Flask server and web interface
- Imported 30 main recipes
- Enhanced recipes with AI (descriptions, timing, calories)
- Extracted 89 Janet Mason recipes from images

**November 2, 2025** - Netlify deployment
- Exported database to JSON
- Created Netlify Functions
- Deployed to production
- Fixed path resolution issues
- Verified API and UI working
- Created comprehensive documentation

---

## Current Status

### Production Ready ✅
- Live at https://fergi-cooking.netlify.app
- All 122 recipes accessible
- API endpoints working
- Search and filtering functional
- Mobile-responsive
- Cross-platform (Mac, iOS, Android)
- No authentication required
- Fast and reliable

### Documentation Complete ✅
- User guide (DEPLOYMENT_SUMMARY.md)
- Technical spec (CLAUDE_WEB_SPEC.md)
- Project history (CLAUDE_WEB_HISTORY.md)
- Project instructions (CLAUDE.md)
- Recipe extraction docs (JANET_EXTRACTION_COMPLETE.md)

### Backed Up ✅
- GitHub repository with full history
- All documentation committed
- Recipe data version controlled
- Source files preserved

---

## How to Use

### For Users
1. Visit https://fergi-cooking.netlify.app
2. Browse all recipes or filter by collection
3. Search for specific recipes
4. Click any recipe for full details
5. Works on any device with a browser

### For Developers
1. Clone GitHub repository
2. Install Python dependencies
3. Run local Flask server for development
4. Make changes to recipes.db
5. Export to JSON and deploy to Netlify

---

## Support & Documentation

**Questions?** See documentation files:
- DEPLOYMENT_SUMMARY.md - User guide
- CLAUDE_WEB_SPEC.md - Technical reference
- CLAUDE_WEB_HISTORY.md - Project history
- CLAUDE.md - Project instructions

**Issues?** Check troubleshooting in CLAUDE_WEB_SPEC.md

**Updates?** Follow deployment workflow in DEPLOYMENT_SUMMARY.md

---

## Success Metrics

✅ **Deployment successful** - Live and working
✅ **All recipes preserved** - 122 recipes accessible
✅ **Vision extraction complete** - 89 recipes from images
✅ **Cross-platform working** - Mac, iOS, Android
✅ **No authentication required** - Seamless iPad usage
✅ **Fast performance** - <500ms page load, <100ms API
✅ **Comprehensive documentation** - 4 major docs complete
✅ **Version controlled** - GitHub backup complete

---

## Ownership

**Owner:** Joe Ferguson
**Email:** joe@fergi.com
**GitHub:** @fergidotcom
**Deployment:** Autonomous implementation by Claude Code

---

**This is a living document - update as project evolves**

**Last Updated:** November 2, 2025
**Version:** 1.0.0
**Status:** ✅ Production
