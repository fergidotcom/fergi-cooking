# Fergi Cooking - Feature Requests & TODO

**Last Updated:** November 2, 2025

---

## High Priority

### ✏️ Full Recipe Edit Form
**Status:** Planned (Edit button exists but form needs completion)
**Description:** Complete implementation of recipe editing for all fields

---

## Medium Priority

### ➕ Add New Recipe Button
**Status:** Planned
**Description:** Create recipes directly from website
**Features:**
- Form to enter recipe details
- Ingredient list builder
- Instruction steps editor
- Image upload
- Auto-generate recipe ID
- Save to Dropbox

### 📷 Recipe Images
**Status:** Planned
**Description:** Support uploading and displaying recipe images
**Current:** Database has recipe_images table but not utilized
**Features:**
- Upload images from website
- Display in recipe cards and detail view
- Store in Dropbox or image hosting service
- Multiple images per recipe
- Image gallery view

### ⭐ Recipe Ratings & Notes
**Status:** Planned
**Description:** Add personal ratings and cooking notes
**Features:**
- Rate recipes 1-5 stars (currently read-only)
- Add cooking notes/modifications
- Track when you last made it
- Mark as "tried" or "want to try"

---

## Lower Priority

### 🛒 Shopping List Generator
**Status:** Idea stage
**Description:** Generate shopping list from selected recipes
**Features:**
- Select multiple recipes
- Combine ingredients
- Adjust quantities for servings
- Organize by store section
- Export/print list

### 📅 Meal Planning
**Status:** Idea stage
**Description:** Plan meals for the week
**Features:**
- Drag recipes to calendar
- Auto-generate shopping lists
- Nutritional summaries
- Leftover tracking

### 🔄 Import/Export
**Status:** Idea stage
**Description:** Import recipes from various sources
**Features:**
- Import from URLs (NYT Cooking, Epicurious, etc.)
- Import from PDF
- Export recipes to standard formats
- Batch import

### 🔍 Advanced Search
**Status:** Idea stage
**Description:** Enhanced search capabilities
**Features:**
- Search by ingredient
- Filter by prep time, calories, cuisine
- "What can I make with..." feature
- Similar recipe suggestions

### 📊 Nutritional Information
**Status:** Idea stage
**Description:** Calculate and display nutritional info
**Features:**
- Auto-calculate from ingredients
- Display per serving
- Track daily intake
- Dietary filters (low-carb, high-protein, etc.)

### 👨‍👩‍👧‍👦 Multi-user Support
**Status:** Idea stage
**Description:** Share recipes with family
**Features:**
- Multiple Dropbox accounts
- Shared recipe collections
- Comments and reviews
- Recipe contributions

---

## Completed Features

### ✅ Print Recipe Button (Nov 2, 2025)
- Print button in recipe detail window
- Clean print layout (hides navigation/UI elements)
- @media print CSS optimization
- Page break control for ingredients and instructions
- Browser's native print dialog

### ✅ Dropbox Integration (Nov 2, 2025)
- OAuth login
- Load/save recipes from Dropbox
- Auto-sync to Mac
- Single source of truth

### ✅ Favorites Filter (Nov 2, 2025)
- Filter tab in navigation
- Toggle favorites functionality
- Persistence in Dropbox

### ✅ Delete Recipes (Nov 2, 2025)
- Functional delete button
- Confirmation dialog
- Removes from Dropbox

### ✅ Explicit Ingredient Instructions (Nov 2, 2025)
- Reformatted indirect references
- All ingredients listed in instructions
- Applied to 23 instructions across ~15-20 recipes

---

## Technical Debt

### Legacy Functions
**Status:** To be removed
**Description:** Old API functions no longer used
**Files:**
- `netlify/functions/get-recipe.js` - Not used (loads from Dropbox now)
- `netlify/functions/get-recipes.js` - Not used
- `netlify/functions/statistics.js` - Not used (or needs reimplementation)

**Action:** Either remove or update to work with Dropbox-based architecture

### Statistics Dashboard
**Status:** Broken
**Description:** Statistics page uses old API
**Fix needed:** Reimplement to calculate stats from local recipes array instead of API

---

## Notes

- **Priority may change** based on user feedback
- **Print button** is current top priority
- **Edit form** is important for full functionality
- **Most features** require minor changes (Dropbox integration makes everything easier)

---

**To add a feature request:**
1. Add to appropriate priority section
2. Include description and benefits
3. Add implementation notes if applicable
4. Update "Last Updated" date

