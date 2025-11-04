# Quick Start Guide for Next Session

**Last Session:** November 4, 2025
**Current Version:** v3.1.6
**Status:** ✅ Production - All systems operational

---

## What Was Accomplished (Nov 4, 2025)

✅ **v3.1.4** - Fixed contributor assignments (89 Janet, 33 Fergi)
✅ **v3.1.5** - Recipe cards now show contributor names (👤 Janet, 👤 Fergi)
✅ **v3.1.6** - Added "Needs Review" filter, flagged 23 incomplete recipes

---

## Current State

### Database
- **Total Recipes:** 122
- **Contributors:** Janet (89), Fergi (33)
- **Flagged for Review:** 23 recipes (18.9%)
- **Location:** Dropbox at `/Apps/Reference Refinement/recipes.json`

### Flagged Recipes Need Work
- **4 recipes** missing ingredients
- **19 recipes** missing instructions
- **1 recipe** is not a valid recipe (ID #1: 240929AgesOfLogosMaster)

### Known Issues for Next Session
1. **Statistics Page** - Shows wrong contributor counts (says 3 sources, should say 2 contributors)
2. **No Review Reasons** - UI doesn't show WHY recipes are flagged
3. **Manual Unflag** - No button to mark recipes as reviewed

---

## Immediate Tasks (Next Session)

### Priority 1: Fix Statistics Page
**File:** `index.html` (lines ~1362-1447)
**Problem:** Counts `source_attribution` instead of `contributor`
**Fix:** Change logic to count unique contributors

```javascript
// CURRENT (wrong):
sourceCounts[r.source_attribution] = ...

// SHOULD BE:
contributorCounts[r.contributor] = ...
```

### Priority 2: Fix Flagged Recipes
**23 recipes need completion:**

**Missing Instructions (19 recipes):**
- Bananas Foster (#3)
- Beef Bourguignon (#6)
- Beef Stroganoff (#8)
- Buttery Breakfast Casserole (#11)
- Chicken Florentine (#14)
- Corned Beef and Cabbage (#18)
- Curried Cauliflower And Chicken (#19)
- Five Sauces for the Modern Cook (#25)
- Gjelina's Roasted Yams (#26)
- Mary Likes Fettuccine With Asparagus (#34)
- Mary Likes Springtime Spaghetti Carbonara (#35)
- Mary wants Fettuccine With Asparagus (#36)
- Mary's Favorite Fettuccine Alfredo (#37)
- Mueller's Classic Lasagna (#39)
- Our Favorite French Onion Soup (#42)
- Pasta Primavera with Asparagus and Peas (#43)
- Pasta with Spicy Sun Dried Tomato Cream Sauce (#44)
- South Indian Vegetable Curry (#48)
- Stilton Chicken with Apples (#49)

**Missing Ingredients (4 recipes):**
- Eggplant Parm (#24)
- Kerala Style Vegetable Korma (#30)
- MikeMaceysMashed Potatoes (#38)
- 240929AgesOfLogosMaster (#1) - DELETE THIS (not a recipe)

---

## Essential Commands

### View Flagged Recipes
```bash
# In browser
https://fergi-cooking.netlify.app
Click "⚠️ Needs Review" button

# Via API
curl -s "https://fergi-cooking.netlify.app/.netlify/functions/get-recipes" | python3 -c "import sys, json; data = json.load(sys.stdin); print([r['title'] for r in data['recipes'] if r.get('needs_review')])"
```

### Deploy Changes
```bash
# After editing recipes.json locally
python3 upload_recipes_to_dropbox.py

# After editing HTML/UI
netlify deploy --prod --dir="." --message="Description of changes"
```

### Test Locally
```bash
netlify dev  # Opens at http://localhost:8888
```

### Check Database Stats
```python
import json
recipes = json.load(open('recipes.json'))
print(f"Total: {len(recipes)}")
print(f"Need review: {sum(1 for r in recipes if r.get('needs_review') == 1)}")
print(f"Janet: {sum(1 for r in recipes if r.get('contributor') == 'Janet')}")
print(f"Fergi: {sum(1 for r in recipes if r.get('contributor') == 'Fergi')}")
```

---

## Important Files

### Documentation (Read These First)
- **CLAUDE.md** - Main project documentation
- **COMPLETE_SESSION_SUMMARY_2025-11-04.md** - Full session details
- **DEPLOYMENT.md** - Deployment procedures

### Scripts
- **fix_contributors.py** - Assign contributors (already run)
- **upload_recipes_to_dropbox.py** - Upload to production database
- **reformat_instructions.py** - Format instructions (legacy)

### Data
- **recipes.json** - Local copy (must upload to Dropbox for changes)
- **netlify/functions/data/contributors.json** - Contributor list

---

## Critical Reminders

### ⚠️ Dropbox is Production Database
- **DON'T** edit local recipes.json and forget to upload
- **DO** run `python3 upload_recipes_to_dropbox.py` after changes
- **VERIFY** changes via API before considering done

### ⚠️ Version Numbers
- Update version in `index.html` line 722
- Update version in `CLAUDE.md`
- Use semantic versioning: vX.Y.Z

### ⚠️ Testing Workflow
1. Edit local files
2. Test with `netlify dev`
3. Upload data to Dropbox (if recipes.json changed)
4. Deploy to Netlify
5. Verify on live site
6. Document changes

---

## Quick Fixes Guide

### Fix a Single Recipe
1. Click "⚠️ Needs Review" button
2. Click on recipe needing work
3. Click "Edit Recipe" button
4. Add missing ingredients or instructions
5. Save (automatically uploads to Dropbox)

### Bulk Update Recipes
1. Edit `recipes.json` locally
2. Run: `python3 upload_recipes_to_dropbox.py`
3. Verify via: `curl .../.netlify/functions/get-recipes`

### Fix Statistics Page
1. Edit `index.html` (lines 1362-1447)
2. Change source counting to contributor counting
3. Deploy: `netlify deploy --prod`
4. Test: Click "Statistics" button

---

## Version Roadmap

### v3.1.7 (Next Release)
- [ ] Fix Statistics page contributor counts
- [ ] Show review reasons in recipe detail
- [ ] Add "Mark as Reviewed" button

### v3.2.0 (Future)
- [ ] Fix all 23 flagged recipes
- [ ] Auto-unflag when recipe is completed
- [ ] Quality dashboard
- [ ] Bulk edit tools

---

## Session End Checklist

When ending next session, update these:
- [ ] Version number in `index.html`
- [ ] Version number in `CLAUDE.md`
- [ ] Create `SESSION_SUMMARY_YYYY-MM-DD_*.md`
- [ ] Update this quick start guide
- [ ] Upload any recipe changes to Dropbox
- [ ] Deploy to Netlify
- [ ] Verify live site

---

## URLs & Access

**Live Site:** https://fergi-cooking.netlify.app
**Admin Panel:** https://app.netlify.com/projects/fergi-cooking
**GitHub:** @fergidotcom
**Email:** fergidotcom@gmail.com

**Project Path:** `/Users/joeferguson/Library/CloudStorage/Dropbox/Fergi/Cooking`

---

## Common Pitfalls

❌ **Don't:** Edit recipes.json without uploading to Dropbox
❌ **Don't:** Deploy without testing locally first
❌ **Don't:** Forget to update version numbers
❌ **Don't:** Skip documentation

✅ **Do:** Test locally with `netlify dev`
✅ **Do:** Upload data changes to Dropbox
✅ **Do:** Update all version numbers
✅ **Do:** Document significant changes

---

**Ready to Start Next Session!**

📖 Read: `COMPLETE_SESSION_SUMMARY_2025-11-04.md` for full context
🎯 Focus: Fix Statistics page and review flagged recipes
🚀 Deploy: Remember to upload to Dropbox AND deploy to Netlify

**Current Status: ✅ All systems operational**
**Live Version: v3.1.6**
**Last Updated: November 4, 2025**
