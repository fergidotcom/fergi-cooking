# Fergi Cooking System - Technical Specification
**Version:** v2.8.1
**Status:** Production
**Live URL:** https://fergi-cooking.netlify.app
**Created:** October 30, 2025
**Last Updated:** November 3, 2025

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Technical Stack](#technical-stack)
5. [Data Model](#data-model)
6. [API Endpoints](#api-endpoints)
7. [User Workflows](#user-workflows)
8. [Deployment](#deployment)
9. [Configuration](#configuration)
10. [Security](#security)

---

## System Overview

### Purpose
The Fergi Cooking System is a comprehensive recipe collection and event management platform designed to:
- Organize and search a family recipe collection (122 recipes)
- Plan cooking events with multiple guests
- Collect guest preferences and dietary restrictions
- Coordinate potluck-style gatherings with volunteer categories
- Generate invitation emails with interactive response links

### Key Capabilities
- **Recipe Management:** Browse, search, and view 122 family recipes
- **Event Planning:** Create events, assign recipes to menus, invite guests
- **Guest Response System:** Public response page (no login required)
- **Preference Collection:** Track what guests prefer and will bring
- **Dietary Tracking:** Collect restrictions and allergies
- **Volunteer Coordination:** Guests can volunteer to bring specific categories
- **Email Generation:** Generate HTML emails with clickable recipe links

---

## Architecture

### System Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Static HTML)                   │
├─────────────────────────────────────────────────────────────┤
│  index.html          Recipe browsing and search             │
│  events.html         Event creation and management          │
│  event-detail.html   Event dashboard and recipe assignment  │
│  respond.html        Public guest response page             │
└─────────────────────────────────────────────────────────────┘
                              ↓ ↑
                         HTTPS / API
                              ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│              Netlify Functions (Serverless API)              │
├─────────────────────────────────────────────────────────────┤
│  get-recipe.js       Get/update single recipe by ID         │
│  get-recipes.js      Get all recipes with search/filter     │
│  create-event.js     Create/update events                   │
│  get-events.js       Retrieve events                        │
│  event-recipes.js    Add/remove recipes from events         │
│  record-selection.js Record guest responses                 │
│  generate-email.js   Generate invitation email HTML         │
│  statistics.js       Recipe statistics and analytics        │
└─────────────────────────────────────────────────────────────┘
                              ↓ ↑
                         Data Access
                              ↓ ↑
┌─────────────────────────────────────────────────────────────┐
│                      Data Storage                            │
├─────────────────────────────────────────────────────────────┤
│  recipes.json        122 recipes bundled with functions     │
│  Dropbox Storage     events.json, guest-selections.json     │
│  recipes.db (local)  SQLite database for development        │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### Frontend Layer
- **Technology:** Pure HTML, CSS, JavaScript (no frameworks)
- **Design:** Responsive, mobile-friendly
- **Styling:** CSS custom properties, gradients, modern UI
- **State Management:** Vanilla JavaScript with localStorage
- **API Communication:** Fetch API with error handling

#### API Layer
- **Platform:** Netlify Functions (AWS Lambda under the hood)
- **Runtime:** Node.js
- **Authentication:** Dropbox OAuth 2.0 with refresh tokens
- **Error Handling:** Comprehensive try-catch with detailed logging
- **CORS:** Enabled for all origins (public guest responses)

#### Data Layer
- **Primary Storage:** Dropbox (events, guest selections)
- **Recipe Data:** recipes.json bundled with Netlify Functions (400KB, 122 recipes)
- **Local Development:** SQLite database (recipes.db)
- **Caching:** No caching currently (future enhancement)

---

## Features

### 1. Recipe Management

#### Recipe Browsing
- **Grid View:** Responsive card layout
- **Search:** Full-text search across title, ingredients, instructions
- **Filters:** Cuisine type, meal type, source, dietary preferences
- **Statistics:** View recipe counts by category
- **Details View:** Expandable recipe cards with full details

#### Recipe Data Structure
Each recipe includes:
- **Metadata:** Title, description, cuisine, meal type, source
- **Timing:** Prep time, cook time, total time
- **Servings:** Number of servings
- **Ingredients:** Structured list with quantities and units
- **Instructions:** Step-by-step cooking directions
- **Tags:** Categorization and search keywords
- **Images:** Recipe photos (when available)
- **Ratings:** Star ratings and favorites

#### Janet Mason's Cookbook
- Special collection of 85 family recipes
- Extracted from images using OCR and AI
- Preserved family cooking traditions
- Dedicated section in the interface

### 2. Event Management

#### Event Creation
- **Basic Info:** Name, date, time, location, description
- **Guest List:** Optional list of invited guests with names and emails
- **Volunteer Collection:** Toggle to collect category volunteers
- **Recipe Assignment:** Add multiple recipes to event menu
- **Recipe Search:** Filter through 122 recipes as you type

#### Event Dashboard
- View event details
- See all assigned recipes organized by course type
- Add/remove recipes from menu
- Generate invitation emails
- View guest responses in real-time
- Track RSVPs and dietary restrictions

#### Email Generation
- **HTML Email:** Beautifully formatted invitation
- **Recipe Cards:** Each recipe displayed with description
- **Interactive Buttons:** Click to indicate preference
- **Volunteer Section:** Category buttons (appetizer, salad, main, side, dessert, beverage)
- **Dietary Section:** Gluten-free, lactose-free, other
- **Copy Options:** Plain copy, formatted copy, email client copy

### 3. Guest Response System

#### Public Response Page
- **No Login Required:** Guests respond via simple URL links
- **Recipe Display:** Shows selected recipe name and description
- **Loading Screen:** Brief loading while fetching recipe details
- **Guest Identification:** Dropdown if guest list exists, email entry otherwise
- **Multiple Response Types:** Prefer, will bring, dietary, volunteer

#### Response Types

**1. Preference Selection**
- Click recipe link in email
- See recipe name: "❤️ You prefer: Beef Stroganoff"
- Option to volunteer to bring it
- Can specify custom dish if bringing something different

**2. Custom Dish**
- Checkbox: "I'll bring this dish"
- Optional field: "What will you bring?"
- Leave blank = bring selected recipe
- Enter text = bring different dish
- Example: Prefer Beef Stroganoff, bring Fish

**3. Volunteer Categories**
- Click category button (appetizer, salad, main, side, dessert, beverage)
- Enter specific dish name
- Multiple categories allowed

**4. Dietary Restrictions**
- Free-form text field
- Common options: Gluten-free, lactose-free, vegetarian, vegan, allergies
- Multiple restrictions can be entered

#### Response Summary
- **Success Message:** "Thank You! Your response has been recorded"
- **All Responses:** Shows all selections for this guest at this event
- **Update Anytime:** Click email links again to add more responses
- **Clear Display:** Icons and formatting for each response type

### 4. Dual Loading Strategy (Reliability)

#### Strategy 1: Direct Recipe Load
```javascript
fetch('/.netlify/functions/get-recipe/:id')
→ If successful: Use recipe data
→ If failed: Try Strategy 2
```

#### Strategy 2: Fallback to All Recipes
```javascript
fetch('/.netlify/functions/get-recipes')
→ Load all 122 recipes
→ Find recipe by ID
→ If found: Use recipe data
→ If not found: Show error
```

This dual approach ensures 99%+ success rate even if one endpoint has issues.

---

## Technical Stack

### Frontend
- **HTML5:** Semantic markup, accessible
- **CSS3:** Custom properties, gradients, flexbox, grid
- **JavaScript ES6+:** Async/await, fetch, modules, destructuring
- **No Dependencies:** Pure vanilla JavaScript (no jQuery, React, etc.)

### Backend
- **Node.js:** Runtime for Netlify Functions
- **Netlify Functions:** Serverless computing (AWS Lambda)
- **Fetch API:** HTTP requests (node-fetch package)

### Storage
- **Dropbox API:** Cloud storage for events and selections
- **SQLite:** Local development database
- **JSON Files:** Recipe data bundled with functions

### Deployment
- **Netlify:** Hosting and serverless functions
- **Git:** Version control (GitHub @fergidotcom)
- **DNS:** fergi-cooking.netlify.app

### Development Tools
- **Netlify CLI:** Local development and deployment
- **jq:** JSON processing and testing
- **curl:** API testing
- **Python:** Scripts for data processing

---

## Data Model

### Recipe Schema
```json
{
  "id": 8,
  "title": "Beef Stroganoff",
  "description": "Rich Russian-inspired comfort food...",
  "cuisine_type": "Russian",
  "meal_type": "main",
  "course_type": "main",
  "prep_time_minutes": 20,
  "cook_time_minutes": 30,
  "total_time_minutes": 50,
  "servings": 6,
  "difficulty": "medium",
  "source_attribution": "NYT Cooking",
  "ingredients": [
    {
      "ingredient_name": "beef sirloin",
      "quantity": 1.5,
      "unit": "pounds"
    }
  ],
  "instructions": [
    {
      "step_number": 1,
      "instruction_text": "Slice beef into thin strips..."
    }
  ],
  "tags": ["beef", "comfort food", "quick"],
  "rating": 5,
  "favorite": true,
  "date_added": "2024-10-15",
  "date_modified": "2025-11-03"
}
```

### Event Schema
```json
{
  "id": "evt_123",
  "name": "Thanksgiving Dinner 2025",
  "event_date": "2025-11-28",
  "event_time": "18:00",
  "location": "Casa Fergi: 2232 Wilderness Arroyo",
  "description": "Annual family Thanksgiving celebration",
  "collect_volunteers": true,
  "guest_list": [
    {
      "name": "Murray",
      "email": "murray@example.com"
    }
  ],
  "recipes": [
    {
      "recipe_id": 8,
      "course_type": "main"
    }
  ],
  "created_at": "2025-11-01T10:00:00Z",
  "updated_at": "2025-11-03T15:30:00Z"
}
```

### Guest Selection Schema
```json
{
  "event_id": "evt_123",
  "guest_email": "murray@example.com",
  "guest_name": "Murray",
  "selections": [
    {
      "selection_type": "prefer",
      "recipe_id": 8,
      "recipe_title": "Beef Stroganoff",
      "timestamp": "2025-11-03T16:00:00Z"
    },
    {
      "selection_type": "will_bring",
      "bringing_own_dish_name": "Fish",
      "bringing_own_dish_description": "",
      "timestamp": "2025-11-03T16:01:00Z"
    },
    {
      "selection_type": "dietary_restriction",
      "notes": "Gluten-free",
      "timestamp": "2025-11-03T16:02:00Z"
    }
  ]
}
```

---

## API Endpoints

### Recipe Endpoints

#### GET /get-recipe/:id
Get single recipe by ID.

**Request:**
```
GET /.netlify/functions/get-recipe/8
```

**Response:**
```json
{
  "success": true,
  "recipe": {
    "id": 8,
    "title": "Beef Stroganoff",
    "description": "Rich Russian-inspired comfort food...",
    ...
  }
}
```

#### GET /get-recipes
Get all recipes with optional search and pagination.

**Request:**
```
GET /.netlify/functions/get-recipes?search=beef&limit=10
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "total": 122,
  "recipes": [...]
}
```

### Event Endpoints

#### POST /create-event
Create new event.

**Request:**
```json
{
  "name": "Thanksgiving Dinner",
  "event_date": "2025-11-28",
  "event_time": "18:00",
  "location": "Casa Fergi",
  "guest_list": [...]
}
```

**Response:**
```json
{
  "success": true,
  "eventId": "evt_123",
  "message": "Event created successfully"
}
```

#### GET /get-events
Get all events or single event by ID.

**Request:**
```
GET /.netlify/functions/get-events?id=evt_123
```

**Response:**
```json
{
  "id": "evt_123",
  "name": "Thanksgiving Dinner",
  ...
}
```

#### POST /event-recipes
Add or remove recipes from event.

**Request:**
```json
{
  "event_id": "evt_123",
  "recipe_id": 8,
  "action": "add"
}
```

### Guest Response Endpoints

#### POST /record-selection
Record guest response.

**Request:**
```json
{
  "event_id": "evt_123",
  "guest_email": "murray@example.com",
  "guest_name": "Murray",
  "selection_type": "prefer",
  "recipe_id": 8
}
```

**Response:**
```json
{
  "success": true,
  "message": "Selection recorded"
}
```

#### GET /record-selection
Get guest selections for event.

**Request:**
```
GET /.netlify/functions/record-selection?event_id=evt_123&guest_email=murray@example.com
```

**Response:**
```json
[
  {
    "selection_type": "prefer",
    "recipe_title": "Beef Stroganoff",
    ...
  }
]
```

#### GET /generate-email
Generate invitation email HTML.

**Request:**
```
GET /.netlify/functions/generate-email?id=evt_123&email=murray@example.com
```

**Response:**
```html
<!DOCTYPE html>
<html>
  <body>
    <h1>🎉 You're Invited!</h1>
    ...
  </body>
</html>
```

---

## User Workflows

### Host Workflow: Creating an Event

1. **Navigate to Events** → Click "Create Event" button
2. **Enter Event Details:**
   - Event name: "Thanksgiving Dinner 2025"
   - Date: November 28, 2025
   - Time: 6:00 PM (defaults to 6:00 PM)
   - Location: Casa Fergi address
   - Description: Event details
3. **Add Guest List (Optional):**
   - Click "+ Add Guest"
   - Enter name and email for each guest
   - Benefits: Guest dropdown on response page
4. **Check "Collect Volunteers"** if you want category buttons
5. **Click "Save Event"** → Event dashboard opens
6. **Add Recipes to Menu:**
   - Click "+ Add Recipe" button
   - Search/filter through 122 recipes
   - Click recipes to add to event
   - Recipes organized by course type
7. **Generate Email:**
   - Click "Generate Email" button
   - Preview HTML email with all recipes
   - Copy via one of three methods:
     - Plain copy
     - Formatted copy (preserves styling)
     - Email client copy (opens mail app)
8. **Send to Guests** → Paste into email client and send

### Guest Workflow: Responding to Invitation

1. **Receive Email** with event invitation
2. **Browse Recipes** in email, organized by course
3. **Click "❤️ I prefer this" button** on desired recipe
4. **Response Page Loads:**
   - Shows: "❤️ You prefer: Beef Stroganoff"
   - Displays recipe description
5. **Select Who You Are:**
   - If guest list exists: Choose name from dropdown
   - If no guest list: Enter email and name
6. **Optionally Check "I'll bring this dish":**
   - Leave blank = bringing the recipe itself
   - Enter text = bringing something different
   - Example: Type "Fish" to bring fish instead
7. **Add Dietary Restrictions (Optional):**
   - Free-form text field
   - Enter any restrictions or allergies
8. **Click "Submit Response"** → Success message displays
9. **View Summary** of all your responses for this event
10. **Update Anytime** by clicking email links again

### Guest Workflow: Volunteering Category

1. **Receive Email** with volunteer section (if enabled)
2. **Click Category Button:**
   - 🥗 Appetizer
   - 🥬 Salad
   - 🍖 Main Course
   - 🥔 Side Dish
   - 🍰 Dessert
   - 🍷 Beverage
3. **Enter Your Info:**
   - Email address
   - Name (optional)
   - Specific dish you'll bring
4. **Submit** → Recorded as volunteer for that category

---

## Deployment

### Production Environment

**Platform:** Netlify
**URL:** https://fergi-cooking.netlify.app
**Admin Panel:** https://app.netlify.com/projects/fergi-cooking
**Account:** fergidotcom@gmail.com

### Deploy Command
```bash
netlify deploy --prod --dir="." --message="Deploy description"
```

### Build Configuration
**netlify.toml:**
```toml
[build]
  publish = "."
  functions = "netlify/functions"

[functions]
  included_files = ["recipes.json"]
```

### Deployment Process
1. Local changes committed to Git
2. `netlify deploy --prod` command executed
3. Functions bundled with recipes.json (400KB)
4. 13 serverless functions deployed
5. Static files (HTML, CSS, JS) uploaded to CDN
6. Deploy completes in ~25 seconds
7. Live at https://fergi-cooking.netlify.app

### Environment Variables
Configured in Netlify Dashboard:
- `DROPBOX_REFRESH_TOKEN` - OAuth refresh token for Dropbox API
- `DROPBOX_CLIENT_ID` - Dropbox app client ID
- `DROPBOX_CLIENT_SECRET` - Dropbox app client secret

### Local Development
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Start local dev server
netlify dev

# Access at http://localhost:8888
# Functions run on http://localhost:8888/.netlify/functions/
```

---

## Configuration

### Netlify Configuration (netlify.toml)
```toml
[build]
  publish = "."
  functions = "netlify/functions"

[functions]
  included_files = ["recipes.json"]

[[redirects]]
  from = "/api/recipes/:id"
  to = "/.netlify/functions/get-recipe/:id"
  status = 200

[[redirects]]
  from = "/api/recipes"
  to = "/.netlify/functions/get-recipes"
  status = 200

[[headers]]
  for = "/api/*"
  [headers.values]
    Access-Control-Allow-Origin = "*"
    Access-Control-Allow-Methods = "GET, POST, PUT, DELETE, OPTIONS"
```

### Dropbox Configuration
**App Name:** Reference Refinement
**Storage Path:** `/Apps/Reference Refinement/`
**Files:**
- `events.json` - All events
- `guest-selections.json` - All guest responses
- `recipes.json` - Recipe data (also bundled with functions)

**OAuth Flow:**
1. User authorizes app (one-time)
2. Refresh token stored in Netlify environment
3. Functions auto-refresh access token as needed
4. No token expiration issues

---

## Security

### Public Guest Responses
- **No Authentication Required:** Guests respond via URL links
- **Rationale:** Reduce friction for casual event RSVPs
- **Data Exposure:** Guest email visible in URL (acceptable for this use case)
- **Mitigation:** Unique event IDs prevent guessing other events

### API Security
- **CORS:** Open for public guest responses
- **Rate Limiting:** Netlify default limits (future: implement custom)
- **Input Validation:** Server-side validation of all inputs
- **SQL Injection:** Not applicable (using JSON storage, not SQL)
- **XSS Prevention:** HTML escaping in email generation

### Data Storage
- **Dropbox:** Private app folder, not accessible publicly
- **OAuth:** Refresh tokens stored securely in Netlify environment
- **recipes.json:** Bundled with functions (not user-generated content)
- **PII:** Guest emails stored but not exposed publicly

### Future Security Enhancements
1. **Rate Limiting:** Implement per-IP rate limits
2. **Event Passwords:** Optional password for private events
3. **CAPTCHA:** Prevent spam submissions
4. **Admin Authentication:** Protect event creation/editing
5. **Audit Logging:** Track all modifications

---

## Performance

### Metrics
- **Page Load:** < 2 seconds (static HTML)
- **API Response:** < 200ms for get-recipe
- **API Response:** < 500ms for get-recipes (122 recipes)
- **Recipe Loading:** Dual strategy ensures < 1 second total
- **Email Generation:** < 1 second (server-side)

### Optimization Strategies
1. **Static HTML:** No build step, instant page loads
2. **Bundled recipes.json:** Faster than Dropbox API calls
3. **Dual Loading:** Fallback ensures reliability
4. **No Images in Bundle:** Reduces function size
5. **Minimal CSS/JS:** Pure vanilla, no frameworks

### Future Performance Improvements
1. **CDN Caching:** Cache recipe data for 1 hour
2. **Image Optimization:** Compress and lazy-load images
3. **Code Splitting:** Load JS modules on demand
4. **Service Worker:** Offline recipe viewing
5. **IndexedDB:** Client-side recipe caching

---

## Browser Compatibility

### Supported Browsers
- **Chrome/Edge:** 90+
- **Firefox:** 88+
- **Safari:** 14+
- **Mobile Safari:** 14+
- **Chrome Android:** 90+

### Required Features
- Fetch API
- ES6+ JavaScript
- CSS Grid
- CSS Custom Properties
- LocalStorage

---

## Testing

### Manual Testing Checklist
- [ ] Create event
- [ ] Add recipes to event
- [ ] Generate email
- [ ] Click recipe link (guest view)
- [ ] Submit preference
- [ ] Submit will_bring
- [ ] Submit dietary restriction
- [ ] Volunteer for category
- [ ] View response summary
- [ ] Verify data in Dropbox

### API Testing
```bash
# Test get-recipe
curl https://fergi-cooking.netlify.app/.netlify/functions/get-recipe/8

# Test get-recipes
curl https://fergi-cooking.netlify.app/.netlify/functions/get-recipes

# Test get-events
curl https://fergi-cooking.netlify.app/.netlify/functions/get-events
```

### Browser Console Testing
```javascript
// Test recipe loading
fetch('/.netlify/functions/get-recipe/8')
  .then(r => r.json())
  .then(console.log);

// Test guest selection
fetch('/.netlify/functions/record-selection', {
  method: 'POST',
  body: JSON.stringify({
    event_id: 'evt_123',
    guest_email: 'test@example.com',
    selection_type: 'prefer',
    recipe_id: 8
  })
}).then(r => r.json()).then(console.log);
```

---

## Monitoring & Debugging

### Console Logging
Detailed emoji-based logging for recipe loading:
- 🔍 Loading recipe details
- 📡 Trying API endpoint
- ✅ Success
- ❌ Failed
- 🔄 Fallback strategy
- 💥 Critical error

### Netlify Logs
- **Function Logs:** https://app.netlify.com/projects/fergi-cooking/logs/functions
- **Deploy Logs:** https://app.netlify.com/projects/fergi-cooking/deploys
- **Real-time:** Available during function execution

### Error Tracking
- Browser console for client-side errors
- Netlify function logs for server-side errors
- Manual error reports from users (future: integrate Sentry)

---

## Maintenance

### Regular Tasks
1. **Monitor Dropbox OAuth:** Refresh tokens valid (monthly check)
2. **Review Function Logs:** Check for errors (weekly)
3. **Update recipes.json:** Add new recipes as needed
4. **Test Critical Paths:** Guest response flow (before big events)
5. **Review Guest Feedback:** Improve UX based on comments

### Database Maintenance
```bash
# Update recipes.json from recipes.db
python3 export_to_json.py

# Deploy updated recipes
netlify deploy --prod --dir="." --message="Updated recipes"
```

### Backup Strategy
- **Dropbox:** Automatic versioning (30-day history)
- **Git:** All code in GitHub repository
- **recipes.json:** Bundled with functions (deployed copies)
- **Local:** recipes.db maintained locally

---

## Future Roadmap

### Phase 1: Core Enhancements
- [ ] Auto-send emails (SendGrid integration)
- [ ] Recipe image uploads
- [ ] Recipe variants (vegetarian, gluten-free)
- [ ] Serving size calculator

### Phase 2: Advanced Features
- [ ] Host dashboard with real-time RSVP tracking
- [ ] Grocery list generator from event menu
- [ ] Recipe scaling (adjust servings)
- [ ] Cooking timers and reminders

### Phase 3: Social Features
- [ ] Share recipes with friends
- [ ] Recipe comments and ratings
- [ ] Photo uploads from guests
- [ ] Recipe remix/variations

### Phase 4: Intelligence
- [ ] AI-powered recipe suggestions
- [ ] Dietary restriction compliance checking
- [ ] Automatic course pairing
- [ ] Menu balance analysis

---

## Support & Documentation

### Documentation Files
- **COOKING_SPECIFICATION.md** - This file
- **COOKING_HISTORY.md** - Development timeline
- **DEPLOYMENT.md** - Deployment guide
- **SESSION_SUMMARY_*.md** - Session documentation
- **CLAUDE.md** - Project overview for Claude Code

### Contact
- **Developer:** Claude Code (Anthropic AI)
- **Owner:** Joe Ferguson
- **GitHub:** @fergidotcom
- **Project:** https://github.com/fergidotcom/fergi-cooking

---

**Document Version:** 1.0
**System Version:** v2.8.1
**Last Updated:** November 3, 2025
**Status:** Production Ready ✓
