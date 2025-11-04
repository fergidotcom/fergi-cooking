# Recipe Data Cleanup Script

## Overview

The `cleanup_recipes.py` script performs comprehensive data cleanup on the Fergi Cooking recipe database. It's part of the v4.0 upgrade to improve data quality and mobile UX.

## What It Does

1. **Removes Non-Recipes** - Identifies and removes books, articles, or other non-recipe content
2. **Extracts Attributions** - Moves attribution text from instructions to proper metadata fields
3. **Fixes OCR Errors** - Corrects common OCR mistakes from Janet Mason's image imports (l→1, O→0, etc.)
4. **Standardizes Ingredients** - Normalizes measurement units and formatting
5. **Verifies Contributors** - Ensures correct contributor assignments (Janet vs Fergi)
6. **Validates Metadata** - Checks cooking times, servings, and other metadata
7. **Flags Reviews** - Marks incomplete recipes with `needs_review` flag

## Prerequisites

### 1. Install Dependencies

```bash
pip3 install dropbox
```

### 2. Set Environment Variable

You need a Dropbox API access token:

```bash
export DROPBOX_ACCESS_TOKEN="your_token_here"
```

Get the token from:
- Netlify environment variables (fergi-cooking site)
- Or generate a new one at https://www.dropbox.com/developers/apps

### 3. Verify Data Path

The script expects recipes at:
```
/Apps/Reference Refinement/recipes.json
```

This is the shared Dropbox location used by both Cooking and Reference Refinement projects.

## Usage

### Basic Usage

```bash
cd /path/to/Cooking
python3 scripts/cleanup_recipes.py
```

### What Happens

1. **Backup Created** - Automatic backup before any changes
   - Saved as: `recipes_backup_YYYYMMDD_HHMMSS.json`

2. **Recipes Processed** - Each recipe is validated and cleaned
   - Progress shown every 10 recipes

3. **Report Generated** - Comprehensive cleanup report created
   - Saved as: `cleanup_report_YYYYMMDD_HHMMSS.txt`

4. **Data Saved** - Cleaned recipes uploaded to Dropbox
   - Replaces existing recipes.json

## Expected Results

### Contributor Distribution

The script verifies expected contributor counts:
- **Janet**: ~85 recipes (from Janet Mason's cookbook)
- **Fergi**: ~37 recipes (general collection)

### Non-Recipe Removal

Identifies and removes entries that are:
- Books or book chapters
- Articles or blog posts
- Reference material (not actual recipes)

### OCR Error Patterns Fixed

Common errors from image OCR:
- `l` (lowercase L) → `1` (number one)
- `O` (uppercase O) → `0` (zero)
- `ll` → `11`
- `OO` → `00`

### Attribution Extraction

Patterns detected and moved to metadata:
- "Recipe from [Name]"
- "Recipe by [Name]"
- "Courtesy of [Name]"
- "Adapted from [Name]"
- "Source: [Name]"

## Output Files

### 1. Backup File
```
recipes_backup_20251104_143022.json
```
Contains original data before cleanup. Keep this for reference.

### 2. Cleanup Report
```
cleanup_report_20251104_143022.txt
```
Detailed report showing:
- Total recipes processed
- Non-recipes removed (with reasons)
- Contributor fixes made
- OCR errors fixed count
- Ingredients standardized count

Example report:
```
============================================================
RECIPE CLEANUP REPORT
Generated: 2025-11-04T14:30:22.123456
============================================================

Total Processed: 122
Recipes Cleaned: 121
Non-Recipes Removed: 1
Attributions Extracted: 15
OCR Errors Fixed: 43
Ingredients Standardized: 845
Contributor Fixes: 8

------------------------------------------------------------
NON-RECIPES REMOVED:
------------------------------------------------------------
- The Complete Cookbook: Failed recipe validation

------------------------------------------------------------
CONTRIBUTOR FIXES:
------------------------------------------------------------
- Beef Stroganoff: Fergi → Janet
- Chicken Piccata: Fergi → Janet
...
```

## Safety Features

### Automatic Backup
- Backup created BEFORE any changes
- Saved locally and can be restored if needed

### Validation
- Recipes must have ingredients and instructions
- Cooking times must be reasonable (0-720 minutes)
- Servings must be 1-100

### Logging
- Detailed console output during processing
- Warnings for suspicious content
- Progress indicators every 10 recipes

## Troubleshooting

### Error: "DROPBOX_ACCESS_TOKEN environment variable not set"

Set the token before running:
```bash
export DROPBOX_ACCESS_TOKEN="your_token_here"
```

### Error: "Dropbox library not installed"

Install the required package:
```bash
pip3 install dropbox
```

### Error: "Failed to load from Dropbox"

Check:
1. Token is valid and not expired
2. Path is correct: `/Apps/Reference Refinement/recipes.json`
3. Network connection is working

### Warning: "Contributor counts unusual"

Expected counts:
- Janet: 80-90 recipes
- Fergi: 30-40 recipes

If counts are far off, manual review may be needed.

## Restoring from Backup

If you need to restore the original data:

```bash
# Find the backup file
ls -lh recipes_backup_*.json

# Restore via Python
python3 -c "
import json
import dropbox
import os

# Load backup
with open('recipes_backup_YYYYMMDD_HHMMSS.json', 'r') as f:
    data = json.load(f)

# Upload to Dropbox
token = os.environ['DROPBOX_ACCESS_TOKEN']
dbx = dropbox.Dropbox(token)
dbx.files_upload(
    json.dumps(data, indent=2).encode('utf-8'),
    '/Apps/Reference Refinement/recipes.json',
    mode=dropbox.files.WriteMode.overwrite
)
print('Restored from backup')
"
```

## Next Steps After Cleanup

1. **Test locally**
   ```bash
   netlify dev
   ```

2. **Verify recipes display correctly**
   - Check recipe cards
   - Open recipe details
   - Verify contributor filter

3. **Check "Needs Review" filter**
   - Should show flagged recipes
   - Fix any incomplete recipes

4. **Deploy to production**
   ```bash
   netlify deploy --prod --dir="." --message="v4.0.0 - Data cleanup complete"
   ```

## Developer Notes

### Adding New Cleanup Rules

To add new cleanup patterns, edit `cleanup_recipes.py`:

```python
class RecipeValidator:
    # Add new OCR error patterns
    OCR_ERRORS = {
        r'your_pattern': 'replacement',
    }

    # Add new measurement standards
    MEASUREMENT_STANDARDS = {
        'your_unit': 'standard_unit',
    }
```

### Custom Validation

Add custom validation in `is_recipe()` method:

```python
def is_recipe(self, recipe: Dict) -> bool:
    # Your custom checks
    if some_condition:
        return False
    return True
```

## Version History

- **v4.0.0** (Nov 4, 2025) - Initial cleanup script
  - Non-recipe removal
  - OCR error fixing
  - Contributor verification
  - Metadata validation

---

**Script Location:** `/scripts/cleanup_recipes.py`
**Author:** Claude Code (Sonnet 4.5)
**Part of:** Fergi Cooking App v4.0
**Documentation:** This file
