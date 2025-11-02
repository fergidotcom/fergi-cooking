# Claude Web - Fergi Cooking App Specification

**Last Updated:** November 2, 2025
**Purpose:** Technical specification for Claude Web to understand and work with the Fergi Cooking App

---

## Project Overview

**Fergi Cooking App** is a recipe collection and management system deployed as a serverless web application.

- **Live URL:** https://fergi-cooking.netlify.app
- **GitHub:** https://github.com/fergidotcom/fergi-cooking
- **Total Recipes:** 122 (33 Main Collection + 89 Janet Mason's Cookbook)
- **Status:** Production - Live and working

---

## Architecture

### Deployment Platform: **Netlify**

**Type:** Static site with serverless functions (JAMstack architecture)

**Why Netlify:**
- No OAuth "Connecting to Dropbox" prompts (user requirement)
- Simple, fast, reliable CDN hosting
- Serverless functions for API
- Free tier sufficient for this use case
- Easy deployment workflow

### Technology Stack

**Frontend:**
- HTML/CSS/JavaScript (vanilla, no framework)
- Vue.js-style reactive pattern in index.html
- Mobile-responsive design
- Single Page Application (SPA)

**Backend:**
- Netlify Functions (Node.js serverless)
- Functions located in `netlify/functions/`
- No traditional server - stateless API

**Data Storage:**
- **Development:** SQLite database (`recipes.db`) in Dropbox
- **Production:** JSON export (`recipes.json`) in git repository
- **Export script:** `export_to_json.py` converts SQLite → JSON

**Version Control:**
- GitHub repository: fergidotcom/fergi-cooking
- Git user: Joe Ferguson <joe@fergi.com>

---

## File Structure

```
Cooking/
├── index.html                    # Main web interface
├── recipes.json                  # Recipe data (122 recipes, 792 KB)
├── netlify.toml                  # Netlify configuration
├── netlify/
│   └── functions/
│       ├── get-recipes.js        # Get all/search recipes API
│       ├── get-recipe.js         # Get single recipe by ID API
│       └── statistics.js         # Get database statistics API
├── export_to_json.py             # SQLite → JSON export script
├── recipes.db                    # Local SQLite database (not in git)
├── server.py                     # Flask dev server (local development only)
├── database.py                   # Database utilities (Python)
├── schema.sql                    # Database schema
├── .gitignore                    # Git exclusions
├── DEPLOYMENT_SUMMARY.md         # Deployment documentation
├── CLAUDE_WEB_SPEC.md            # This file - technical spec
├── CLAUDE_WEB_HISTORY.md         # Project history and context
├── CLAUDE.md                     # Claude Code project instructions
└── [Various Python scripts]      # Recipe extraction and enhancement scripts
```

**Recipe Source Files (in git, but not used in production):**
- `*.pdf` - Recipe PDFs from various sources
- `*.pages` - Recipe documents in Pages format
- `Janet Mason/*.JPG` - 85 cookbook images (extracted to database)

---

## API Endpoints

All API endpoints are Netlify Functions accessed via `/api/*` paths.

### GET /api/recipes
**Function:** `netlify/functions/get-recipes.js`

**Purpose:** Get all recipes with optional search/filter

**Query Parameters:**
- `search` (string) - Search in title, description, ingredients, instructions
- `limit` (number) - Limit number of results
- `offset` (number) - Pagination offset

**Response:**
```json
{
  "success": true,
  "count": 122,
  "total": 122,
  "recipes": [
    {
      "id": 1,
      "title": "Recipe Title",
      "description": "Recipe description",
      "prep_time_minutes": 15,
      "cook_time_minutes": 30,
      "total_time_minutes": 45,
      "servings": "4",
      "calories_per_serving": 350,
      "cuisine_type": "Italian",
      "meal_type": "Dinner",
      "source_attribution": "NYT Cooking",
      "rating": 5,
      "favorite": 0,
      "date_added": "2025-11-01 12:00:00",
      "date_modified": "2025-11-01 12:00:00"
    }
  ]
}
```

**Note:** Returns summary view (no ingredients/instructions in list)

---

### GET /api/recipes/:id
**Function:** `netlify/functions/get-recipe.js`

**Purpose:** Get single recipe with full details

**Path Parameter:**
- `id` (number) - Recipe ID

**Response:**
```json
{
  "success": true,
  "recipe": {
    "id": 1,
    "title": "Recipe Title",
    "description": "Full description",
    "ingredients": [
      {
        "id": 1,
        "recipe_id": 1,
        "ingredient_order": 1,
        "quantity": "2",
        "unit": "cups",
        "ingredient_name": "flour",
        "preparation": "sifted",
        "ingredient_group": null
      }
    ],
    "instructions": [
      {
        "id": 1,
        "recipe_id": 1,
        "step_number": 1,
        "instruction_text": "Preheat oven to 350°F",
        "instruction_group": null
      }
    ],
    "tags": ["vegetarian", "easy"],
    "images": []
  }
}
```

**Note:** Returns complete recipe with ingredients, instructions, tags, images

---

### GET /api/statistics
**Function:** `netlify/functions/statistics.js`

**Purpose:** Get database statistics

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total_recipes": 122,
    "by_source": [
      {"source_attribution": "Janet Mason Cookbook", "count": 89},
      {"source_attribution": "NYT Cooking", "count": 15}
    ],
    "by_cuisine": [
      {"cuisine_type": "Italian", "count": 20},
      {"cuisine_type": "American", "count": 35}
    ],
    "favorites": 8,
    "janet_recipes": 89,
    "main_recipes": 33
  }
}
```

---

## Database Schema

### SQLite Schema (recipes.db)

**Primary Tables:**

1. **recipes** - Main recipe information
   - id (INTEGER PRIMARY KEY)
   - title (TEXT NOT NULL)
   - description (TEXT)
   - prep_time_minutes (INTEGER)
   - cook_time_minutes (INTEGER)
   - total_time_minutes (INTEGER)
   - servings (TEXT)
   - calories_per_serving (INTEGER)
   - difficulty (TEXT)
   - cuisine_type (TEXT)
   - meal_type (TEXT)
   - source_attribution (TEXT)
   - source_url (TEXT)
   - original_filename (TEXT)
   - file_path (TEXT)
   - notes (TEXT)
   - rating (INTEGER)
   - favorite (INTEGER DEFAULT 0)
   - vegetarian (INTEGER DEFAULT 0)
   - vegan (INTEGER DEFAULT 0)
   - gluten_free (INTEGER DEFAULT 0)
   - dairy_free (INTEGER DEFAULT 0)
   - date_added (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
   - date_modified (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)

2. **ingredients** - Recipe ingredients
   - id (INTEGER PRIMARY KEY)
   - recipe_id (INTEGER FOREIGN KEY)
   - ingredient_order (INTEGER)
   - quantity (TEXT)
   - unit (TEXT)
   - ingredient_name (TEXT NOT NULL)
   - preparation (TEXT)
   - ingredient_group (TEXT)

3. **instructions** - Step-by-step instructions
   - id (INTEGER PRIMARY KEY)
   - recipe_id (INTEGER FOREIGN KEY)
   - step_number (INTEGER NOT NULL)
   - instruction_text (TEXT NOT NULL)
   - instruction_group (TEXT)

4. **tags** - Recipe tags/categories
   - id (INTEGER PRIMARY KEY)
   - tag_name (TEXT UNIQUE NOT NULL)

5. **recipe_tags** - Many-to-many relationship
   - recipe_id (INTEGER FOREIGN KEY)
   - tag_id (INTEGER FOREIGN KEY)

6. **recipe_images** - Recipe images
   - id (INTEGER PRIMARY KEY)
   - recipe_id (INTEGER FOREIGN KEY)
   - image_path (TEXT NOT NULL)
   - image_type (TEXT)
   - display_order (INTEGER DEFAULT 0)

---

## Configuration Files

### netlify.toml

```toml
[build]
  publish = "."
  functions = "netlify/functions"

[functions]
  included_files = ["recipes.json"]

[[redirects]]
  from = "/api/recipes/:id"
  to = "/.netlify/functions/get-recipe/:id"
  status = 200

[[redirects]]
  from = "/api/recipes"
  to = "/.netlify/functions/get-recipes"
  status = 200

[[redirects]]
  from = "/api/statistics"
  to = "/.netlify/functions/statistics"
  status = 200

[[redirects]]
  from = "/api/search"
  to = "/.netlify/functions/get-recipes"
  status = 200

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, POST, PUT, DELETE, OPTIONS"
    Access-Control-Allow-Headers = "Content-Type"
```

**Key Configuration:**
- `included_files = ["recipes.json"]` - Bundles recipes.json with functions
- API redirects map `/api/*` to Netlify Functions
- SPA fallback serves index.html for all routes
- CORS headers enabled for API endpoints

---

### .gitignore

**Excluded from git:**
- `recipes.db` - SQLite database (keep in Dropbox, export to JSON for deployment)
- `recipes.db-journal` - SQLite journal file
- `.netlify/` - Netlify build artifacts
- `__pycache__/` - Python bytecode
- `.env` - Environment variables
- `*.log` - Log files
- `.DS_Store` - Mac metadata
- `*.mp4`, `*.mov`, `*.avi` - Large video files

**Included in git:**
- `recipes.json` - Recipe data export (792 KB)
- `*.pdf`, `*.pages` - Recipe source files (already committed)
- `Janet Mason/*.JPG` - Cookbook images (already committed)
- All Python scripts and utilities

---

## Recipe Collections

### Main Collection (33 recipes)
**Source Attribution:** Various (NYT Cooking, Epicurious, custom)

**Examples:**
- Beef Bourguignon (multiple variants)
- Meatloaf recipes (Joe's, Laura's, Irene's)
- Vegetarian dishes (Korma, Eggplant Parm, Portobello Stroganoff)
- Pasta dishes (Fettuccine Alfredo, Lasagna, Primavera)
- Specialty items (Jerk Chicken, French Onion Soup, Curries)

**Characteristics:**
- Sourced from recipe PDFs and Pages documents
- Enhanced with AI-generated descriptions and timing
- Calorie estimates added
- Ingredient quantities integrated into instructions

---

### Janet Mason's Cookbook (89 recipes)
**Source Attribution:** "Janet Mason Cookbook" (with variants)

**Extraction Source:** 85 cookbook images (IMG_8111.JPG through IMG_8195.JPG)

**Categories:**
- Appetizers & Snacks (12 recipes)
- Soups (12 recipes)
- Salads & Dressings (15 recipes)
- Sauces (8 recipes)
- Breads & Baked Goods (20 recipes)
- Side Dishes (10 recipes)
- Main Dishes (8 recipes)
- Desserts & Breakfast (4 recipes)

**Extraction Method:**
- Vision-based extraction using Claude's image reading capabilities
- Processed in 9 batches
- 98.9% success rate (88/89 recipes extracted successfully)
- Complete ingredient lists, instructions, timing, and calorie estimates

**Note:** Original source images can be safely discarded - all data extracted to database

---

## Deployment Workflow

### Initial Deployment (Completed)

1. **Export database to JSON:**
   ```bash
   python3 export_to_json.py
   ```

2. **Initialize git repository:**
   ```bash
   git init
   git add .gitignore netlify.toml index.html recipes.json netlify/
   git commit -m "Initial deployment"
   ```

3. **Create GitHub repository:**
   ```bash
   gh repo create fergi-cooking --public --source=. --remote=origin --push
   ```

4. **Deploy to Netlify:**
   ```bash
   netlify deploy --prod --dir=. --create-site fergi-cooking
   ```

### Updating Recipes

**When recipes are added/modified in SQLite database:**

1. **Export to JSON:**
   ```bash
   python3 export_to_json.py
   ```

2. **Commit and push:**
   ```bash
   git add recipes.json
   git commit -m "Updated recipes: [description]"
   git push origin main
   ```

3. **Deploy to Netlify:**
   ```bash
   netlify deploy --prod --dir=. --message="Recipe update"
   ```

**Alternative: Automatic deployment**
- Configure Netlify to auto-deploy on git push
- Settings → Build & deploy → Continuous deployment
- Connect to GitHub repository

---

## Local Development

### Requirements
- Python 3.x
- Flask and dependencies (`pip install -r requirements.txt`)
- SQLite3
- Netlify CLI (optional, for function testing)

### Running Local Server

**Option 1: Flask server (for development)**
```bash
python3 server.py --port 5001
```
Access at: http://127.0.0.1:5001

**Option 2: Netlify Dev (test functions locally)**
```bash
netlify dev
```
Access at: http://localhost:8888

### Database Operations

**Initialize database:**
```bash
python3 -c "from database import RecipeDatabase; RecipeDatabase().initialize_database()"
```

**Add recipe:**
```python
from database import RecipeDatabase
db = RecipeDatabase()
recipe_id = db.add_recipe({
    'title': 'Recipe Name',
    'description': 'Description',
    'ingredients': [...],
    'instructions': [...]
})
```

**Export to JSON:**
```bash
python3 export_to_json.py
```

---

## UI Features

### Main Interface (index.html)

**Navigation Buttons:**
- "All Recipes" - Show all 122 recipes
- "Main Collection" - Filter to 33 main recipes (excludes Janet's)
- "📖 Janet Mason's Cookbook" - Filter to 89 Janet recipes (purple button)
- "Needs Review" - Filter recipes needing review

**Filtering Logic:**
```javascript
// Main Collection: Exclude any recipe with "Janet" in source_attribution
mainRecipes = recipes.filter(r =>
  !r.source_attribution || !r.source_attribution.includes('Janet')
);

// Janet's Cookbook: Include any recipe with "Janet" in source_attribution
janetRecipes = recipes.filter(r =>
  r.source_attribution && r.source_attribution.includes('Janet')
);
```

**Search:**
- Real-time search across title, description, ingredients, instructions
- Case-insensitive
- Powered by `/api/recipes?search=query`

**Recipe Cards:**
- Display title, prep time, cook time, calories, servings
- Show cuisine type and source attribution tags
- Star ratings (if available)
- Click to view full recipe details

**Recipe Modal:**
- Full recipe details
- Complete ingredient list with quantities
- Step-by-step instructions
- Nutritional information
- Close with X button or click outside

---

## Important Implementation Details

### Netlify Function Path Resolution

**Issue:** Netlify Functions couldn't initially find recipes.json

**Solution:** Robust path resolution trying multiple locations:

```javascript
function loadRecipes() {
  if (recipesData) return recipesData;

  const possiblePaths = [
    path.join(__dirname, '../../recipes.json'),     // Local dev
    path.join(process.cwd(), 'recipes.json'),       // Netlify root
    '/var/task/recipes.json',                       // Netlify function root
    path.join(__dirname, '../../../recipes.json'),  // Parent directory
  ];

  for (const filepath of possiblePaths) {
    try {
      recipesData = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      console.log(`Loaded recipes from: ${filepath}`);
      return recipesData;
    } catch (e) {
      console.log(`Failed to load from ${filepath}: ${e.message}`);
    }
  }

  throw new Error('Could not find recipes.json in any known location');
}
```

**Configuration:** `netlify.toml` includes `included_files = ["recipes.json"]` to bundle with functions

---

### API URL Configuration

**index.html uses relative API URLs:**
```javascript
apiUrl: '/api'
```

**Redirects in netlify.toml map to functions:**
- `/api/recipes` → `/.netlify/functions/get-recipes`
- `/api/recipes/:id` → `/.netlify/functions/get-recipe/:id`
- `/api/statistics` → `/.netlify/functions/statistics`

This works in both local dev and production without URL changes.

---

## Python Utilities

### Key Scripts

**export_to_json.py**
- Exports recipes.db to recipes.json
- Includes all recipes, ingredients, instructions, tags, images
- Output: 122 recipes, ~792 KB JSON file

**database.py**
- RecipeDatabase class for all database operations
- Methods: add_recipe(), get_recipe(), get_all_recipes(), search_recipes(), update_recipe(), delete_recipe(), get_statistics()
- Uses sqlite3 with row_factory for dict results

**server.py**
- Flask development server
- REST API endpoints matching Netlify Functions
- CORS enabled
- For local development only (not used in production)

**Extraction Scripts:**
- `extract_batch_1.py` through `extract_batch_9_COMPLETION.py`
- Vision-based recipe extraction from Janet Mason cookbook images
- Each script processes 5-10 images
- Inserts structured recipe data into database

**Enhancement Scripts:**
- `enhance_all_recipes.py` - Add descriptions, timing, calories to existing recipes
- `enhance_instructions.py` - Integrate ingredient quantities into instructions
- `add_calories.py` - Add calorie estimates to recipes

---

## User Requirements & Constraints

### Critical Requirements

1. **No OAuth Prompts**
   - User specifically requested: "We can't have any of this 'Connecting to Dropbox' nonsense"
   - Solution: recipes.json in git repository, no Dropbox API integration
   - iPad app usage must be seamless with no connection prompts

2. **Cross-Platform Access**
   - Must work on Mac, iOS, Android
   - Solution: Web-based app accessible via browser
   - Can be added to home screen on mobile devices

3. **Development Stage**
   - User said: "be bold with your experiments"
   - "We will get more conservative later"
   - Rapid iteration and deployment encouraged

### Design Decisions

**Data Storage:** JSON in git repo (not Dropbox API)
- Simpler, faster, no authentication
- Easy to version control
- Small file size (792 KB) - perfect for git

**Deployment:** Netlify (not Paul's server)
- Serverless scales automatically
- Free tier sufficient
- Easy to migrate to Paul's server later if needed

**Frontend:** Vanilla JavaScript (no framework)
- Simple, fast, no build step
- Easy to understand and modify
- Works everywhere

---

## Testing & Verification

### Production Verification

**API Tests:**
```bash
# Get all recipes
curl https://fergi-cooking.netlify.app/api/recipes

# Search recipes
curl "https://fergi-cooking.netlify.app/api/recipes?search=chicken"

# Get single recipe
curl https://fergi-cooking.netlify.app/api/recipes/1

# Get statistics
curl https://fergi-cooking.netlify.app/api/statistics
```

**Results:**
- ✅ All endpoints return 200 OK
- ✅ 122 recipes accessible
- ✅ Search functionality working
- ✅ Fast response times (~100ms)

**Web Interface:**
- ✅ Loads correctly on desktop and mobile
- ✅ Recipe cards display properly
- ✅ Navigation buttons work
- ✅ Search filters results
- ✅ Recipe modal shows full details
- ✅ Mobile-responsive design

---

## Monitoring & Logs

### Netlify Dashboard
**URL:** https://app.netlify.com/projects/fergi-cooking

**Available:**
- Build logs
- Function logs
- Deploy history
- Analytics (if enabled)

### Function Logs
**URL:** https://app.netlify.com/projects/fergi-cooking/logs/functions

**Shows:**
- Path resolution attempts
- Recipe loading success/failure
- API request logs
- Error messages

---

## Future Enhancements

### Phase 1: User Features (Priority)
- [ ] Add recipes via web interface
- [ ] Edit recipes in browser
- [ ] Upload photos to recipes
- [ ] Rate and favorite recipes
- [ ] Add cooking notes

### Phase 2: Advanced Features
- [ ] Meal planning calendar
- [ ] Grocery list generator
- [ ] Recipe scaling (2x, 1/2, etc.)
- [ ] Nutrition calculator
- [ ] Print-friendly recipe cards
- [ ] Export to PDF

### Phase 3: Social Features
- [ ] Share recipes via link
- [ ] Recipe collections/cookbooks
- [ ] Family recipe contributions
- [ ] Comments on recipes

### Phase 4: Mobile Apps
- [ ] Progressive Web App (PWA)
- [ ] Offline access
- [ ] Native iOS app (optional)
- [ ] Native Android app (optional)

---

## Troubleshooting

### Common Issues

**Problem:** API returns 500 error
**Solution:** Check function logs for path resolution errors. Ensure recipes.json is included in deployment.

**Problem:** Recipes not displaying
**Solution:** Check browser console for API errors. Verify `/api/recipes` endpoint works.

**Problem:** Search not working
**Solution:** Check that search query parameter is being sent correctly. Verify API endpoint receives search param.

**Problem:** Recipe modal not opening
**Solution:** Check browser console for JavaScript errors. Verify recipe ID exists in database.

### Debug Mode

**Enable in index.html:**
```javascript
// Add to app object
debug: true
```

**View in browser console:**
- API requests and responses
- Filter operations
- Recipe loading status

---

## Security Considerations

### Current Implementation

**Public Access:**
- App is publicly accessible (no authentication)
- All recipes are public
- Read-only for users (no write operations in UI yet)

**API Security:**
- CORS enabled for all origins
- GET-only endpoints (no mutations)
- No sensitive data exposed
- No user accounts or authentication

**Future Considerations:**
- Add authentication for recipe editing
- Implement user accounts
- Add role-based access control
- Rate limiting for API endpoints

---

## Performance

### Current Metrics

**Page Load Time:** ~500ms
**API Response Time:** ~100ms
**Total Asset Size:** ~800 KB (mostly recipes.json)
**CDN:** Netlify global CDN

**Optimization Opportunities:**
- Implement pagination for recipe list
- Lazy load recipe details
- Compress images (when added)
- Cache API responses in browser

---

## Contacts & Links

**Production URL:** https://fergi-cooking.netlify.app
**GitHub Repository:** https://github.com/fergidotcom/fergi-cooking
**Netlify Dashboard:** https://app.netlify.com/projects/fergi-cooking
**Function Logs:** https://app.netlify.com/projects/fergi-cooking/logs/functions

**Owner:** Joe Ferguson
**Email:** joe@fergi.com
**GitHub:** @fergidotcom

---

**Document Version:** 1.0
**Last Updated:** November 2, 2025
**Maintained By:** Claude Code

---

## Quick Reference Commands

```bash
# Local development
python3 server.py --port 5001

# Export database
python3 export_to_json.py

# Deploy to Netlify
netlify deploy --prod --dir=. --message="Update description"

# Git operations
git add recipes.json
git commit -m "Updated recipes"
git push origin main

# View function logs
netlify logs:function get-recipes
```

---

**End of Specification**
