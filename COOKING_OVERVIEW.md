# COOKING PROJECT OVERVIEW

**Project Name:** Fergi's Recipe Collection
**Project Type:** Personal Recipe Database & Management System
**Status:** Active Development
**Version:** 1.5 (Enhanced)
**Last Updated:** November 1, 2025

---

## Purpose

A comprehensive personal recipe collection and management system for organizing, searching, and managing family recipes and cooking resources. Provides a web-based interface for browsing recipes with detailed timing, nutritional information, and enhanced cooking instructions that include ingredient quantities inline.

**Key Value Proposition:** Eliminates the need to constantly refer back to ingredients while cooking by including quantities directly in instruction steps.

---

## Current Architecture

### Technology Stack

**Backend:**
- Python 3.x
- Flask web framework
- Flask-CORS for API access
- SQLite database

**Frontend:**
- Single-page HTML/CSS/JavaScript application
- No framework dependencies (vanilla JS)
- Responsive design with CSS Grid/Flexbox

**Data Processing:**
- PDF extraction tools (PyPDF2/pdfplumber)
- Python scripts for recipe import and enhancement
- SQLite for structured data storage

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Web Browser                        │
│              (Safari/Chrome/Firefox)                 │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP Requests
                   ▼
┌─────────────────────────────────────────────────────┐
│              Flask Web Server                        │
│              (server.py:5000)                        │
│  ┌──────────────────────────────────────────────┐  │
│  │   REST API Endpoints                         │  │
│  │   /api/recipes, /api/recipes/:id             │  │
│  │   /api/search, /api/statistics               │  │
│  └──────────────┬───────────────────────────────┘  │
└─────────────────┼───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│            Database Layer                            │
│            (database.py)                             │
│  ┌──────────────────────────────────────────────┐  │
│  │  RecipeDatabase class                        │  │
│  │  - CRUD operations                           │  │
│  │  - Search functionality                      │  │
│  │  - Statistics generation                     │  │
│  └──────────────┬───────────────────────────────┘  │
└─────────────────┼───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│              SQLite Database                         │
│              (recipes.db)                            │
│  ┌──────────────────────────────────────────────┐  │
│  │  Tables: recipes, ingredients, instructions  │  │
│  │  136 total recipes (51 main + 85 Janet's)   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Key Objectives and Requirements

### Completed Objectives ✅
1. **Recipe Database** - Structured storage of 136 recipes
2. **Web Interface** - Browse and search recipes
3. **Recipe Import** - Extract from PDFs and manual entry
4. **Enhanced Descriptions** - Professional, informative descriptions for all main recipes
5. **Timing Information** - Prep, cook, and total times
6. **Nutritional Data** - Calorie estimates per serving
7. **Inline Ingredient Quantities** - Instructions include amounts (no more flipping back!)
8. **Search Functionality** - Full-text search across recipes
9. **Favorites System** - Mark and filter favorite recipes
10. **Rating System** - 5-star rating for recipes

### In Progress 🔄
1. Recipe testing and refinement
2. Additional recipe imports
3. User feedback integration

### Planned Features 📋
1. **Meal Planning** - Weekly meal plan generator
2. **Shopping Lists** - Auto-generate from selected recipes
3. **Recipe Scaling** - Adjust ingredient quantities for servings
4. **Image Support** - Add photos to recipes
5. **Tags & Categories** - Advanced filtering (vegetarian, gluten-free, etc.)
6. **Export Features** - PDF/print-friendly formats
7. **Mobile App** - Native iOS/Android interface
8. **Recipe Sharing** - Share recipes with family
9. **Cooking Mode** - Step-by-step guided cooking interface
10. **Nutrition Tracking** - Detailed nutritional breakdown

---

## Implementation Status

### ✅ Built and Functional

**Database Schema:**
- `recipes` table - Core recipe metadata
- `ingredients` table - Recipe ingredients with quantities
- `instructions` table - Step-by-step cooking instructions
- All enhanced with timing, calories, descriptions

**API Endpoints:**
- `GET /api/recipes` - List all recipes
- `GET /api/recipes/:id` - Get single recipe with details
- `POST /api/recipes` - Create new recipe
- `PUT /api/recipes/:id` - Update recipe
- `DELETE /api/recipes/:id` - Delete recipe
- `GET /api/search?q=query` - Search recipes
- `GET /api/statistics` - Database statistics

**Web Interface Features:**
- Recipe grid with cards showing timing/calories
- Recipe detail modal with complete information
- Edit/delete functionality
- Search bar with live filtering
- Filter by source (Main recipes vs Janet's recipes)
- Filter by "Needs Review" status
- Favorites toggle
- Responsive design for all screen sizes

**Enhancement Scripts:**
- Recipe description generator (30 recipes enhanced)
- Instruction enhancement with inline quantities (37 steps enhanced)
- Calorie data importer
- PDF extraction tools
- Bulk import utilities

### 🔄 In Progress

**Data Quality:**
- 73 recipes marked "Needs Review" (mostly Janet's collection)
- Some recipes need title cleanup
- Some instructions need manual refinement

**Features:**
- Testing enhanced instructions during actual cooking
- Gathering feedback on descriptions and timing accuracy

### 📋 Planned

**Near-term:**
- Recipe testing and accuracy verification
- Image upload and display
- Print-friendly recipe cards
- Recipe duplication detection

**Long-term:**
- Mobile-responsive improvements
- Offline capability (PWA)
- Multi-user support (family sharing)
- Integration with grocery delivery services

---

## File Structure

```
Cooking/
├── CLAUDE.md                               # Project documentation for Claude
├── COOKING_OVERVIEW.md                     # This file
├── COOKING_CHANGELOG.md                    # Change log
├── RECIPE_ENHANCEMENT_SUMMARY.md           # Recent enhancement details
├── README.md                               # User-facing README
├── QUICKSTART.md                           # Quick start guide
├── PROJECT_SUMMARY.md                      # Project summary
├── DOCUMENTATION_INDEX.md                  # Documentation index
├── QUICK_REFERENCE.md                      # Quick reference
│
├── Core Application Files
├── server.py                               # Flask web server & REST API
├── database.py                             # Database operations layer
├── recipes.db                              # SQLite database (136 recipes)
├── index.html                              # Main web interface
├── index_backup.html                       # UI backup
├── schema.sql                              # Database schema definition
├── requirements.txt                        # Python dependencies
├── START_SERVER.sh                         # Server startup script
│
├── Recipe Processing Scripts
├── recipe_extractor.py                     # PDF recipe extraction
├── vision_recipe_extractor.py              # Vision-based extraction
├── import_recipes.py                       # Recipe import utilities
├── import_main_recipes.py                  # Main recipe imports
├── import_janet_recipes.py                 # Janet's recipe imports
├── cleanup_incomplete_recipes.py           # Data cleanup
├── enhance_all_recipes.py                  # Description/timing enhancement
├── enhance_instructions.py                 # Inline quantity enhancement
├── add_calories.py                         # Calorie data addition
├── analyze_and_enhance_recipes.py          # Analysis utilities
│
├── Recipe Source Files (PDFs & Pages)
├── [50+ PDF files]                         # Recipe PDFs from various sources
├── [Multiple .pages files]                 # Custom/modified recipes
├── Janet Mason/                            # Janet's recipe collection (85 recipes)
│   └── [85 PDF files]
│
└── Session Documentation
    ├── SESSION_NOTES.md                    # Development session notes
    ├── WELCOME.md                          # Welcome/intro
    └── UPDATED_WELCOME.md                  # Updated welcome

```

### Key Components

**server.py** (216 lines)
- Flask application setup
- REST API endpoint definitions
- Static file serving
- Error handling

**database.py** (detailed length unknown)
- `RecipeDatabase` class
- CRUD operations for recipes
- Search and filter methods
- Statistics generation

**index.html** (1,264 lines)
- Complete single-page application
- Recipe grid rendering
- Modal-based recipe detail view
- Edit forms with dynamic ingredient/instruction lists
- Search and filter UI
- Statistics dashboard

**recipes.db** (SQLite database)
- 136 total recipes
- 51 main recipes (enhanced)
- 85 Janet Mason recipes
- Full relational structure with ingredients and instructions

---

## Dependencies and Tools

### Python Dependencies (requirements.txt)

```
Flask==3.0.0
flask-cors==4.0.0
PyPDF2==3.0.1
pdfplumber==0.10.3
Pillow==10.1.0
```

### Development Tools

- **Python 3.x** - Runtime environment
- **SQLite 3** - Database (built-in to Python)
- **Any modern browser** - Chrome, Safari, Firefox for UI
- **Text editor** - For recipe editing and development

### Runtime Requirements

- **Operating System:** macOS (tested), Linux, Windows compatible
- **Python Version:** 3.8+
- **Disk Space:** ~100MB (for database and PDFs)
- **RAM:** Minimal (~50MB for Flask server)
- **Network:** Local only (127.0.0.1:5000)

---

## Development Setup Instructions

### Initial Setup

1. **Navigate to project directory:**
   ```bash
   cd ~/Library/CloudStorage/Dropbox/Fergi/Cooking
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Verify database exists:**
   ```bash
   ls -lh recipes.db
   # Should show ~490KB file
   ```

### Running the Application

**Option 1: Using the startup script**
```bash
bash START_SERVER.sh
```

**Option 2: Manual start**
```bash
python3 server.py
```

**Option 3: With custom port**
```bash
python3 server.py --port 8000
```

**Option 4: Debug mode**
```bash
python3 server.py --debug
```

### Accessing the Application

1. **Start the server** (see above)
2. **Open browser** to http://127.0.0.1:5000
3. **Browse recipes** - Main interface loads automatically

### Development Workflow

**Adding new recipes:**
```bash
# Place PDF in Cooking directory
python3 recipe_extractor.py "RecipeName.pdf"
# Or use web interface to manually add
```

**Updating database:**
```bash
sqlite3 recipes.db
# Run SQL commands
```

**Enhancing recipes:**
```bash
python3 enhance_all_recipes.py
python3 enhance_instructions.py
```

**Backup database:**
```bash
cp recipes.db recipes.db.backup-$(date +%Y%m%d)
```

---

## Infrastructure Details

### Deployment Configuration

**Current Status:** Local development only

**GitHub Repository:** ❌ Not currently under version control
- **Planned:** Initialize Git repository
- **Recommended repo name:** `fergi-cooking-recipes`
- **Branch structure:** `main` for stable, `dev` for development

**Netlify Deployment:** ❌ Not applicable
- Static frontend could be deployed to Netlify
- Would require backend API hosted separately

**Server Deployment:** ❌ Not currently deployed
- **Local only:** Runs on 127.0.0.1:5000
- **Potential deployment:** fergi.com/recipes (if deployed)
- **Requirements for deployment:**
  - WSGI server (Gunicorn/uWSGI)
  - Reverse proxy (nginx)
  - SSL certificate for HTTPS
  - Environment variable configuration

### Environment Variables

**Current:** None required (local development)

**For Production Deployment (future):**
```bash
# Flask configuration
FLASK_ENV=production
FLASK_SECRET_KEY=<random-secret-key>
FLASK_PORT=5000

# Database
DATABASE_PATH=/path/to/recipes.db

# CORS (if needed for external access)
CORS_ORIGINS=https://fergi.com

# Server
HOST=0.0.0.0
PORT=5000
```

### Configuration Files

**server.py configuration:**
- Default host: `127.0.0.1`
- Default port: `5000`
- Debug mode: `False` (use `--debug` flag for development)

**database.py configuration:**
- Database file: `recipes.db` (in current directory)
- No connection pooling (single-user application)

### Data Storage

**Location:** `/Users/joeferguson/Library/CloudStorage/Dropbox/Fergi/Cooking/`

**Dropbox Sync:** ✅ Active
- All files sync across devices via Dropbox
- Database changes sync automatically
- Recipe PDFs accessible from all devices

**Backup Strategy:**
- Dropbox provides automatic versioning
- Manual backups recommended before major changes
- Database exports to SQL for version control (planned)

### Security Considerations

**Current (Local Development):**
- ✅ Localhost only (not exposed to network)
- ✅ No authentication required
- ✅ No sensitive data in recipes

**For Production (Future):**
- ⚠️ Would need authentication
- ⚠️ HTTPS required
- ⚠️ Rate limiting for API
- ⚠️ Input validation and sanitization
- ⚠️ CORS configuration for allowed origins

---

## Known Issues and Technical Debt

### Current Issues

1. **Recipe Titles Need Cleanup**
   - 73 recipes marked "NEEDS TITLE"
   - Mostly from Janet Mason collection
   - Impact: Poor searchability and display

2. **Instruction Enhancement Incomplete**
   - 37 out of 52 instructions enhanced (71%)
   - Some ingredient references not matched
   - Some inline quantities may be verbose

3. **Missing Images**
   - No recipe photos currently
   - Database schema doesn't include image support
   - Impact: Less visually appealing interface

4. **No Version Control**
   - Not in Git repository
   - Change tracking via Dropbox only
   - Collaboration difficult

5. **Single User Only**
   - No multi-user support
   - No authentication system
   - Can't share with family members remotely

### Technical Debt

1. **Frontend Framework**
   - Vanilla JavaScript becoming complex
   - Would benefit from React/Vue for better state management
   - Current code is maintainable but not scalable

2. **Database Migrations**
   - No migration system (Alembic, etc.)
   - Schema changes done manually
   - Risk of data inconsistency

3. **API Documentation**
   - No OpenAPI/Swagger documentation
   - Endpoints documented only in code comments
   - Makes integration difficult

4. **Testing**
   - No automated tests
   - No unit tests for database operations
   - No integration tests for API
   - Manual testing only

5. **Error Handling**
   - Basic error handling in API
   - No comprehensive logging system
   - Errors shown as simple alerts

6. **Performance**
   - No pagination for recipe list
   - Full database load on each request
   - Acceptable for 136 recipes, won't scale to thousands

7. **Mobile Experience**
   - Responsive but not optimized for mobile
   - No PWA features (offline support, install prompt)
   - Small touch targets in some areas

### Planned Improvements

**High Priority:**
1. Initialize Git repository
2. Clean up recipe titles (73 recipes)
3. Add image upload support
4. Implement automated backups

**Medium Priority:**
5. Add unit tests for database operations
6. Implement API documentation (Swagger)
7. Add pagination for recipe list
8. Improve mobile experience

**Low Priority:**
9. Consider frontend framework migration
10. Add multi-user support
11. Implement advanced search features
12. Add recipe import from websites

---

## Related Projects

**Reference Refinement** (`~/Library/CloudStorage/Dropbox/Fergi/AI Wrangling/References`)
- Similar document management challenges
- Could share search/indexing technology
- Both deal with organizing large document collections

**Ferguson Family Archive** (`~/Library/CloudStorage/Dropbox/Fergi/Ferguson Family Archive`)
- Family history and documentation
- Recipe collection is part of family heritage
- Potential integration for historical family recipes

**FergiDotCom** (`~/Library/CloudStorage/Dropbox/Fergi/FergiDotCom`)
- Meta-project for orchestrating all Claude Code projects
- Cooking project is one of the managed sub-projects

---

## Project Context

This is one of four active Claude Code projects in the Fergi workspace:

1. **FergiDotCom** - Meta-project orchestration
2. **Reference Refinement** - Academic reference management (production)
3. **Cooking** - Recipe collection (this project)
4. **Ferguson Family Archive** - Family history documentation

All projects share the Fergi workspace root and use the project switcher utility for easy navigation.

---

## Contact & Maintenance

**Project Owner:** Joe Ferguson
**Maintained by:** Claude Code sessions
**Primary Use:** Personal recipe collection and cooking reference
**Update Frequency:** Active development, multiple sessions per week

**For questions or issues:**
- Review this documentation
- Check SESSION_NOTES.md for recent changes
- Consult RECIPE_ENHANCEMENT_SUMMARY.md for enhancement details

---

**Last Updated:** November 1, 2025
**Document Version:** 1.0
**Project Version:** 1.5 (Enhanced)
