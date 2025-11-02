# Upload recipes.json to Dropbox - Quick Start

**You're almost done!** Just need to upload recipes.json to your Dropbox so the website can access it.

**Note:** Fergi Cooking uses the **same Dropbox app** as Reference Refinement. Both projects share the `/Apps/Reference Refinement/` folder.

---

## Quick 2-Minute Setup

### Step 1: Get a Dropbox Access Token

1. **Visit:** https://www.dropbox.com/developers/apps
2. **Click** on the "**Reference Refinement**" app (same app used for both projects)
3. **Go to "Permissions" tab**
   - Enable: ☑️ `files.content.write`
   - Enable: ☑️ `files.content.read`
   - Click "Submit" to save (if not already enabled)
4. **Go to "Settings" tab**
5. **Scroll down** to "Generated access token" section
6. **Click "Generate"** button
7. **Copy the token** (it starts with `sl.xxxxx`)

### Step 2: Run the Upload Script

Open Terminal in the Cooking folder and run:

```bash
cd ~/Library/CloudStorage/Dropbox/Fergi/Cooking
python3 upload_recipes_simple.py
```

When prompted, paste your access token and press Enter.

The script will upload `recipes.json` (794 KB) to Dropbox root: `/recipes.json`

---

## Alternative: Manual Upload

If you prefer not to use the script:

**Note:** You cannot manually upload to the app folder via dropbox.com. The app folder (`/Apps/Reference Refinement/`) is only accessible via the Dropbox API. You must use the upload script above.

---

## Step 3: Connect Website to Dropbox

1. **Visit:** https://fergi-cooking.netlify.app
2. Click **"Connect Dropbox"** button
3. Log into Dropbox (if not already logged in)
4. Click **"Allow"** to authorize the app
5. You'll be redirected back to the website
6. **Recipes load automatically!** 🎉

---

## Troubleshooting

### "recipes.json not found in Dropbox"
- Make sure you uploaded to **root** (`/recipes.json`)
- Not in a subfolder (`/Cooking/recipes.json` won't work)

### "Authentication failed"
- Make sure you copied the **entire token** (including `sl.` prefix)
- Make sure you enabled **both permissions** in Dropbox app settings
- Try generating a **new token**

### "Module 'dropbox' not found"
```bash
pip3 install dropbox
```

---

## What Happens Next?

Once uploaded and connected:

✅ **Website loads recipes** from Dropbox
✅ **Edit/favorite/delete** recipes on website
✅ **Changes save to Dropbox** automatically
✅ **Dropbox syncs to Mac** automatically
✅ **No more manual deployments** needed for recipe changes

---

## Files Location

**On Dropbox:**
- `/recipes.json` ← Master copy (122 recipes, 794 KB)

**On Your Mac:**
- `~/Library/CloudStorage/Dropbox/Fergi/Cooking/recipes.json` ← Auto-synced from Dropbox
- `~/Library/CloudStorage/Dropbox/Fergi/Cooking/recipes.db` ← Source database (for adding new recipes)

---

## Daily Workflow After Setup

**View/Edit Recipes:**
- Visit https://fergi-cooking.netlify.app (no login needed after first time)
- Browse, search, favorite, delete recipes
- Changes save automatically to Dropbox
- Dropbox syncs to your Mac

**Add New Recipes from PDFs:**
1. Extract to `recipes.db` on Mac (using existing scripts)
2. Run `python3 export_to_json.py`
3. Dropbox auto-uploads the updated `recipes.json`
4. Reload website - new recipes appear!

---

## Need Help?

See:
- `DROPBOX_SETUP.md` - Full documentation
- `upload_recipes_simple.py` - The upload script (with prompts)
- `DEPLOYMENT.md` - Architecture and deployment info

---

**Ready to go!** Run the upload script and you're all set. 🚀
