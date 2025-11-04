# Cooking App - Complete Technical Specification

**Project:** Fergi's Recipe Collection
**Current Version:** v4.0.0
**Last Updated:** November 4, 2025
**Type:** Recipe Management Web Application
**Status:** ✅ Production - https://fergi-cooking.netlify.app

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Database Schema](#database-schema)
5. [API Endpoints](#api-endpoints)
6. [User Interface](#user-interface)
7. [Mobile UX](#mobile-ux)
8. [Data Management](#data-management)
9. [Deployment](#deployment)
10. [Configuration](#configuration)

---

## Overview

### Purpose
A personal recipe collection and management system for organizing, searching, and managing family recipes with AI-powered import capabilities and mobile-optimized cooking experience.

### Key Users
- **Janet** - Primary user, iPhone, adds recipes from her cookbook (85 recipes)
- **Joe (Fergi)** - Administrator, manages general recipe collection (37 recipes)
- **Event Guests** - View recipes and respond to event invitations

### Technology Stack
- **Frontend:** Vanilla JavaScript, HTML5, CSS3
- **Backend:** Netlify Functions (Node.js)
- **Database:** Dropbox (recipes.json) + Local SQLite (recipes.db)
- **AI:** Anthropic Claude API (recipe formatting)
- **OCR:** Tesseract.js (image text extraction)
- **Hosting:** Netlify
- **Storage:** Dropbox API
- **Version Control:** GitHub

---

## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────┐
│           User Interface Layer                   │
│  (index.html, add-recipe.html, events.html)     │
└────────────────┬────────────────────────────────┘
                 │
                 │ HTTPS
                 │
┌────────────────▼────────────────────────────────┐
│         Netlify Functions Layer                  │
│  (19 serverless functions)                      │
│  - Recipe CRUD                                   │
│  - Event Management                              │
│  - AI Integration (Claude API)                   │
│  - OCR Processing (Tesseract.js)                │
│  - Contributor Management                        │
└────────────────┬────────────────────────────────┘
                 │
                 │ API Calls
                 │
┌────────────────▼────────────────────────────────┐
│           Data Storage Layer                     │
│                                                  │
│  ┌──────────────────┐  ┌─────────────────────┐│
│  │   Dropbox        │  │  Local SQLite       ││
│  │  recipes.json    │  │  recipes.db         ││
│  │  (Production)    │  │  (Development)      ││
│  └──────────────────┘  └─────────────────────┘│
└──────────────────────────────────────────────────┘
```

### Data Flow

#### Recipe Import Flow
```
User uploads file/photo
        ↓
extract-file.js (OCR if needed)
        ↓
format-recipe.js (Claude API)
        ↓
User selects contributor
        ↓
User reviews formatted recipe
        ↓
add-recipe.js saves to Dropbox
        ↓
Recipe appears in main view
```

#### Recipe Display Flow
```
User opens index.html
        ↓
get-recipes.js loads from Dropbox
        ↓
JavaScript renders recipe cards
        ↓
User clicks recipe
        ↓
get-recipe.js fetches details
        ↓
Modal displays full recipe
```

---

## Features

### Core Features (v4.0)

#### 1. Recipe Browsing
- **Recipe Cards Grid**
  - Responsive grid (3 cols desktop, 2 cols tablet, 1 col mobile)
  - Card displays: title, contributor, prep/cook time, servings, tags
  - Color-coded contributor badges (Janet = purple)
  - "Needs Review" warning badge (red)
  - Hover effects and animations

- **Search & Filtering**
  - Full-text search (title, ingredients, instructions)
  - Contributor filter dropdown (Janet, Fergi, etc.)
  - "Needs Review" filter (shows incomplete recipes)
  - Real-time filtering (no page reload)

- **Recipe Detail Modal** ✨ NEW v4.0: Mobile-optimized
  - Full-screen on mobile with smooth scrolling
  - Sticky header (title stays visible)
  - Formatted ingredients list
  - Step-by-step instructions with numbering
  - Cooking metadata (times, servings, difficulty)
  - Action buttons (Cooking Mode, Print, Edit)
  - iOS smooth scrolling enabled
  - 44x44px minimum touch targets

#### 2. Recipe Import ✨ NEW v4.0: Camera Integration
- **Four Import Methods:**
  1. **Camera Capture** (Mobile) - Direct photo capture
  2. **File Upload** - PDF, Word, Images, Text
  3. **Paste Text** - Copy/paste from websites
  4. **Manual Entry** - Type recipe directly

- **AI-Powered Formatting**
  - Automatic ingredient extraction
  - Instruction parsing and numbering
  - Metadata extraction (times, servings)
  - Smart text cleanup

- **OCR Processing**
  - Tesseract.js integration
  - Supports JPG, PNG images
  - 30-60 second processing time
  - Progress indicators

- **4-Step Import Wizard**
  1. Choose import method / upload file
  2. Select contributor
  3. Review AI-formatted recipe
  4. Final review and save

#### 3. Mobile Cooking Mode
- **Dedicated cooking.html interface**
- Large, readable text (18-28px)
- Big step numbers (40px circles)
- Checkable ingredient list
- Wake Lock API (screen stays on)
- Shareable URLs (cooking.html?recipe_id=X)
- "Cooking Mode" button in recipe detail

#### 4. Event Management
- **Create Events**
  - Event name, date, time, location
  - Recipe assignment (multiple recipes per event)
  - Guest list management

- **Guest Response System**
  - Public response page (respond.html?event_id=X)
  - Recipe preference selection
  - "Will bring" vs "Prefers" options
  - Custom dish names
  - Dietary restrictions
  - Volunteer categories

- **Event Dashboard**
  - Guest response tracking
  - Recipe assignments
  - Email generation with multiple copy methods
  - Response statistics

#### 5. Contributor Management
- **Public Access** (no authentication required)
- CRUD operations (Create, Read, Update, Delete)
- Contributor statistics (recipe counts)
- Automatic contributor assignment during import
- Filter recipes by contributor

#### 6. Data Management ✨ NEW v4.0
- **Cleanup Script** (scripts/cleanup_recipes.py)
  - Remove non-recipes (books, articles)
  - Fix OCR errors (l→1, O→0, etc.)
  - Standardize ingredients
  - Extract attributions to metadata
  - Verify contributor assignments
  - Flag incomplete recipes
  - Automatic backup
  - Comprehensive reporting

---

## Database Schema

### Recipe Object Schema

```json
{
  "id": 1,
  "title": "Baking Powder Biscuits",
  "description": "Traditional Southern-style biscuits",
  "ingredients": [
    "2 cups all-purpose flour",
    "1 tablespoon baking powder",
    "1 teaspoon salt",
    "1/2 cup cold butter, cubed",
    "3/4 cup whole milk"
  ],
  "instructions": [
    "Preheat oven to 450°F (230°C)",
    "In a large bowl, whisk together flour, baking powder, and salt",
    "Cut cold butter into flour mixture until it resembles coarse crumbs",
    "Make a well in center and pour in milk. Stir until just combined",
    "Turn dough onto floured surface and knead gently 3-4 times",
    "Pat dough to 3/4-inch thickness and cut into rounds",
    "Place on ungreased baking sheet and bake 10-12 minutes until golden"
  ],
  "prep_time_minutes": 15,
  "cook_time_minutes": 12,
  "total_time_minutes": 27,
  "servings": 12,
  "difficulty": "Easy",
  "cuisine_type": "American",
  "meal_type": "Side",
  "contributor": "Janet",
  "source_attribution": "Janet Mason's Cookbook",
  "tags": ["biscuits", "bread", "southern", "quick bread"],
  "calories_per_serving": 180,
  "notes": "Keep butter cold for flakier biscuits",
  "image_url": null,
  "created_at": "2025-01-15T10:30:00Z",
  "updated_at": "2025-11-04T14:22:00Z",
  "favorite": false,
  "rating": 5,
  "needs_review": false
}
```

### Event Object Schema

```json
{
  "id": 1,
  "name": "Thanksgiving Dinner 2025",
  "date": "2025-11-28",
  "time": "14:00",
  "location": "Ferguson House",
  "recipes": [5, 12, 23, 45],
  "guests": [
    {
      "name": "Murray",
      "email": "murray@example.com",
      "responses": {
        "5": {
          "type": "prefer",
          "recipe_id": 5,
          "custom_dish": null
        },
        "12": {
          "type": "will_bring",
          "recipe_id": 12,
          "custom_dish": "Fish (different than Beef Stroganoff)"
        }
      },
      "dietary_restrictions": "None",
      "will_bring_own_dish": false,
      "volunteer_categories": ["Setup"]
    }
  ],
  "created_at": "2025-10-15T10:00:00Z",
  "updated_at": "2025-11-01T12:00:00Z"
}
```

### Contributor Object Schema

```json
{
  "name": "Janet",
  "created_at": "2025-10-30T10:00:00Z",
  "recipe_count": 89
}
```

### Database Statistics

**Current Data (v4.0):**
- Total Recipes: 122
- Contributors:
  - Janet: 89 recipes
  - Fergi: 33 recipes
- Needs Review: 23 recipes
- Cuisine Types: American, Italian, Indian, Caribbean, French, etc.
- Meal Types: Main, Side, Dessert, Appetizer, Breakfast

---

## API Endpoints

### Recipe Endpoints

#### GET `/api/get-recipes`
**Description:** Get all recipes or search/filter

**Query Parameters:**
- `search` - Search query (title, ingredients, instructions)
- `contributor` - Filter by contributor name
- `needs_review` - Filter incomplete recipes (true/false)

**Response:**
```json
{
  "success": true,
  "recipes": [...],
  "count": 122
}
```

#### GET `/api/get-recipe?id={id}`
**Description:** Get single recipe by ID

**Response:**
```json
{
  "success": true,
  "recipe": {...}
}
```

#### PUT `/api/get-recipe?id={id}`
**Description:** Update single recipe

**Body:** Complete recipe object

**Response:**
```json
{
  "success": true,
  "recipe": {...}
}
```

#### POST `/api/add-recipe`
**Description:** Add new recipe

**Body:** Recipe object (without ID)

**Response:**
```json
{
  "success": true,
  "recipe_id": 123
}
```

#### POST `/api/update-recipe`
**Description:** Update existing recipe

**Body:** Recipe object with ID

**Response:**
```json
{
  "success": true,
  "recipe": {...}
}
```

#### POST `/api/save-recipes`
**Description:** Bulk save recipes to Dropbox

**Body:**
```json
{
  "recipes": [...]
}
```

#### GET `/api/load-recipes`
**Description:** Load recipes from Dropbox

**Response:**
```json
{
  "success": true,
  "recipes": [...]
}
```

#### GET `/api/statistics`
**Description:** Get recipe statistics

**Response:**
```json
{
  "success": true,
  "total_recipes": 122,
  "by_contributor": {
    "Janet": 89,
    "Fergi": 33
  },
  "by_cuisine": {...},
  "by_meal_type": {...}
}
```

### Import Endpoints

#### POST `/api/extract-file`
**Description:** Extract text from uploaded file (PDF, Word, Image, Text)

**Body:** FormData with file

**Response:**
```json
{
  "success": true,
  "text": "Extracted recipe text..."
}
```

#### POST `/api/format-recipe`
**Description:** Format recipe text using Claude AI

**Body:**
```json
{
  "text": "Raw recipe text..."
}
```

**Response:**
```json
{
  "success": true,
  "recipe": {
    "title": "...",
    "ingredients": [...],
    "instructions": [...]
  }
}
```

### Event Endpoints

#### POST `/api/create-event`
**Description:** Create or update event

**Body:** Event object

**Response:**
```json
{
  "success": true,
  "event": {...}
}
```

#### GET `/api/get-events`
**Description:** Get all events

**Response:**
```json
{
  "success": true,
  "events": [...]
}
```

#### POST `/api/save-events`
**Description:** Save events to Dropbox

**Body:**
```json
{
  "events": [...]
}
```

#### POST `/api/event-recipes`
**Description:** Manage recipes in event

**Body:**
```json
{
  "event_id": 1,
  "action": "add" | "remove",
  "recipe_id": 5
}
```

#### POST `/api/record-selection`
**Description:** Record guest recipe selection

**Body:**
```json
{
  "event_id": 1,
  "guest_name": "Murray",
  "guest_email": "murray@example.com",
  "recipe_id": 5,
  "selection_type": "prefer" | "will_bring",
  "custom_dish_name": "Fish",
  "dietary_restrictions": "None",
  "will_bring_own_dish": false,
  "volunteer_categories": ["Setup"]
}
```

#### POST `/api/generate-email`
**Description:** Generate event invitation email

**Body:**
```json
{
  "event": {...}
}
```

**Response:**
```json
{
  "success": true,
  "subject": "...",
  "body": "..."
}
```

### Contributor Endpoints

#### GET `/api/manage-contributors`
**Description:** Get all contributors

**Response:**
```json
{
  "success": true,
  "contributors": ["Janet", "Fergi", "Nancy", "Lauren"]
}
```

#### POST `/api/manage-contributors`
**Description:** Add new contributor

**Body:**
```json
{
  "action": "add",
  "name": "New Contributor"
}
```

### Authentication Endpoints (v3.1 - Backend Only)

#### POST `/api/send-verification-code`
**Description:** Send 6-digit verification code via email

**Body:**
```json
{
  "email": "user@example.com"
}
```

#### POST `/api/verify-code`
**Description:** Verify code and create session

**Body:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Note:** Authentication UI not yet implemented (Phase 2 pending).

---

## User Interface

### Pages

#### 1. index.html - Main Recipe Browser
**Purpose:** Browse and search recipes

**Sections:**
- Header with title and version
- Navigation bar with filters and search
- Recipe cards grid
- Recipe detail modal
- Dropbox status indicator

**Key Elements:**
- Search bar (full-text search)
- Contributor filter dropdown
- "Needs Review" filter button
- "Add Recipe" button
- Recipe cards (responsive grid)
- Recipe detail modal (mobile-optimized v4.0)

**Mobile Optimizations (v4.0):**
- Full-screen modal (100vh)
- Sticky recipe header
- Smooth scrolling
- 44x44px touch targets
- Vertical button stacks

#### 2. add-recipe.html - Recipe Import Wizard
**Purpose:** Import new recipes

**Steps:**
1. **Import Method**
   - Camera capture (mobile) ✨ NEW v4.0
   - File upload
   - Paste text

2. **Contributor Selection**
   - Choose existing contributor
   - Or add new contributor

3. **Format Recipe**
   - AI formats extracted text
   - Shows processing indicator
   - Displays formatted recipe preview

4. **Review & Save**
   - Edit if needed
   - Save to database
   - Return to main page

**Features:**
- 4-step progress indicator
- File type detection
- OCR progress feedback
- AI formatting status
- Form validation

#### 3. cooking.html - Mobile Cooking Mode
**Purpose:** Step-by-step cooking interface

**Features:**
- Large, readable text (18-28px)
- Big step numbers (40px circles)
- Ingredient checkboxes
- Wake Lock (screen stays on)
- Recipe title at top
- Progress through steps
- Shareable URL (cooking.html?recipe_id=X)

**Design:**
- Minimal distractions
- Maximum readability
- Optimized for 2-foot viewing distance
- Works offline after first load

#### 4. events.html - Event Management
**Purpose:** Create and manage cooking events

**Features:**
- Event list view
- Create new event button
- Event form (name, date, time, location)
- Recipe assignment interface
- Guest management
- Link to event dashboard

#### 5. event-detail.html - Event Dashboard
**Purpose:** View event details and guest responses

**Features:**
- Event information display
- Recipe list with assignments
- Guest response tracking
- Email generation
- Response statistics
- Multiple copy methods for email

#### 6. respond.html - Guest Response Page
**Purpose:** Public page for guests to respond

**Features:**
- Event information display
- Recipe selection interface
- Preference vs. Will Bring options
- Custom dish name input
- Dietary restrictions field
- Volunteer category selection
- Submit response button

**URL Format:** `respond.html?event_id=X`

### Design System

#### Colors
```css
--primary-color: #2c3e50;    /* Headers, text */
--secondary-color: #e74c3c;  /* Accent, buttons */
--accent-color: #3498db;     /* Links, highlights */
--success-color: #27ae60;    /* Success states */
--warning-color: #f39c12;    /* Warnings, alerts */
--background: #ecf0f1;       /* Page background */
--card-background: #ffffff;  /* Card backgrounds */
--text-color: #2c3e50;       /* Primary text */
--text-muted: #7f8c8d;       /* Secondary text */
--border-color: #bdc3c7;     /* Borders, dividers */
```

#### Typography
```css
/* Desktop */
--font-size-h1: 2.5rem;
--font-size-h2: 2rem;
--font-size-h3: 1.5rem;
--font-size-body: 1rem;
--line-height: 1.6;

/* Mobile (v4.0) */
--font-size-h2-mobile: 1.5rem;
--font-size-body-mobile: 1rem;
--line-height-mobile: 1.6;
```

#### Spacing
```css
--spacing-xs: 0.5rem;
--spacing-sm: 1rem;
--spacing-md: 2rem;
--spacing-lg: 3rem;

/* Mobile touch targets */
--touch-target-min: 44px;  /* iOS HIG */
```

#### Shadows
```css
--shadow: 0 2px 10px rgba(0,0,0,0.1);
--shadow-hover: 0 4px 20px rgba(0,0,0,0.15);
```

---

## Mobile UX

### Mobile-First Design Principles (v4.0)

#### 1. Touch Targets
- Minimum 44x44px (iOS Human Interface Guidelines)
- Applies to: buttons, links, close buttons, checkboxes
- Generous padding around interactive elements

#### 2. Scrolling
- iOS smooth scrolling enabled (`-webkit-overflow-scrolling: touch`)
- Full-screen modals on mobile (100vh)
- Sticky headers for context
- Bottom padding for comfortable scrolling

#### 3. Layout
- Single column on mobile (<768px)
- Vertical button stacks
- Column layout for metadata
- Full-width forms

#### 4. Typography
- Minimum 16px body text (prevents zoom on iOS)
- Larger headings (1.5rem on mobile)
- Comfortable line-height (1.6)
- Adequate contrast ratios

#### 5. Navigation
- Fixed navigation bar (sticky at top)
- Large tap targets for filters
- Clear visual hierarchy
- Breadcrumb trails

### Responsive Breakpoints

```css
/* Mobile First */
/* Base styles: 320px - 767px */

@media (min-width: 768px) {
  /* Tablet: 768px - 1023px */
  /* 2-column grid */
}

@media (min-width: 1024px) {
  /* Desktop: 1024px+ */
  /* 3-column grid */
}
```

### Device Testing Matrix

**iOS Devices (Priority):**
- iPhone SE (375x667)
- iPhone 12/13/14 (390x844)
- iPhone 14 Pro Max (430x932)
- iPhone 15 Pro (393x852)
- iPad Air (820x1180)

**Android Devices:**
- Pixel 6 (412x915)
- Samsung S21 (384x854)

**Browsers:**
- Safari iOS (primary)
- Chrome iOS
- Chrome Android

### Camera Integration (v4.0)

**Device Detection:**
```javascript
const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);
const hasCamera = 'mediaDevices' in navigator &&
                  'getUserMedia' in navigator.mediaDevices;
```

**Camera Input:**
```html
<input type="file" accept="image/*" capture="environment">
```

**Features:**
- Auto-shows on mobile devices
- Uses rear camera by default
- Fallback to photo picker if unavailable
- Integrates with existing OCR pipeline

---

## Data Management

### Storage Architecture

#### Production Storage: Dropbox
**Path:** `/Apps/Reference Refinement/recipes.json`
**Shared with:** Reference Refinement project
**Access:** OAuth 2.0 with auto-refresh tokens

**Advantages:**
- Real-time sync across devices
- No redeployment needed for data updates
- Shared data model with Reference Refinement
- Automatic backup and versioning
- Accessible from multiple projects

**Structure:**
```json
{
  "recipes": [...],
  "metadata": {
    "total_count": 122,
    "last_updated": "2025-11-04T14:30:00Z",
    "version": "4.0.0",
    "contributor_counts": {
      "Janet": 89,
      "Fergi": 33
    }
  }
}
```

#### Development Storage: SQLite
**Path:** `recipes.db` (local only)
**Purpose:** Local development and testing

**Tables:**
- recipes
- ingredients
- instructions
- tags
- cooking_log
- recipe_images
- recipes_fts (full-text search)

**Export:** `python3 export_to_json.py` → recipes.json

### Data Synchronization

**Upload to Dropbox:**
```bash
python3 upload_recipes_to_dropbox.py
```

**Netlify Function Access:**
- Functions read from Dropbox via OAuth
- Auto-refresh tokens (lib/dropbox-auth.js)
- No redeployment needed for data changes

### Backup Strategy

**Automatic Backups:**
- Cleanup script creates backup before changes
- Format: `recipes_backup_YYYYMMDD_HHMMSS.json`

**Manual Backups:**
```bash
# From Dropbox
python3 -c "
import dropbox, json, os
dbx = dropbox.Dropbox(os.environ['DROPBOX_ACCESS_TOKEN'])
_, res = dbx.files_download('/Apps/Reference Refinement/recipes.json')
with open('backup.json', 'wb') as f:
    f.write(res.content)
"
```

**Version Control:**
- All code in GitHub
- Tagged releases (v3.1.6, v4.0.0, etc.)
- Session summaries document changes

### Data Cleanup (v4.0)

**Script:** `scripts/cleanup_recipes.py`

**Operations:**
1. **Validation**
   - Verify recipe structure
   - Remove non-recipes (books, articles)
   - Check required fields

2. **OCR Error Fixing**
   - l → 1 (lowercase L to number)
   - O → 0 (uppercase O to zero)
   - ll → 11, OO → 00

3. **Standardization**
   - Ingredient formatting
   - Measurement units
   - Cooking times
   - Servings

4. **Attribution Extraction**
   - Move attributions from instructions to metadata
   - Patterns: "Recipe from X", "By X", "Source: X"

5. **Contributor Verification**
   - Ensure correct assignments
   - Expected: 85 Janet / 37 Fergi

6. **Metadata Validation**
   - Times: 0-720 minutes
   - Servings: 1-100
   - Required fields present

**Safety:**
- Automatic backup before execution
- Comprehensive validation
- Detailed reporting
- Can be run multiple times

**Usage:**
```bash
export DROPBOX_ACCESS_TOKEN="your_token"
python3 scripts/cleanup_recipes.py
```

---

## Deployment

### Netlify Configuration

**Site Name:** fergi-cooking
**URL:** https://fergi-cooking.netlify.app
**Build Command:** None (direct deployment)
**Publish Directory:** `.` (root)
**Functions Directory:** `netlify/functions`

**netlify.toml:**
```toml
[build]
  functions = "netlify/functions"
  publish = "."

[functions]
  # Include recipes.json in function bundles
  included_files = ["recipes.json", "netlify/functions/data/**"]

[[redirects]]
  from = "/api/*"
  to = "/.netlify/functions/:splat"
  status = 200
```

### Environment Variables

**Required in Netlify:**
```
DROPBOX_ACCESS_TOKEN=xxx           # Dropbox OAuth token
DROPBOX_REFRESH_TOKEN=xxx          # Auto-refresh token
DROPBOX_APP_KEY=xxx                # Dropbox app key
DROPBOX_APP_SECRET=xxx             # Dropbox app secret
ANTHROPIC_API_KEY=xxx              # Claude AI API key
```

### Deployment Commands

**Local Testing:**
```bash
netlify dev
# Opens at http://localhost:8888
```

**Deploy to Production:**
```bash
netlify deploy --prod --dir="." --message="Deploy message"
```

**Deploy Preview:**
```bash
netlify deploy --dir="." --message="Preview message"
```

### CI/CD Pipeline

**GitHub Integration:**
- Auto-deploy on push to `main` branch
- Preview deploys for pull requests
- Build logs in Netlify dashboard

**Deployment Process:**
1. Push to GitHub
2. Netlify detects change
3. Bundles functions (includes recipes.json)
4. Deploys functions (19 total)
5. Deploys static files
6. Updates live site

**Build Time:** ~7 seconds
**Function Bundle Time:** ~2 seconds

### Monitoring

**Netlify Dashboard:**
- Build logs: https://app.netlify.com/projects/fergi-cooking/deploys
- Function logs: https://app.netlify.com/projects/fergi-cooking/logs/functions
- Analytics: https://app.netlify.com/projects/fergi-cooking/analytics

**Key Metrics:**
- Page load time: <1s
- Function cold start: <500ms
- Function warm: <100ms
- Recipe modal load: <500ms

---

## Configuration

### File Structure

```
Cooking/
├── index.html                      # Main recipe browser
├── add-recipe.html                 # Recipe import wizard
├── cooking.html                    # Mobile cooking mode
├── events.html                     # Event management
├── event-detail.html               # Event dashboard
├── respond.html                    # Guest response page
├── recipes.json                    # Recipe data (122 recipes)
├── recipes.db                      # SQLite database (local)
├── netlify.toml                    # Netlify configuration
├── CLAUDE.md                       # Project documentation
├── DEPLOYMENT.md                   # Deployment guide
├── COOKING_SPECIFICATION.md        # This file
├── COOKING_HISTORY.md              # Version history
├── SESSION_SUMMARY_*.md            # Session documentation
├── QUICK_START_V4.0.md            # Quick reference
├── netlify/functions/              # 19 serverless functions
│   ├── lib/
│   │   └── dropbox-auth.js        # OAuth helper
│   ├── get-recipe.js              # Get/update single recipe
│   ├── get-recipes.js             # Get all/search recipes
│   ├── save-recipes.js            # Bulk save
│   ├── load-recipes.js            # Load from Dropbox
│   ├── add-recipe.js              # Add new recipe
│   ├── update-recipe.js           # Update recipe
│   ├── extract-file.js            # File text extraction
│   ├── format-recipe.js           # AI formatting
│   ├── manage-contributors.js     # Contributor CRUD
│   ├── create-event.js            # Create/update events
│   ├── get-events.js              # Get events
│   ├── save-events.js             # Save to Dropbox
│   ├── event-recipes.js           # Event recipe management
│   ├── record-selection.js        # Guest responses
│   ├── generate-email.js          # Event emails
│   ├── send-verification-code.js  # Email codes (v3.1)
│   ├── verify-code.js             # Validate codes (v3.1)
│   ├── statistics.js              # Recipe stats
│   └── data/
│       └── contributors.json      # Contributor list
├── scripts/
│   ├── cleanup_recipes.py         # Data cleanup script (v4.0)
│   ├── README_CLEANUP.md          # Cleanup documentation
│   ├── fix_contributors.py        # Contributor assignment
│   ├── reformat_instructions.py   # Instruction reformatter
│   ├── export_to_json.py          # DB to JSON export
│   └── upload_recipes_to_dropbox.py # Upload to Dropbox
└── *.pdf, *.pages                 # Original recipe files
```

### Dependencies

**Frontend:**
- No build step required
- Vanilla JavaScript (ES6+)
- HTML5, CSS3
- Web APIs: Fetch, File, MediaDevices

**Backend (Netlify Functions):**
```json
{
  "dependencies": {
    "@anthropic-ai/sdk": "^0.9.0",
    "dropbox": "^10.34.0",
    "pdf-parse": "^1.1.1",
    "mammoth": "^1.6.0",
    "tesseract.js": "^5.0.0"
  }
}
```

**Python Scripts:**
```
dropbox==11.36.2
```

### Version History

- **v1.0** - Initial SQLite database
- **v2.0** - Web interface and search
- **v2.8** - Event management
- **v3.0** - Recipe import wizard with AI
- **v3.1** - Contributor management, auth backend
- **v4.0** - Mobile UX fixes, camera integration ✨ Current

---

## Performance Specifications

### Target Metrics

**Page Load:**
- First Paint: <1.0s
- Time to Interactive: <2.0s
- Total Page Size: <500KB

**Recipe Modal:**
- Load time: <500ms
- Scroll performance: 60fps
- Touch response: <100ms

**Mobile Specific:**
- iOS smooth scrolling enabled
- Hardware acceleration for animations
- Optimized image loading
- Wake Lock for cooking mode

### Optimization Techniques

**Frontend:**
- Minimal external dependencies
- Inline critical CSS
- Lazy loading for images (future)
- Local storage caching (future)

**Backend:**
- Function warm starts (<100ms)
- Dropbox response caching (15min)
- Minimal function size
- Efficient data serialization

---

## Security

### Data Access
- **Public:** Recipe viewing, event responses
- **No Authentication:** Contributor management (public)
- **Backend Only:** Verification codes (v3.1, UI pending)

### API Security
- CORS enabled for Netlify domains
- API keys in environment variables
- Dropbox OAuth with auto-refresh
- Rate limiting via Netlify

### Data Privacy
- No user tracking
- No analytics
- No cookies (except wake lock)
- Guest emails stored in Dropbox only

---

## Future Enhancements

### v4.1 - Enhanced Cooking Mode
- Three-mode architecture
- Step-by-step navigation
- Embedded ingredients per step
- Progress indicators
- Swipe gestures

### v4.2 - Timer Integration
- Web-based timers
- Notification API
- Audio alerts
- Haptic feedback
- Multiple concurrent timers

### v4.3 - Desktop Polish
- Two-column layout
- Sticky ingredients sidebar
- Generous typography
- Enhanced print styles

### v5.0 - Advanced Features (Future)
- Voice control ("Hey Siri, next step")
- Recipe photos
- Meal planning
- Grocery list generation
- Social features (sharing, ratings)
- Apple Watch companion app

---

## Appendix

### Browser Support

**Desktop:**
- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

**Mobile:**
- Safari iOS 14+ ✅ (Primary)
- Chrome iOS 90+ ✅
- Chrome Android 90+ ✅

### Known Limitations

- No offline support (requires network)
- No user authentication (public access)
- No recipe photos (text only)
- No nutritional calculation
- No recipe scaling
- No print-to-PDF

### Support & Maintenance

**Issue Tracking:** GitHub Issues
**Documentation:** CLAUDE.md, session summaries
**Updates:** As needed, no fixed schedule
**Backup:** Automatic via Dropbox, manual on demand

---

**Technical Specification**
**Version:** v4.0.0
**Last Updated:** November 4, 2025
**Status:** ✅ Production Ready
**Maintained By:** Fergi (Joe Ferguson)
**AI Assistant:** Claude Code (Anthropic)
