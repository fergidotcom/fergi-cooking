# CLAUDE.md - Cooking Project

This file provides guidance to Claude Code (claude.ai/code) when working with the Cooking project.

## Project Overview

**Cooking Project** - A personal recipe collection and management system for organizing, searching, and managing family recipes and cooking resources.

**Project Location:** `/Users/joeferguson/Library/CloudStorage/Dropbox/Fergi/Cooking`
**Created:** October 30, 2025
**Purpose:** Organize and manage recipe collection, create searchable recipe database, document family recipes

## Project Structure

```
Cooking/
├── CLAUDE.md                           # This file - Project documentation
├── *.pdf                               # Recipe PDFs (50+ files)
├── *.pages                             # Recipe documents (Pages format)
├── Janet Mason/                        # Sub-collection of recipes
└── (Future: Recipe database, search tools, web interface)
```

## Current Contents

The project contains 50+ recipe files including:

**Recipe Categories:**
- Main Dishes: Beef Bourguignon, Beef Stroganoff, Chicken Piccata, Meatloaf variants
- Vegetarian: Vegetable Korma, Eggplant Parmesan, Portabello Mushroom Stroganoff
- Pasta: Fettuccine Alfredo, Lasagna, Pasta Primavera
- Specialty: Jerk Chicken, Curries, French Onion Soup
- Breakfast: Breakfast Casseroles, Italian Baked Eggs

**File Formats:**
- PDF recipes (from web sources like NYT Cooking, Epicurious)
- Pages documents (custom recipes and modifications)
- Recipe collections (Adrienne Cookbook, NancyBernRecipes, etc.)

## Potential Features

The following are ideas for developing this project:

### Recipe Database
- Extract recipes from PDFs and Pages documents
- Structure into searchable database (SQLite, JSON, or similar)
- Tag recipes by category, cuisine, difficulty, prep time
- Track favorites and modifications

### Recipe Search Tool
- Full-text search across all recipes
- Filter by ingredients, category, time
- Find recipes using available ingredients
- Suggest similar recipes

### Recipe Management
- Convert recipes to standard format
- Scale recipe quantities
- Calculate nutritional information
- Track cooking history and notes

### Web Interface
- Browse recipe collection
- View recipes with formatting
- Add cooking notes and ratings
- Share recipes with family

### Recipe Import/Export
- Import from common recipe websites
- Export to PDF, Markdown, or other formats
- Sync with recipe apps
- Backup recipe collection

## Development Notes

**File Access:**
- All files are in Dropbox, synced across devices
- PDF files can be read directly
- Pages documents may need conversion to extract text
- Some recipes have both .pages and .pdf versions

**Recipe Organization:**
- Many recipes from popular sources (NYT Cooking, Epicurious)
- Some custom family recipes (Joe's Meatloaf, Beef Bourguignon variants)
- Special collections (Adrienne Cookbook, Janet Mason subfolder)
- Recipes span multiple cuisines (American, Italian, Indian, Caribbean)

## Common Tasks

### Adding New Recipes
1. Save recipe file to Cooking folder
2. Use consistent naming: `[Dish Name] [Source/Variant].pdf`
3. Update this documentation if adding new categories

### Finding Recipes
Currently manual search through files. Future: Build search tool.

### Recipe Modifications
For custom variants:
1. Create new .pages document with recipe name + "Fergi" or "Joe's"
2. Document modifications from original
3. Export to PDF for easy sharing

## Future Development Ideas

**Phase 1: Organization**
- Create recipe inventory spreadsheet/database
- Tag all recipes with metadata
- Identify duplicates and variants

**Phase 2: Extraction**
- Extract recipe text from PDFs
- Parse recipe format (ingredients, instructions)
- Create structured recipe database

**Phase 3: Tools**
- Build recipe search tool
- Create web interface for browsing
- Add recipe import/export features

**Phase 4: Advanced**
- Meal planning tool
- Grocery list generator
- Recipe scaling calculator
- Cooking timer integration

## Related Projects

**Reference Refinement** (`~/Library/CloudStorage/Dropbox/Fergi/AI Wrangling/References`)
- Similar document management and search challenges
- Could share search/indexing technology
- Both deal with organizing large document collections

**Ferguson Family Archive** (`~/Library/CloudStorage/Dropbox/Fergi/Ferguson Family Archive`)
- Family history and documentation
- Could include historical family recipes
- Recipe collection is part of family heritage

## Notes

This project is currently in **planning/organization phase**. No code has been written yet.

The recipe collection represents years of accumulated cooking knowledge and family traditions. Any development should preserve the original files and metadata.

## Getting Started

When you're ready to start development on this project:

1. **Inventory:** Create list of all recipes with metadata
2. **Choose format:** Decide on database structure (SQLite, JSON, etc.)
3. **Extract recipes:** Build tool to parse PDFs and Pages documents
4. **Build search:** Create search interface
5. **Iterate:** Add features based on usage and needs

---

**Last Updated:** October 30, 2025
**Status:** Project initialized, awaiting development direction
