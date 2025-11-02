# Dropbox Integration Setup Guide

**Fergi Cooking now uses Dropbox as the single source of truth for recipes!**

## Overview

As of November 2, 2025, Fergi Cooking uses **Dropbox** to store `recipes.json`, just like Reference Refinement uses Dropbox for `decisions.txt`. This means:

✅ **Edits persist** - Changes made on the website are saved to Dropbox
✅ **Auto-sync to Mac** - Dropbox automatically syncs changes to your Mac
✅ **Single source of truth** - `/recipes.json` in Dropbox is the master copy
✅ **No manual harvest needed** - Changes appear on Mac via Dropbox sync
✅ **Works everywhere** - Access from any device with your Dropbox account

---

## Architecture

```
Website (https://fergi-cooking.netlify.app)
    ↓ OAuth Login
    ↓ Load/Save via Dropbox API
Dropbox: /recipes.json (MASTER)
    ↓ Auto-sync
Your Mac: ~/Library/CloudStorage/Dropbox/Fergi/Cooking/recipes.json (synced copy)
```

---

## Initial Setup (One-Time)

### Step 1: Upload recipes.json to Dropbox

You need to put the initial `recipes.json` file in your Dropbox so the website can load it.

**Option A: Via Python Script (Recommended)**
```bash
# Install dropbox package if needed
pip3 install dropbox

# Get a Dropbox access token:
# 1. Go to https://www.dropbox.com/developers/apps
# 2. Select the "Fergi Cooking" app (or create it)
# 3. Go to "Permissions" tab
# 4. Enable: files.content.write, files.content.read
# 5. Go to "Settings" tab, scroll to "Generated access token"
# 6. Click "Generate" and copy the token

# Run upload script
python3 upload_recipes_to_dropbox.py <YOUR_ACCESS_TOKEN>
```

**Option B: Manual Upload**
1. Log into dropbox.com
2. Upload `recipes.json` to the ROOT of your Dropbox (not in a folder)
3. Verify it's at `/recipes.json` (not `/Cooking/recipes.json`)

### Step 2: Visit the Website

1. Go to https://fergi-cooking.netlify.app
2. You'll see "Not connected to Dropbox"
3. Click "Connect Dropbox"
4. Log into your Dropbox account
5. Authorize the app
6. You'll be redirected back and recipes will load!

---

## How It Works

### When You Visit the Site:

1. **OAuth Check:** Site checks for saved Dropbox token in browser localStorage
2. **If Not Connected:** Shows "Connect Dropbox" button
3. **If Connected:** Loads `/recipes.json` from Dropbox
4. **Display:** Shows all 122 recipes

### When You Edit/Favorite/Delete:

1. **Change:** You click "Add to Favorites", "Delete Recipe", etc.
2. **Update Array:** Recipe is modified in the JavaScript array
3. **Save to Dropbox:** Entire `recipes.json` is uploaded to Dropbox
4. **Sync:** Dropbox automatically syncs the file to your Mac
5. **Result:** Change is permanent and appears on your Mac

---

## Key Differences from Old System

### Old System (API-based, Read-Only):
```
recipes.db (Mac) → export_to_json.py → recipes.json → Deploy → Netlify
                                                        ↓
                                                   Website (read-only)
```

**Problems:**
- Website edits didn't work
- Had to regenerate JSON and redeploy
- No way to save changes from website

### New System (Dropbox-based, Fully Editable):
```
                  ┌─ Edit on website ──→ Save to Dropbox ─┐
                  │                                        ↓
recipes.db (Mac) → export_to_json.py → Upload → Dropbox:/recipes.json ← Auto-sync
                                                         ↑
                                                    Website loads from here
```

**Benefits:**
- Website changes persist
- Auto-syncs to Mac
- No deploy needed for data changes
- Single source of truth

---

## Daily Workflow

### View and Edit Recipes:
1. Visit https://fergi-cooking.netlify.app
2. Browse, search, view recipes
3. Click "★ Favorites" to see favorites
4. Add/remove favorites (changes save immediately)
5. Edit recipes (coming soon - currently view-only)
6. Delete recipes (works now)

### Add New Recipes from PDFs:
1. **On Mac:** Add recipe to `recipes.db` using extraction scripts
2. **Export:** Run `python3 export_to_json.py`
3. **Check:** recipes.json updated on Mac
4. **Sync:** Dropbox automatically uploads to cloud
5. **Website:** Reload page - new recipe appears!

---

## Database Management

### recipes.db (SQLite - Mac only)
- **Location:** `~/Library/CloudStorage/Dropbox/Fergi/Cooking/recipes.db`
- **Purpose:** Source database for adding new recipes from PDFs
- **Export:** `python3 export_to_json.py` → creates recipes.json
- **Workflow:** Add new recipes here, then export

### recipes.json (JSON - Dropbox master)
- **Location:** Dropbox: `/recipes.json`
- **Purpose:** Master copy used by website
- **Synced to:** `~/Library/CloudStorage/Dropbox/Fergi/Cooking/recipes.json`
- **Changes:** Made via website OR by exporting from recipes.db

### Workflow Pattern:
```
New recipes from PDFs:
recipes.db → export → recipes.json → auto-upload → Dropbox

Edits/favorites from website:
Website → save → Dropbox → auto-sync → Mac

Best practice:
- Add new recipes via recipes.db
- Edit/favorite/organize via website
- Both paths update the same Dropbox file
```

---

## Features Now Available

✅ **OAuth Login:** Secure Dropbox authentication
✅ **Load from Dropbox:** All recipes loaded from `/recipes.json`
✅ **Save to Dropbox:** Changes written back immediately
✅ **Favorites Filter:** Click "★ Favorites" to see favorited recipes
✅ **Toggle Favorites:** Click heart icon to add/remove from favorites
✅ **Delete Recipes:** Delete button actually works now
✅ **Auto-sync:** All changes sync to Mac via Dropbox

---

## Troubleshooting

### "recipes.json not found in Dropbox"
**Solution:** Upload recipes.json to Dropbox root using setup script or manual upload

### "Not connected to Dropbox"
**Solution:** Click "Connect Dropbox" button and authorize

### "OAuth failed"
**Solution:** Check that DROPBOX_APP_SECRET is set in Netlify environment variables
```bash
netlify env:list | grep DROPBOX
```

### Changes don't appear on Mac
**Solution:**
- Check Dropbox is running on Mac
- Verify `/recipes.json` exists in Dropbox web interface
- Check Dropbox sync status

### Website shows old recipes
**Solution:**
- Hard refresh browser (Cmd+Shift+R or Ctrl+Shift+R)
- Clear browser cache
- Disconnect and reconnect Dropbox

---

## Security

- **OAuth tokens** stored in browser localStorage
- **Dropbox app** has limited permissions (only file access)
- **No passwords** stored in code or website
- **HTTPS only** - all connections encrypted
- **Token refresh** handled automatically by Dropbox SDK

---

## Backups

Your recipes are safe because:

1. **Dropbox** maintains version history (30-day retention)
2. **Mac copy** synced via Dropbox
3. **Previous backups** in Cooking folder:
   - `recipe_backup_*.tar.gz`
   - `recipes_backup_*.db`
4. **Git repository** tracks code changes

To restore from backup:
```bash
# Restore database
cp recipes_backup_20251102_072601.db recipes.db

# Re-export and upload
python3 export_to_json.py
python3 upload_recipes_to_dropbox.py <TOKEN>
```

---

## Development Notes

### For Claude Code AI:

When user wants to add/modify recipes:

1. **Website changes** (favorites, edits, deletes):
   - User makes change on website
   - Change saves to Dropbox automatically
   - No action needed - it just works!

2. **New recipes from PDFs**:
   - Update `recipes.db` on Mac
   - Run `python3 export_to_json.py`
   - Dropbox auto-syncs to cloud
   - Website picks up changes on next load

3. **Deploying code changes**:
   - Only deploy when HTML/CSS/JS changes
   - Data changes DON'T need deployment
   - `netlify deploy --prod --dir="." --message="description"`

---

## Future Enhancements

Possible additions:
- ✨ Edit recipe form (full recipe editing)
- ✨ Add recipe button (create new recipes)
- ✨ Batch import from files
- ✨ Recipe ratings and notes
- ✨ Shopping list generator
- ✨ Meal planning

---

**Last Updated:** November 2, 2025
**Status:** ✅ Fully operational with Dropbox integration
**Live URL:** https://fergi-cooking.netlify.app
