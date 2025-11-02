# Quick Start Guide - Recipe Collection System

## System Status: ✅ READY TO USE

Your recipe database system is **fully operational** and ready to use!

### What's Been Set Up

✅ **Database Created** - `recipes.db` with 136 recipes
- 51 recipes from main Cooking folder
- 85 recipes from Janet Mason folder
- All automatically attributed to correct sources

✅ **Web Server Running** - Flask server at http://127.0.0.1:5000
- REST API for programmatic access
- Beautiful web interface for browsing and editing

✅ **All Components Installed**
- Python packages (Flask, PDF extraction, OCR)
- Tesseract OCR for image processing
- Database with normalized schema

---

## Access Your Recipes NOW

### Open the Web Interface

**Simply open this URL in your browser:**

```
http://127.0.0.1:5000
```

Or click here if viewing in a browser: [Launch Recipe Collection](http://127.0.0.1:5000)

---

## What You Can Do

### Browse Recipes
- View all 136 recipes in a beautiful grid layout
- See recipe cards with source attribution
- Click any recipe to view full details

### Search & Filter
- Search by recipe name, ingredients, instructions
- Find recipes by source (Janet, Fergi, Epicurious, etc.)
- Filter by cuisine type (Italian, Indian, French, etc.)

### View Full Recipe Details
- Complete ingredient lists with quantities
- Step-by-step instructions
- Cooking times and serving sizes
- Source attribution

### Edit Any Recipe
- Click "Edit Recipe" button on any recipe
- Modify title, description, times, servings
- Add/remove/edit ingredients
- Add/remove/edit cooking instructions
- Change source attribution
- Add cooking notes

### Manage Favorites
- Mark recipes as favorites with ★ button
- Rate recipes 1-5 stars
- Add personal cooking notes

### View Statistics
- Click "Statistics" button in navigation
- See recipes by source
- See recipes by cuisine
- View favorite counts

---

## Current Recipe Breakdown

**Total Recipes: 136**

**By Source:**
- Janet: 85 recipes
- Unknown: 21 recipes
- Epicurious: 8 recipes
- Fergi: 7 recipes (your recipes!)
- NYT Cooking: 7 recipes
- Marty: 2 recipes
- Others: Various (Adrienne, Diane, Irene, Laura, Mike, Nancy)

**By Cuisine:**
- Italian: 7 recipes
- Indian: 6 recipes
- American: 5 recipes
- French: 4 recipes
- Caribbean: 1 recipe

---

## Server Management

### Check if Server is Running

```bash
curl http://127.0.0.1:5000/api/statistics
```

If you see JSON output, the server is running!

### Start the Server (if stopped)

```bash
cd ~/Library/CloudStorage/Dropbox/Fergi/Cooking
python3 server.py
```

The server will start at: http://127.0.0.1:5000

### Stop the Server

Press `Ctrl+C` in the terminal where server is running

Or find and kill the process:
```bash
ps aux | grep server.py
kill <process_id>
```

---

## Common Tasks

### Add a New Recipe File

1. Save the recipe file (PDF, Pages, or image) to the Cooking folder
2. Run the import:
   ```bash
   python3 import_recipes.py --file "NewRecipe.pdf"
   ```
3. Refresh the web interface

### Re-import All Recipes

If you want to start fresh:
```bash
rm recipes.db
python3 import_recipes.py
```

### Backup Your Database

```bash
cp recipes.db recipes_backup_$(date +%Y%m%d).db
```

### Search via API

```bash
curl "http://127.0.0.1:5000/api/search?q=chicken"
```

---

## Tips for Using the System

### Editing Janet Mason Recipes
The Janet Mason images have been OCR'd (text extracted from images). The extracted text may need cleaning up:
1. Click on any Janet recipe
2. Click "Edit Recipe"
3. Update the title (currently "IMG_XXXX")
4. Clean up ingredients and instructions
5. Save changes

### Recipe Titles
Many recipe titles were auto-generated from filenames. You can edit them to be more descriptive!

### Source Attribution
You are "Fergi" in the system. Change any recipe's source to "Fergi" to claim it as yours.

### Rating System
Rate recipes as you cook them (1-5 stars) to remember which ones you loved!

### Search Tips
- Search for ingredients: "chicken", "pasta", "garlic"
- Search for cooking methods: "baked", "fried", "roasted"
- Search for cuisine: "italian", "indian", "french"

---

## Keyboard Shortcuts (Web Interface)

- `Enter` in search box - Perform search
- Click recipe card - View details
- `Escape` (planned) - Close modals

---

## Files You Care About

| File | Purpose |
|------|---------|
| `recipes.db` | **Your recipe database** (BACK THIS UP!) |
| `index.html` | Web interface |
| `server.py` | Web server |
| `import_recipes.py` | Import new recipes |
| `README.md` | Full documentation |
| `QUICKSTART.md` | This file |

---

## What's Next?

### Immediate Actions
1. ✅ Open http://127.0.0.1:5000
2. ✅ Browse your recipes
3. ✅ Edit recipe titles and details
4. ⬜ Mark your favorites
5. ⬜ Rate recipes you've cooked

### Optional Enhancements
- Edit Janet Mason recipe titles (currently IMG_XXXX)
- Add cooking notes to recipes
- Rate recipes as you cook them
- Add tags for better organization
- Take photos of dishes and add to recipes

---

## Need Help?

### Check the Logs
If something isn't working, check the server output in the terminal

### Re-read Documentation
- `README.md` - Comprehensive documentation
- `CLAUDE.md` - Project overview

### Common Issues

**Can't connect to web interface?**
- Make sure server is running: `python3 server.py`
- Try: http://localhost:5000 instead of 127.0.0.1

**Search not working?**
- Check that recipes.db exists
- Try refreshing the page

**Edit not saving?**
- Check browser console for errors (F12)
- Make sure all required fields are filled

---

## System Architecture Summary

```
Recipe Files (PDF/Pages/Images)
         ↓
  [recipe_extractor.py]
    Extracts & Parses
         ↓
   [database.py]
  Stores in SQLite
         ↓
    [server.py]
   REST API Server
         ↓
   [index.html]
  Web Interface
         ↓
      YOU! 👨‍🍳
```

---

## Enjoy Your Recipe Collection!

You now have a professional-grade recipe management system with:
- 📚 136 recipes indexed and searchable
- 🔍 Full-text search
- ✏️ Complete editing capabilities
- 📊 Statistics and analytics
- ⭐ Favorites and ratings
- 🎨 Beautiful web interface

**Start cooking!** 👨‍🍳🍳

---

*Created: October 30, 2025*
*Status: Fully Operational*
*Next Session: Just run `python3 server.py` and open http://127.0.0.1:5000*
