# Fergi's Recipe Collection

A comprehensive recipe management system with mobile cooking mode, AI-powered import, event planning, and real-time Dropbox sync.

**Live at:** https://fergi-cooking.netlify.app
**Version:** 3.1.0 (November 2025)
**Database:** 122 recipes | 5 contributors
**Platform:** Netlify (serverless) + Dropbox (data storage)

## ✨ What's New in v3.1 (November 2025)

👨‍🍳 **Mobile Cooking Mode** - Dedicated interface with LARGE text (readable from 2 feet away!), ingredient checkboxes, big step numbers, and screen stays on while cooking. Perfect for Janet's kitchen! Try it: [cooking.html?recipe_id=5](https://fergi-cooking.netlify.app/cooking.html?recipe_id=5)

🔐 **Authentication Backend** - Optional passwordless email login for contributors (backend deployed, UI coming in Phase 2). Enables separate event management per contributor.

👥 **More Contributors** - Added Nancy, Lauren, and The Cooks. Now 5 contributors ready to create their own events.

See [CHANGELOG.md](CHANGELOG.md) for complete version history.

## ✨ What's in v3.0 (Previous Release)

🤖 **AI-Powered Recipe Import** - Upload PDFs, Word docs, or images, and let Claude AI format them into perfect recipes

👥 **Contributor Management** - Track who contributed each recipe, filter by contributor, see statistics

📅 **Event Planning** - Create cooking events, assign recipes, collect guest preferences via public response page

💾 **Dropbox Migration** - All data in Dropbox for instant updates without redeployment

---

## 🎯 Features (v3.1.0)

### 🤖 AI-Powered Recipe Import
- **4-step wizard** for guided recipe entry
- **File upload support:** PDF, Word (.docx), Images (OCR), Plain Text
- **AI formatting** via Claude Sonnet 4 API
- **Text paste option** for quick entry
- **Live preview** with edit capability
- **Auto-save to Dropbox** (no redeployment needed)

### 👥 Contributor Management
- **Public system** (no authentication required)
- **Add/remove contributors** with validation
- **Filter recipes by contributor**
- **Statistics dashboard** with contributor breakdown
- **Auto-assignment:** 85 Janet Mason recipes, 37 Fergi recipes

### 📅 Event Planning
- **Create cooking events** with date/time/location
- **Assign recipes** to events
- **Guest preference collection** (public response page)
- **Email generation** with multiple copy methods
- **Dietary restrictions tracking**
- **Volunteer categories** (appetizers, mains, desserts, etc.)

### 🔍 Recipe Browsing & Search
- **Full-text search** across all fields
- **Filter by contributor, source, cuisine, meal type**
- **Beautiful card-based grid** display
- **Responsive design** for mobile
- **👨‍🍳 Cooking Mode (NEW v3.1)** - Mobile-first cooking interface with:
  - LARGE text (18-28px) readable from 2 feet away
  - Big step numbers in colored circles
  - Ingredient checkboxes to mark off as you use them
  - Wake Lock API - screen stays on while cooking!
  - Perfect for glancing at while stirring pots
- **Two-column print layout** (ingredients left, instructions right)
- **Statistics dashboard** with counts and breakdowns

### 🔐 Optional Authentication (Backend Ready - v3.1)
- **Passwordless email verification** - 6-digit codes (no passwords!)
- **Optional login** for contributors to establish identity
- **Separate event management** per contributor (Phase 2)
- **Backend deployed** - UI coming in next release
- **Philosophy:** "These are recipes, not state secrets!" - Zero friction

### 💾 Real-Time Dropbox Sync
- **Single source of truth:** All data in Dropbox
- **No redeployment needed** for data updates
- **Auto-refresh OAuth tokens**
- **Shared data folder** with Reference Refinement app
- **Instant updates** across all devices

## 🏗️ System Architecture (v3.1)

### Serverless + Dropbox Architecture
```
┌──────────────────────────────────────────────────────────────┐
│        Web Interface (fergi-cooking.netlify.app)             │
│  - Static HTML/CSS/JS hosted on Netlify CDN                  │
│  - Mobile cooking mode (cooking.html) ⭐ NEW v3.1            │
│  - Recipe import wizard (add-recipe.html)                    │
│  - Event management (events.html, event-detail.html)         │
│  - Guest responses (respond.html - public, no auth)          │
│  - Recipe browsing (index.html)                              │
└──────────────────────────────────────────────────────────────┘
                              ↕ API Calls
┌──────────────────────────────────────────────────────────────┐
│           Netlify Functions (19 serverless APIs)             │
│  + send-verification-code.js, verify-code.js ⭐ NEW v3.1    │
│  Recipe: get-recipes, get-recipe, add-recipe, update-recipe  │
│  Contributors: manage-contributors (CRUD)                    │
│  Events: create-event, get-events, save-events               │
│  Import: extract-file, format-recipe (Claude API)            │
│  Utility: load-recipes, save-recipes, record-selection       │
│  Helper: lib/dropbox-auth (OAuth with auto-refresh)          │
└──────────────────────────────────────────────────────────────┘
                              ↕ Dropbox API
┌──────────────────────────────────────────────────────────────┐
│         Dropbox Storage (/Apps/Reference Refinement/)        │
│  - recipes.json (122 recipes, 548KB)                         │
│  - contributors.json (8 contributors)                        │
│  - events.json (cooking events)                              │
│  - guest-selections.json (guest responses)                   │
│  SINGLE SOURCE OF TRUTH - No redeployment needed!            │
└──────────────────────────────────────────────────────────────┘
                              ↕ Dropbox Sync
┌──────────────────────────────────────────────────────────────┐
│         Your Mac (~/Dropbox/Apps/Reference Refinement/)      │
│  - Auto-synced local copies of all JSON files                │
│  - recipes.db (SQLite - legacy, for local querying)          │
└──────────────────────────────────────────────────────────────┘

                    ┌─────────────────────┐
                    │  Claude Sonnet 4 API │
                    │  (Recipe Formatting) │
                    └─────────────────────┘
```

### Key Benefits
✅ **Zero-downtime updates** - Data changes don't require redeployment
✅ **Real-time sync** - All devices see changes instantly via Dropbox
✅ **Scalable** - Netlify Functions auto-scale to demand
✅ **Cost-effective** - Free tier covers typical usage
✅ **Shared storage** - Same Dropbox folder as Reference Refinement app

## 🚀 Quick Start

### For Users (Just Browse Recipes)
Visit **https://fergi-cooking.netlify.app** - no installation required!

### For Contributors (Add Recipes)
1. Visit https://fergi-cooking.netlify.app
2. Click **"+ Add Recipe"**
3. Follow the 4-step wizard:
   - Upload file or paste text
   - Select contributor (or add new)
   - Let AI format the recipe
   - Review and save
4. Done! Recipe appears instantly.

### For Developers (Local Development)

#### Prerequisites
1. **Node.js** (for Netlify CLI)
2. **Netlify CLI**: `npm install -g netlify-cli`
3. **Netlify account** and site linked

#### Local Development
```bash
# Clone repository
cd ~/path/to/Cooking

# Install dependencies (if needed)
npm install

# Start local dev server (includes functions)
netlify dev
# Opens at http://localhost:8888

# Deploy to production
netlify deploy --prod --dir="." --message="Your changes"
```

### For Data Management (Legacy Local Tools)

The legacy Python tools are still available for batch operations:

#### Prerequisites
1. **Python 3.8+**
2. **Tesseract OCR** (for image extraction)

```bash
brew install tesseract
pip3 install -r requirements.txt
```

## Usage

### Step 1: Import Recipes

Import all recipes from the current directory:
```bash
python3 import_recipes.py
```

This will:
- Scan all PDFs, Pages documents, and images
- Extract recipe content using PDF parsing and OCR
- Parse ingredients and instructions
- Detect source attribution
- Populate the SQLite database
- Special handling for "Janet Mason" folder (attributed to Janet)

Import a single file:
```bash
python3 import_recipes.py --file "Beef Bourguignon Joe's Recipe.pdf"
```

Import with custom source:
```bash
python3 import_recipes.py --file "recipe.pdf" --source "Fergi"
```

### Step 2: Start the Web Server

```bash
python3 server.py
```

The server will start at: **http://127.0.0.1:5000**

Options:
```bash
python3 server.py --host 0.0.0.0 --port 8080 --debug
```

### Step 3: Access the Web Interface

Open your browser to: **http://127.0.0.1:5000**

## Web Interface Features

### Home View
- Grid display of all recipes
- Recipe cards showing title, source, cuisine, ratings
- Click any recipe to view full details

### Recipe Detail View
- Complete recipe information
- Ingredients with quantities
- Step-by-step instructions
- Metadata (times, servings, ratings, etc.)
- Edit, delete, and favorite buttons

### Edit Recipe
- Modify any field: title, description, times, servings
- Add/remove/edit ingredients
- Add/remove/edit instructions
- Change source attribution
- Update ratings and favorites
- Add cooking notes

### Search
- Full-text search across all fields
- Search by ingredient names
- Filter results in real-time

### Statistics Dashboard
- Total recipe count
- Recipes by source
- Recipes by cuisine
- Favorite recipe count

## Database Schema

### Tables

**recipes** - Main recipe information
- id, title, description, times, servings, difficulty
- cuisine_type, meal_type, source_attribution
- ratings, favorites, dietary flags

**ingredients** - Recipe ingredients
- recipe_id, order, quantity, unit, name, preparation

**instructions** - Cooking steps
- recipe_id, step_number, instruction_text

**tags** - Flexible categorization
- tag_name

**recipe_tags** - Many-to-many relationship

**cooking_log** - Cooking history and notes

**recipe_images** - Recipe photos

### Full-Text Search

SQLite FTS5 virtual table for fast searching across:
- Recipe titles
- Descriptions
- Ingredient names
- Instructions

## 🔌 API Endpoints (Netlify Functions)

All endpoints are serverless functions deployed at `/.netlify/functions/{function-name}`

### Recipe Management
```bash
# Get all recipes (with optional contributor filter)
GET /.netlify/functions/get-recipes
GET /.netlify/functions/get-recipes?contributor=Janet%20Mason

# Get single recipe
GET /.netlify/functions/get-recipe?id=1

# Add new recipe
POST /.netlify/functions/add-recipe
Body: { title, ingredients, instructions, contributor, ... }

# Update recipe
PUT /.netlify/functions/update-recipe?id=1
Body: { title, ingredients, ... }

# Load from Dropbox
GET /.netlify/functions/load-recipes

# Save to Dropbox
POST /.netlify/functions/save-recipes
Body: { recipes: [...] }
```

### Recipe Import (AI-Powered)
```bash
# Extract text from file (PDF, Word, Image, Text)
POST /.netlify/functions/extract-file
Body: multipart/form-data with file

# Format recipe with AI (Claude Sonnet 4)
POST /.netlify/functions/format-recipe
Body: { text: "raw recipe text" }
```

### Contributor Management
```bash
# Get all contributors
GET /.netlify/functions/manage-contributors

# Add contributor
POST /.netlify/functions/manage-contributors
Body: { name: "Contributor Name" }

# Remove contributor
DELETE /.netlify/functions/manage-contributors?name=Name
```

### Event Management
```bash
# Get all events
GET /.netlify/functions/get-events

# Create/update event
POST /.netlify/functions/create-event
Body: { name, date, time, location, description, guests: [...] }

# Save events to Dropbox
POST /.netlify/functions/save-events
Body: { events: [...] }

# Manage event recipes
POST /.netlify/functions/event-recipes
Body: { eventId, recipeId, action: "add|remove" }

# Record guest response
POST /.netlify/functions/record-selection
Body: { eventId, guestName, recipeId, selectionType, ... }

# Generate event email
POST /.netlify/functions/generate-email
Body: { eventId }
```

### Legacy Endpoints (Deprecated)
The old Flask API endpoints (`server.py`) are no longer used in production but remain available for local development.

## File Structure

```
Cooking/
├── CLAUDE.md                    # Project documentation
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── schema.sql                   # Database schema
├── database.py                  # Database operations
├── recipe_extractor.py          # Recipe extraction logic
├── import_recipes.py            # Batch import script
├── server.py                    # Flask web server
├── index.html                   # Web interface
├── recipes.db                   # SQLite database (created on import)
├── *.pdf                        # Recipe PDFs
├── *.pages                      # Recipe Pages documents
└── Janet Mason/                 # Janet's recipes (images)
    └── *.JPG                    # Scanned recipe pages
```

## Source Attribution

The system automatically detects sources from filenames:

- **Fergi** - Files with "Joe's", "Joes", or "Fergi" in the name
- **Janet** - All files in "Janet Mason" folder
- **NYT Cooking** - Files with "NYT" or "New York Times"
- **Epicurious** - Files with "Epicurious"
- **Named recipes** - Files with person names (Laura, Irene, Mike, etc.)

You can manually edit source attribution in the web interface.

## Tips & Best Practices

### For Best OCR Results
- Ensure images are clear and well-lit
- High-resolution images work best
- Text should be horizontal (not rotated)

### Recipe Organization
- Use consistent naming: `[Dish Name] [Source].pdf`
- Add metadata through web interface after import
- Use tags for flexible categorization
- Mark favorites and rate recipes as you cook them

### Backup
The entire database is in `recipes.db` - back it up regularly:
```bash
cp recipes.db recipes_backup_$(date +%Y%m%d).db
```

### Re-importing
To re-import all recipes (will create a new database):
```bash
rm recipes.db
python3 import_recipes.py
```

## Troubleshooting

### "Module not found" errors
Install missing dependencies:
```bash
pip3 install <module-name>
```

### OCR not working
Install Tesseract:
```bash
brew install tesseract
```

### Pages documents not extracting
Pages extraction uses macOS `textutil`. For best results, export Pages documents to PDF first.

### Database locked errors
Only one process can write to SQLite at a time. Close any database viewers before running imports.

### Web interface can't connect to API
Ensure the server is running on port 5000 and check CORS settings in `server.py`.

## Future Enhancements

Potential features to add:
- [ ] Meal planning tool
- [ ] Grocery list generator
- [ ] Recipe scaling calculator
- [ ] Print-friendly recipe view
- [ ] Export recipes to PDF
- [ ] Recipe sharing
- [ ] Nutrition information
- [ ] Cooking timers
- [ ] Recipe collections/cookbooks
- [ ] Photo upload for recipes
- [ ] Import from recipe websites
- [ ] Mobile app

## License

Personal use only. This is a family recipe collection management system.

## Support

For issues or questions:
1. Check this README
2. Review the CLAUDE.md file
3. Check the code comments
4. The system is designed to be self-documenting

---

**Created:** October 30, 2025
**Version:** 3.0.0
**Last Updated:** November 3, 2025
**Author:** Fergi (with Claude Code assistance)
**Live Site:** https://fergi-cooking.netlify.app

Enjoy your organized recipe collection! 👨‍🍳
