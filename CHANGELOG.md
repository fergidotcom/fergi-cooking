# Changelog - Fergi Cooking

All notable changes to the Fergi Cooking project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.0.0] - 2025-11-07

### 🎉 MAJOR RELEASE - Mobile-First UI Redesign

**Status:** ✅ Deployed to Production
**Live URL:** https://fergi-cooking.netlify.app
**Session:** SESSION_SUMMARY_2025-11-07_V4.0_UI_REDESIGN.md

### Changed - Complete Visual Redesign

#### Ferguson Family Archive Design System Integration
- Integrated complete design system from Ferguson Family Archive project
- New CSS design tokens system:
  - **Colors:** Primary (#3b82f6), Success (#10b981), Warning (#f59e0b), Danger (#ef4444)
  - **Spacing:** 8px base grid system (--space-xs through --space-2xl)
  - **Typography:** Consistent font sizes (--font-xs through --font-4xl) and weights
  - **Shadows:** Four-level shadow system (--shadow-sm through --shadow-xl)
  - **Border Radius:** Consistent radius values (--radius-sm through --radius-full)
- Legacy variable mappings for backward compatibility

#### Mobile-First Responsive Improvements
- Enhanced mobile-first responsive layout throughout
- Improved touch targets: 44px minimum height on all interactive elements
- Better spacing and gap management using design tokens
- Full-screen modals on mobile devices with smooth animations
- Sticky headers with proper z-index management
- Responsive navigation that adapts to mobile, tablet, and desktop

#### Component Refinements
- **Recipe Cards:**
  - Refined hover effects (transform + shadow-xl)
  - Better border treatment with primary color on hover
  - Improved card header gradients
  - Better information hierarchy with updated typography

- **Buttons:**
  - Consistent sizing with min-height: 44px
  - Smooth 0.2s transitions
  - Proper hover states with lift effect (translateY(-2px))
  - Updated color scheme matching design system

- **Forms:**
  - Enhanced focus states with ring effect (box-shadow)
  - Better input padding and border radius
  - Smooth transitions on interaction
  - Improved label typography

- **Modals:**
  - Smooth fade-in and slide-up animations
  - Better close button (44px, rounded, with rotate animation)
  - Improved overlay darkness (rgba(0, 0, 0, 0.75))
  - Full-screen on mobile with proper scrolling

#### Updated Files
- ✅ `index.html` - Complete CSS redesign with all design tokens
- ✅ `events.html` - Updated with design system
- ✅ `event-detail.html` - Updated with design system
- ✅ `respond.html` - Updated with design system
- ✅ `add-recipe.html` - Updated with design system
- ✅ `cooking.html` - Lightly updated (colors/typography only, maintained kitchen UX)

### Technical

#### Backward Compatibility
- All 19 Netlify Functions unchanged
- No breaking changes to functionality
- Legacy CSS variable mappings ensure compatibility
- All existing features preserved:
  - Recipe browsing, search, and filtering
  - Contributor management
  - Event management and guest responses
  - Recipe import wizard
  - Mobile cooking mode
  - Dropbox synchronization

#### Design Decisions
- Mobile-first approach: base styles for mobile, enhanced for larger screens
- Consistent 0.2s transition timing for all interactions
- Primary color changed from dark blue-gray (#2c3e50) to modern blue (#3b82f6)
- Success color changed from darker green to modern emerald (#10b981)
- Warning/secondary unified to amber (#f59e0b)
- Danger color standardized to red (#ef4444)

### Notes
- This is a major version bump (3.1.x → 4.0.0) due to significant visual changes
- No functionality changes - purely a design system upgrade
- Sets visual standard for future Fergi projects
- Cooking mode intentionally left minimal (kitchen-optimized)

---

## [3.1.0] - 2025-11-04

### 🎉 MAJOR FEATURE - Mobile Cooking Mode

**Status:** ✅ Deployed to Production
**Live URL:** https://fergi-cooking.netlify.app
**Session:** SESSION_SUMMARY_2025-11-03_V3.1_COOKING_MODE.md

### Added

#### Mobile-First Cooking Interface
- **NEW:** `cooking.html` - Dedicated mobile cooking mode interface
- Large, readable text (18-28px) - readable from 2 feet away
- Single column layout optimized for phones
- Ingredient checkboxes to mark off as you use them
- Big step numbers in colored circles (40px)
- Wake Lock API - keeps screen on while cooking!
- Shareable URLs: `cooking.html?recipe_id=X`
- Beautiful loading states and error handling
- Print-friendly styles

#### User Experience Improvements
- "👨‍🍳 Cooking Mode" button added to recipe detail modal
- Opens full-screen cooking interface in new tab
- Prominent red gradient button (stands out)
- Automatic recipe loading with fallback strategy
- Clean, minimal UI perfect for kitchen use

#### Backend Ready for Authentication (Phase 2)
- **NEW:** `send-verification-code.js` - Email 6-digit verification codes
- **NEW:** `verify-code.js` - Validate codes and create sessions
- Passwordless email authentication system (backend complete)
- Dropbox storage for verification codes and users
- Session token generation
- Ready for UI integration (next release)

### Design Documentation
- **NEW:** `DESIGN_SPEC_V3.1_USER_EVENTS_MOBILE.md` - Complete 3-phase specification
  - Mobile cooking mode design (IMPLEMENTED ✅)
  - Passwordless authentication design (Backend ready ⏳)
  - Event segregation design (Planned 📋)

### What Problem This Solves
**Janet's Complaint:** "I can't read recipes on my phone while cooking!"

**Solution:** Dedicated cooking mode with:
- Text 2x larger than standard mobile view
- Clear visual hierarchy (big numbers, bold quantities)
- No screen timeout (Wake Lock API)
- Minimal interaction required
- Perfect for glancing at while cooking

### New Netlify Functions
- `send-verification-code.js` (178 lines) - Email verification
- `verify-code.js` (210 lines) - Code validation & sessions

### Total Functions: 19 (was 17)

### Environment Variables (Optional for Phase 2)
- `RESEND_API_KEY` - For email verification (Phase 2 feature)

### Next Steps (Phases 2 & 3)
- Phase 2: Add login UI, session management, user profiles
- Phase 3: Event ownership, "My Events" filtering, access control

---

## [3.0.0] - 2025-11-03

### 🎉 MAJOR RELEASE - Recipe Import System

**Status:** ✅ Deployed to Production
**Live URL:** https://fergi-cooking.netlify.app
**Session:** COMPLETE_SESSION_SUMMARY_2025-11-03_V3.0_DEPLOYMENT.md

### Added

#### Recipe Import Wizard
- 4-step wizard interface with progress indicators
- File upload support: PDF, Word (.docx), Images (OCR), Plain Text
- Text paste option for quick recipe entry
- AI-powered recipe formatting using Claude Sonnet 4 API
- Live preview panel with edit capability
- Contributor selection with inline add functionality
- Save directly to Dropbox (no redeployment needed)

#### Contributor Management
- Public contributor management (no authentication)
- Add/remove contributors via modal interface
- Automatic validation (no duplicates, no empty names)
- Block removal if contributor has recipes
- Contributor filter dropdown on main page
- Statistics dashboard with contributor breakdown
- Auto-assigned 85 recipes to "Janet Mason", 37 to "Fergi"

#### New Backend Functions (4)
- `extract-file.js` - Extract text from uploaded files (PDF, Word, Images)
- `format-recipe.js` - AI recipe formatting via Claude API
- `add-recipe.js` - Save new recipes to Dropbox
- `manage-contributors.js` - Full CRUD for contributors

#### UI Enhancements
- + Add Recipe button (orange, prominent) in main navigation
- 👥 Contributors button (teal) in main navigation
- Beautiful two-column print layout (ingredients left, instructions right)
- Enhanced statistics with contributor counts
- Contributor filter dropdown

### Changed

#### Architecture
- **BREAKING:** Migrated from bundled recipes.json to Dropbox-only storage
- All data now in `/Apps/Reference Refinement/` (shared with Reference Refinement)
- Single database file per application (recipes.json for Cooking)
- Real-time updates without redeployment
- Functions use Dropbox API with auto-refresh tokens

#### Updated Functions (3)
- `get-recipes.js` - Now fetches from Dropbox, supports contributor filtering
- `save-recipes.js` - Updated to use Dropbox with auto-refresh
- `netlify.toml` - Removed bundled files, added new API endpoints

### Dependencies
- Added `pdf-parse@2.4.5` - PDF text extraction
- Added `mammoth@1.11.0` - Word document parsing
- Added `tesseract.js@6.0.1` - OCR for images (no external API!)
- Added `@anthropic-ai/sdk@0.68.0` - Claude API integration
- Added `lambda-multipart-parser@1.0.1` - File upload handling
- Total: 43 new packages (52 total)

### Fixed
- Recipe names now display correctly (no more "Recipe #X")
- Custom dish name handling for guest responses
- API endpoint reliability improvements

### Known Limitations
- Image OCR takes 30-60 seconds (tesseract.js processing time)
- Old .doc files not supported (only .docx)
- Requires ANTHROPIC_API_KEY environment variable
- No recipe versioning or edit history
- No duplicate recipe detection
- File size limit: 10MB
- Contributor assignment is runtime (not saved to database)

### Environment Variables Required
- **NEW:** `ANTHROPIC_API_KEY` - Required for recipe formatting

---

## [2.8.1] - 2025-11-03

### Fixed
- Custom dish name handling for "will_bring" responses
- Smart detection: user input becomes dish name, not description
- Improved form labels with clear help text
- Example: Murray prefers Beef Stroganoff but brings Fish → Shows "You will bring: Fish"

---

## [2.8.0] - 2025-11-03

### 🔧 CRITICAL FIX - API Endpoints

**Session:** SESSION_SUMMARY_2025-11-03_RECIPE_DISPLAY_FIXES.md

### Fixed
- Broken get-recipe and get-recipes API endpoints
- Recipe names now display correctly throughout system
- Bundled recipes.json with Netlify Functions (`included_files` config)
- Both single recipe and all recipes endpoints fully functional
- Dual loading strategy: try get-recipe first, fallback to get-recipes

### Added
- Loading screen displays while fetching recipe details
- Form refuses to display without recipe data (prevents errors)
- Comprehensive error handling and console logging
- Detailed debugging with emojis in console

---

## [2.7.9] - 2025-11-03

### Enhanced
- Robust recipe loading with dual strategy
- Comprehensive error handling for recipe fetching
- Loading indicators during API calls
- Recipe data validation before display

---

## [2.7.8] - 2025-11-03

### Changed
- Removed all "Recipe #X" fallback text
- Shows actual recipe names (e.g., "Beef Stroganoff", "Bananas Foster")
- Context-aware headings for guest responses (prefer vs. will_bring)

---

## [2.7.0] - 2025-11-02

### Added
- Event management system
- Guest preference collection
- Recipe-to-event assignment
- Email generation with multiple copy methods
- Public guest response page (no authentication)
- Dietary restrictions tracking
- Volunteer category collection

---

## [2.0.0] - 2025-11-01

### 🎉 MAJOR RELEASE - Janet Mason's Cookbook Integration

### Added
- Extracted 85 recipes from Janet Mason's cookbook images
- Batch OCR extraction scripts (9 batches)
- Recipe metadata and categorization
- Source attribution system

### Changed
- Database expanded to 122 recipes (from 37)
- Enhanced recipe schema with source tracking

---

## [1.0.0] - 2025-10-30

### 🎉 INITIAL RELEASE

**Session:** PROJECT_SUMMARY.md

### Added
- SQLite database with 37 initial recipes
- Recipe browsing interface
- Full-text search capability
- Recipe filtering by source, cuisine, meal type
- Recipe detail view with formatted ingredients and instructions
- Recipe statistics dashboard
- Netlify Functions backend (5 functions)
- Deployed to https://fergi-cooking.netlify.app

#### Database Schema
- `recipes` - Recipe metadata and details
- `ingredients` - Recipe ingredients with quantities
- `instructions` - Step-by-step cooking instructions
- `tags` - Recipe tags and categories
- `cooking_log` - Cooking history and notes
- `recipe_images` - Recipe images
- `recipes_fts` - Full-text search index

#### Initial Backend Functions
- `get-recipes.js` - Get all/search recipes
- `get-recipe.js` - Get single recipe by ID
- `statistics.js` - Recipe statistics
- `save-recipes.js` - Bulk save recipes
- `load-recipes.js` - Load from Dropbox

### Recipe Sources
- NYT Cooking
- Epicurious
- Custom family recipes
- Recipe collections (Adrienne Cookbook, NancyBernRecipes)

---

## Version History Summary

- **v3.0.0** (2025-11-03) - Recipe Import System & Contributor Management
- **v2.8.1** (2025-11-03) - Custom Dish Name Fix
- **v2.8.0** (2025-11-03) - API Endpoints Fix
- **v2.7.9** (2025-11-03) - Enhanced Recipe Loading
- **v2.7.8** (2025-11-03) - Recipe Name Display Improvements
- **v2.7.0** (2025-11-02) - Event Management System
- **v2.0.0** (2025-11-01) - Janet Mason's Cookbook (122 recipes)
- **v1.0.0** (2025-10-30) - Initial Release (37 recipes)

---

## Links

- **Live Site:** https://fergi-cooking.netlify.app
- **Netlify Admin:** https://app.netlify.com/projects/fergi-cooking
- **Dropbox Data:** `/Apps/Reference Refinement/`
- **Documentation:** CLAUDE.md, DEPLOYMENT.md
- **Complete Session Summary:** COMPLETE_SESSION_SUMMARY_2025-11-03_V3.0_DEPLOYMENT.md

---

**Maintained by:** Fergi Workspace
**Last Updated:** November 3, 2025
