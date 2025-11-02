# Fergi Cooking - Deployment Guide

**Quick Reference:** This project is deployed to Netlify at https://fergi-cooking.netlify.app

**⭐ NEW:** As of November 2, 2025, recipes are stored in Dropbox (not deployed to Netlify)

---

## Deployment Overview

**Platform:** Netlify
**Site Name:** fergi-cooking
**Production URL:** https://fergi-cooking.netlify.app
**Admin Dashboard:** https://app.netlify.com/projects/fergi-cooking
**Account:** fergidotcom@gmail.com
**Data Storage:** Dropbox (`/recipes.json`)

---

## Architecture (NEW - Dropbox Integration)

### Data Flow:
```
┌──────────────────────────────┐
│  Website                     │
│  (fergi-cooking.netlify.app) │
│  - OAuth login               │
│  - Load from Dropbox         │
│  - Save to Dropbox           │
└──────────────────────────────┘
           ↓↑ Dropbox API
┌──────────────────────────────┐
│  Dropbox: /recipes.json      │
│  (SINGLE SOURCE OF TRUTH)    │
└──────────────────────────────┘
           ↓ Auto-sync
┌──────────────────────────────┐
│  Your Mac (Dropbox sync)     │
│  recipes.json (synced copy)  │
│  recipes.db (export source)  │
└──────────────────────────────┘
```

### Key Points:
- **recipes.json in Dropbox** is the master database
- **Website loads/saves** directly from/to Dropbox
- **Changes auto-sync** to your Mac via Dropbox
- **recipes.db** used only for adding new recipes from PDFs
- **No deployment needed** for recipe data changes

## Project Structure

```
Cooking/
├── index.html                      # Main web interface (with Dropbox OAuth)
├── recipes.json                    # Recipe data (auto-syncs from Dropbox)
├── recipes.db                      # SQLite database (export source only)
├── netlify.toml                    # Netlify configuration
├── DROPBOX_SETUP.md                # ⭐ Dropbox setup guide
├── upload_recipes_to_dropbox.py    # Initial upload script
└── netlify/
    └── functions/                  # Serverless functions
        ├── dropbox-oauth.js        # ⭐ Dropbox OAuth handler
        ├── get-recipe.js           # (Legacy - not used)
        ├── get-recipes.js          # (Legacy - not used)
        └── statistics.js           # (Legacy - not used)
```

**Note:** get-recipe.js, get-recipes.js, and statistics.js are now unused. The website loads directly from Dropbox.

---

## Quick Deploy Commands

### Deploy to Production (Fastest)
```bash
netlify deploy --prod --dir="." --message="Your deploy message"
```

### Preview Deploy (Test first)
```bash
netlify deploy --dir="." --message="Testing changes"
```

### Check Status
```bash
netlify status
```

### View Logs
```bash
netlify functions:logs
```

---

## Complete Deployment Workflow

### 1. Make Changes
Edit files as needed:
- `index.html` - Web interface changes
- `netlify/functions/*.js` - Backend function changes
- `recipes.json` - Recipe data updates

### 2. Test Locally (Optional)
```bash
netlify dev
# Opens at http://localhost:8888
```

### 3. Deploy
```bash
# Production deploy
netlify deploy --prod --dir="." --message="Description of changes"
```

### 4. Verify
Visit: https://fergi-cooking.netlify.app

---

## Common Deployment Scenarios

### After Recipe Database Updates

When you update the SQLite database (`recipes.db`), you need to regenerate `recipes.json`:

```bash
# Generate updated recipes.json from database
python3 export_to_json.py  # (if this script exists)
# OR manually export from database

# Deploy updated recipes
netlify deploy --prod --dir="." --message="Updated recipe data"
```

### After Instruction Reformatting

Just deploy (recipes.json should be up-to-date):

```bash
netlify deploy --prod --dir="." --message="Updated recipe instructions"
```

### After UI Changes

```bash
# Edit index.html
# Then deploy
netlify deploy --prod --dir="." --message="UI improvements"
```

### After Function Changes

```bash
# Edit files in netlify/functions/
# Then deploy (functions are automatically bundled)
netlify deploy --prod --dir="." --message="Updated serverless functions"
```

---

## What Gets Deployed

**Included:**
- `index.html` - Main web interface
- `recipes.json` - Recipe data (included in function bundle via netlify.toml)
- `netlify/functions/*.js` - Serverless functions
- All other web assets (CSS, JS, images if any)

**Excluded (via .gitignore):**
- `recipes.db` - SQLite database (too large, use recipes.json instead)
- `*.py` - Python scripts (run locally only)
- Backup files
- Node modules (if any)

---

## Netlify Configuration (netlify.toml)

Current configuration:
- **Publish directory:** `.` (current directory)
- **Functions directory:** `netlify/functions`
- **Included in functions:** `recipes.json`

**API Routes:**
- `/api/recipes` → `get-recipes` function
- `/api/recipes/:id` → `get-recipe` function
- `/api/statistics` → `statistics` function
- `/api/search` → `get-recipes` function

All routes fallback to `index.html` for SPA routing.

---

## Troubleshooting

### Deploy Fails

**Check:**
1. Are you in the correct directory?
   ```bash
   pwd  # Should show: .../Dropbox/Fergi/Cooking
   ```

2. Is netlify CLI installed?
   ```bash
   which netlify  # Should show: /opt/homebrew/bin/netlify
   ```

3. Are you logged in?
   ```bash
   netlify status  # Should show your account
   ```

### Functions Not Working

**Check function logs:**
```bash
netlify functions:logs
```

**Test locally:**
```bash
netlify dev
```

**Common issues:**
- `recipes.json` not updated - regenerate from database
- Function syntax errors - check logs
- CORS issues - already configured in netlify.toml

### Site Not Updating

**Clear cache:**
1. Hard refresh browser (Cmd+Shift+R)
2. Check deployment URL in terminal output
3. Use unique deploy URL for testing

---

## Deployment History

| Date | Version | Description |
|------|---------|-------------|
| Nov 2, 2025 | v1.1 | Updated recipe instructions to use explicit ingredients |
| Nov 1, 2025 | v1.0 | Initial deployment with recipe collection |

---

## Environment Variables

Currently: None required

If you add API keys or secrets in the future:
```bash
netlify env:set KEY_NAME value
netlify env:list
```

---

## CI/CD (Optional Future Enhancement)

Currently: Manual deployments via CLI

**To enable automatic deployments:**
1. Connect GitHub repository to Netlify
2. Configure build settings in Netlify dashboard
3. Deployments will trigger on git push

---

## Site Settings

**Custom Domain:** Not configured (using fergi-cooking.netlify.app)

To add custom domain:
1. Go to: https://app.netlify.com/projects/fergi-cooking/settings/domain
2. Add custom domain
3. Configure DNS records

---

## Monitoring

**Check site status:**
- Netlify Dashboard: https://app.netlify.com/projects/fergi-cooking
- Function logs: https://app.netlify.com/projects/fergi-cooking/logs/functions
- Analytics: https://app.netlify.com/projects/fergi-cooking/analytics

---

## Quick Reference Card

```bash
# MOST COMMON COMMANDS

# Deploy to production NOW
netlify deploy --prod --dir="." --message="Updated recipes"

# Check what site you're deploying to
netlify status

# Test locally before deploying
netlify dev

# View function logs
netlify functions:logs
```

---

## For Claude Code AI

When user asks to "deploy to Netlify":

1. **Verify location:** Check you're in the Cooking directory
2. **Check status:** Run `netlify status` to verify site linkage
3. **Deploy:** Run `netlify deploy --prod --dir="." --message="[description]"`
4. **Confirm:** Report the production URL: https://fergi-cooking.netlify.app

**Do NOT:**
- Run `netlify init` (already linked)
- Try to configure netlify.toml (already configured)
- Deploy from wrong directory
- Forget the `--prod` flag for production deploys

---

## Additional Resources

- **Netlify Docs:** https://docs.netlify.com
- **Netlify Functions:** https://docs.netlify.com/functions/overview/
- **Fergi Infrastructure Guide:** See `FERGI_INFRASTRUCTURE_GUIDE.md` in parent directory

---

**Last Updated:** November 2, 2025
**Site URL:** https://fergi-cooking.netlify.app
**Status:** ✓ Active and deployed
