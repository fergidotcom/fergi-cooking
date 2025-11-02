# Fergi's Recipe Collection - Database & Web Interface

A comprehensive recipe management system that extracts, indexes, and provides a beautiful web interface for your recipe collection.

## Features

✨ **Complete Recipe Management**
- Extract recipes from PDFs, Apple Pages documents, and images (via OCR)
- Normalized SQLite database with full-text search
- Beautiful, responsive web interface
- Full CRUD operations (Create, Read, Update, Delete)
- Edit any aspect of recipes directly in the browser

🔍 **Smart Extraction**
- Automatic source attribution detection
- Recipe parsing (ingredients, instructions, times, servings)
- Filename-based metadata extraction
- Support for Janet Mason collection with automatic attribution

📊 **Features**
- Search across titles, descriptions, ingredients, instructions
- Filter by source, cuisine, meal type
- Mark recipes as favorites
- Rate recipes (1-5 stars)
- Track dietary preferences (vegetarian, vegan, gluten-free, etc.)
- View statistics dashboard

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Web Interface (HTML/CSS/JS)              │
│  - Recipe browsing & search                                  │
│  - Full editing capabilities                                 │
│  - Statistics dashboard                                      │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                  Flask REST API (server.py)                  │
│  - /api/recipes - List/search recipes                        │
│  - /api/recipes/<id> - Get/update/delete recipe             │
│  - /api/statistics - Database stats                          │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│              Database Layer (database.py)                    │
│  - SQLite database with normalized schema                   │
│  - Full-text search support                                  │
│  - CRUD operations                                           │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│        Recipe Extraction (recipe_extractor.py)               │
│  - PDF text extraction (PyPDF2, pdfplumber)                 │
│  - Image OCR (Tesseract)                                     │
│  - Pages document conversion                                 │
│  - Recipe parsing & metadata extraction                      │
└─────────────────────────────────────────────────────────────┘
```

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Tesseract OCR** (for image extraction)

Install Tesseract on macOS:
```bash
brew install tesseract
```

### Setup

1. **Install Python dependencies:**
```bash
pip3 install -r requirements.txt
```

Note: If you encounter issues with some packages, you can install the essentials:
```bash
pip3 install flask flask-cors PyPDF2 pdfplumber Pillow pytesseract
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

## API Endpoints

### GET /api/recipes
List all recipes (with optional pagination)
```bash
curl http://127.0.0.1:5000/api/recipes
curl http://127.0.0.1:5000/api/recipes?limit=10&offset=0
```

### GET /api/recipes/:id
Get single recipe with full details
```bash
curl http://127.0.0.1:5000/api/recipes/1
```

### POST /api/recipes
Create new recipe
```bash
curl -X POST http://127.0.0.1:5000/api/recipes \
  -H "Content-Type: application/json" \
  -d '{"title":"New Recipe","source_attribution":"Fergi",...}'
```

### PUT /api/recipes/:id
Update recipe
```bash
curl -X PUT http://127.0.0.1:5000/api/recipes/1 \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title",...}'
```

### DELETE /api/recipes/:id
Delete recipe
```bash
curl -X DELETE http://127.0.0.1:5000/api/recipes/1
```

### GET /api/search?q=query
Search recipes
```bash
curl http://127.0.0.1:5000/api/search?q=chicken
```

### GET /api/statistics
Get database statistics
```bash
curl http://127.0.0.1:5000/api/statistics
```

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
**Version:** 1.0
**Author:** Fergi (with Claude Code assistance)

Enjoy your organized recipe collection! 👨‍🍳
