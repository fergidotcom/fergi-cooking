# Cooking App Session Checkpoint - Pre-v4.0

**Date:** November 4, 2025
**Current Version:** v3.1.6
**Next Version:** v4.0.0
**Purpose:** Comprehensive checkpoint before major mobile UX overhaul

---

## 📊 Context Usage

**Current:** ~47,000 / 200,000 tokens (~24% used, 76% remaining)
**Status:** ✅ Healthy - Plenty of room for v4.0 implementation

---

## 📍 Current State Summary

### System Status
- **Production URL:** https://fergi-cooking.netlify.app
- **Database:** 122 recipes (89 Janet, 33 Fergi, 23 need review)
- **Netlify Functions:** 19 deployed and operational
- **Last Deploy:** v3.1.6 - November 4, 2025

### Recent Work (v3.1.4 - v3.1.6)
1. ✅ **v3.1.6** - Needs Review filter implemented
   - 23 recipes flagged as incomplete
   - Red warning badges on recipe cards
   - Filter shows missing ingredients/instructions

2. ✅ **v3.1.5** - Contributor display bugfix
   - Recipe cards show proper contributor names
   - Fixed source_attribution vs contributor confusion

3. ✅ **v3.1.4** - Contributor assignment fix
   - All 122 recipes assigned contributors
   - Renamed "Janet Mason" to "Janet"
   - Fixed contributor filter functionality

### Key Features Currently Working
- Recipe browsing with search and filters
- Contributor management and filtering
- Event management system
- Guest response collection
- Recipe import wizard (PDF, Word, Images, Text)
- AI-powered recipe formatting
- Mobile cooking mode (cooking.html)
- Wake Lock API for screen-on while cooking
- Print-optimized recipe layout

---

## 🚨 Critical Issues Identified for v4.0

### 1. **CRITICAL: Mobile Modal Broken**
**Severity:** BLOCKING - Users cannot read recipes on mobile

**Problem:**
- Recipe detail modal shows only ~30% of content on iPhone
- Content is cut off and unscrollable
- Affects all mobile users (primary use case)

**Root Cause:**
- Modal using fixed positioning without proper viewport constraints
- No overflow handling for mobile screens
- Missing touch-optimized scrolling

**Impact:**
- Janet (primary user) cannot use app effectively on iPhone
- Mobile cooking mode is great, but browsing is broken

### 2. **Data Quality Issues**
**Severity:** HIGH - Affects user experience

**Problems:**
- At least one non-recipe entry (book) in database
- Instructions contain attributions that should be metadata
- Inconsistent formatting across recipes
- OCR errors from Janet Mason image imports
- Contributor counts may need verification (should be 85/37 not 89/33)

### 3. **Missing Mobile Optimizations**
**Severity:** MEDIUM - Feature gap

**Missing:**
- Camera integration for recipe capture
- Step-by-step cooking navigation
- Timer integration with notifications
- Progressive disclosure of recipe information
- Touch-optimized gestures

---

## 📋 v4.0 Implementation Plan

### Overview
Based on comprehensive UX analysis documents in ~/Downloads/:
- COOKING_v3_1_COMPREHENSIVE_MOBILE_UX_ANALYSIS.md
- COOKING_v3_1_MOBILE_UX_COMPLETE_ANALYSIS.md
- COOKING_v3_1_CLEANUP_AND_RESPONSIVE_INSTRUCTIONS.md

### Phase Breakdown

#### **Phase 1: Fix Mobile Modal (IMMEDIATE - 2 hours)**
**Priority:** P0 - BLOCKING

**Tasks:**
1. Fix modal overflow issue - proper scrolling
2. Implement viewport constraints for iOS safe areas
3. Add scroll indicators
4. Ensure 44x44px minimum touch targets
5. Test on iPhone Safari emulation

**Files to Update:**
- `index.html` - Modal CSS fixes
- Create `/styles/mobile-responsive.css`

**Success Criteria:**
- ✅ 100% of recipe content visible on mobile
- ✅ Smooth 60fps scrolling
- ✅ Close button accessible
- ✅ Touch targets meet iOS guidelines

#### **Phase 2: Data Cleanup Script (4 hours)**
**Priority:** P0 - Critical for data integrity

**Tasks:**
1. Create `scripts/cleanup_recipes.py`
2. Remove non-recipes (book entries)
3. Extract attributions from instructions → metadata
4. Fix OCR errors (l→1, O→0, etc.)
5. Verify contributor counts (85 Janet, 37 Fergi)
6. Embed ingredient quantities in instructions
7. Create backup before running
8. Generate cleanup report

**New Files:**
- `/scripts/cleanup_recipes.py`
- `/scripts/cleanup_report.txt` (generated)

**Success Criteria:**
- ✅ 0 non-recipes in database
- ✅ 85/37 contributor split correct
- ✅ All ingredients standardized
- ✅ Attributions in metadata fields

#### **Phase 3: Mobile Camera Integration (3 hours)**
**Priority:** P1 - High value feature

**Tasks:**
1. Add camera capture to add-recipe.html
2. Implement file input with camera access
3. Support both rear/front camera
4. Process with existing OCR pipeline
5. Test on iOS/Android

**Files to Update:**
- `add-recipe.html` - Add camera capture UI
- `/netlify/functions/extract-file.js` - Handle camera images

**Implementation:**
```html
<input type="file" accept="image/*" capture="environment">
```

**Success Criteria:**
- ✅ Camera launches on mobile devices
- ✅ Photos processed with OCR
- ✅ Works on iOS Safari and Android Chrome

#### **Phase 4: Three-Mode Mobile Architecture (8 hours)**
**Priority:** P1 - Major UX improvement

**Modes:**
1. **Discovery Mode** - Recipe browsing (existing)
2. **Planning Mode** - Full recipe view with checkable ingredients
3. **Cooking Mode** - Step-by-step with large text (enhance existing)

**Tasks:**
1. Build step-by-step navigation
2. Implement embedded ingredient display per step
3. Add progress indicators (dots)
4. Enable swipe gestures
5. Enhance wake lock implementation

**New Files:**
- `/scripts/cooking-mode.js`
- `/styles/cooking-mode.css`

**Success Criteria:**
- ✅ Step navigation with large 32px text
- ✅ Embedded ingredients per step
- ✅ Swipe gestures working
- ✅ Progress indicators visible

#### **Phase 5: Timer Integration (4 hours)**
**Priority:** P2 - Nice to have

**Tasks:**
1. Web-based timers with Notification API
2. Audio alerts using Web Audio API
3. Haptic feedback for iOS
4. Background persistence with service worker
5. Visual countdown with progress ring
6. Multiple concurrent timers

**New Files:**
- `/scripts/timer-manager.js`
- `/timer-worker.js` (service worker)

**Success Criteria:**
- ✅ Timers work with notifications
- ✅ Audio alerts functional
- ✅ Multiple timers supported
- ✅ Background persistence

#### **Phase 6: Desktop Generous Layout (3 hours)**
**Priority:** P2 - Polish

**Tasks:**
1. Two-column desktop layout
2. Fixed 420px ingredients sidebar (sticky)
3. Scrollable instructions with embedded ingredients
4. 20px base font size
5. 48px spacing between steps

**Files to Update:**
- `index.html` - Desktop layout CSS
- `/styles/desktop-layout.css`

**Success Criteria:**
- ✅ Ingredients sidebar sticky
- ✅ Large readable fonts
- ✅ Generous spacing
- ✅ Print-optimized

---

## 📁 File Inventory

### Frontend Files
```
index.html              - Main recipe browser (NEEDS MOBILE FIX)
events.html             - Event management
event-detail.html       - Event dashboard
respond.html            - Guest response page
add-recipe.html         - Recipe import wizard (NEEDS CAMERA)
cooking.html            - Mobile cooking mode (NEEDS ENHANCEMENT)
```

### Data Files
```
recipes.json            - 122 recipes (NEEDS CLEANUP)
recipes.db              - SQLite database (local only)
```

### Backend Functions (19 total)
```
netlify/functions/
├── get-recipe.js                   - Get/update single recipe
├── get-recipes.js                  - Get all/search recipes
├── save-recipes.js                 - Bulk save
├── load-recipes.js                 - Load from Dropbox
├── add-recipe.js                   - Add new recipe
├── update-recipe.js                - Update recipe
├── extract-file.js                 - Extract text from uploads (NEEDS CAMERA SUPPORT)
├── format-recipe.js                - AI recipe formatting
├── manage-contributors.js          - Contributor CRUD
├── create-event.js                 - Create/update events
├── get-events.js                   - Get events
├── save-events.js                  - Save to Dropbox
├── event-recipes.js                - Event recipe management
├── record-selection.js             - Guest responses
├── generate-email.js               - Event emails
├── send-verification-code.js       - Email codes (v3.1)
├── verify-code.js                  - Validate codes (v3.1)
├── statistics.js                   - Recipe stats
└── lib/dropbox-auth.js             - OAuth helper
```

### Scripts
```
fix_contributors.py          - Contributor assignment script (v3.1.4)
reformat_instructions.py     - Instruction reformatter
export_to_json.py            - Export DB to JSON
upload_recipes_to_dropbox.py - Upload to Dropbox
```

### Documentation
```
CLAUDE.md                              - Project documentation
DEPLOYMENT.md                          - Netlify deployment guide
COOKING_SPECIFICATION.md               - Feature specifications
COOKING_HISTORY.md                     - Development history
COOKING_CHANGELOG.md                   - Version changelog
SESSION_SUMMARY_2025-11-04_*.md        - Recent session summaries
BUGFIX_2025-11-04_CONTRIBUTOR_FILTER.md - Contributor fix docs
```

---

## 🔍 Critical Code Locations

### Mobile Modal (PRIORITY FIX)
**File:** `index.html`
**Lines:** Search for `.recipe-detail-modal` or similar modal CSS

**Current Issue:**
```css
/* Likely current problematic CSS */
.modal {
  position: fixed;
  /* Missing: max-height, overflow-y, touch scrolling */
}
```

**Required Fix:**
```css
.recipe-modal {
  position: fixed;
  top: 10px;
  left: 10px;
  right: 10px;
  bottom: 10px;
  max-height: calc(100vh - 20px);
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}
```

### Recipe Data Structure
**File:** `recipes.json`
**Current Schema:**
```json
{
  "id": 1,
  "title": "Recipe Name",
  "ingredients": ["2 cups flour", "1 tsp salt"],
  "instructions": ["Step 1", "Step 2"],
  "prep_time": "15 min",
  "cook_time": "30 min",
  "servings": 6,
  "contributor": "Janet",
  "source_attribution": "NYT Cooking",
  "needs_review": false
}
```

**Enhanced Schema (v4.0):**
```json
{
  "id": 1,
  "title": "Recipe Name",
  "ingredients": [
    { "id": "flour", "quantity": "2 cups", "item": "flour" }
  ],
  "instructions": [
    {
      "step": 1,
      "text": "Mix ingredients",
      "ingredients": ["flour", "salt"],
      "timer": { "default": 10, "min": 8, "max": 12 }
    }
  ]
}
```

---

## 🧪 Testing Requirements

### Device Testing Matrix
```
iOS Devices (PRIORITY):
□ iPhone SE 2020 (375x667)
□ iPhone 12/13/14 (390x844)
□ iPhone 14 Pro Max (430x932)
□ iPhone 15 Pro (393x852)
□ iPad 10.9" (820x1180)

Android Devices:
□ Pixel 6 (412x915)
□ Samsung S21 (384x854)

Desktop:
□ Chrome DevTools device emulation
□ MacBook Pro 14" (1512x982)
```

### Browser Testing
- Safari iOS (PRIORITY - Janet's browser)
- Chrome iOS
- Chrome Android
- Chrome Desktop
- Firefox Desktop

### Performance Targets
- First Paint: <1.0s
- Recipe Modal Load: <0.5s
- Step Navigation: <100ms
- Timer Precision: ±1 second
- Scroll Performance: 60fps

---

## 🔄 Git Status

```
Current branch: main
Modified files:
  M CLAUDE.md
  M index.html
  M events.html
  M event-detail.html
  M netlify/functions/get-recipes.js
  M recipes.json

Untracked files:
  ?? BUGFIX_2025-11-04_CONTRIBUTOR_FILTER.md
  ?? COOKING_HISTORY.md
  ?? COOKING_SPECIFICATION.md
  ?? FINAL_VERIFICATION_2025-11-04.md
  ?? fix_contributors.py
  ?? schema_updates.sql
```

---

## 📦 Deployment Configuration

### Netlify
- **Site:** fergi-cooking
- **URL:** https://fergi-cooking.netlify.app
- **Functions:** Auto-deploy from `netlify/functions/`
- **Build:** Direct deployment (no build step)

### Dropbox
- **Path:** `/Apps/Reference Refinement/recipes.json`
- **Shared with:** Reference Refinement project
- **OAuth:** Auto-refresh tokens via lib/dropbox-auth.js

---

## ⚠️ Pre-Implementation Checklist

Before starting v4.0 implementation:

- [x] Create comprehensive checkpoint documentation
- [ ] Commit and push current state to GitHub
- [ ] Create v3.1.6 git tag
- [ ] Backup recipes.json from Dropbox
- [ ] Test current production site
- [ ] Document any breaking changes
- [ ] Review all UX analysis documents
- [ ] Set up local testing environment

---

## 🎯 v4.0 Success Criteria

### Must Have (P0)
1. ✅ Mobile modal displays 100% of recipe content
2. ✅ Smooth scrolling on all mobile devices
3. ✅ Data cleanup removes all non-recipes
4. ✅ Contributor counts verified (85/37)
5. ✅ Camera capture working on mobile

### Should Have (P1)
6. ✅ Step-by-step cooking mode functional
7. ✅ Embedded ingredients per step
8. ✅ Progress indicators in cooking mode
9. ✅ Swipe gestures for navigation

### Nice to Have (P2)
10. ✅ Timer integration with notifications
11. ✅ Haptic feedback on iOS
12. ✅ Desktop generous layout
13. ✅ Multiple concurrent timers

---

## 📝 Notes for Implementation

### Critical Reminders
1. **MOBILE FIRST:** Fix the modal BEFORE anything else
2. **BACKUP DATA:** Always backup before running cleanup script
3. **TEST EARLY:** Use Chrome DevTools device emulation
4. **JANET'S USE CASE:** iPhone Safari is primary browser
5. **WAKE LOCK:** Already implemented, just enhance cooking mode

### Technical Considerations
- iOS Safari has specific scrolling requirements (`-webkit-overflow-scrolling: touch`)
- Touch targets must be 44x44px minimum (iOS HIG)
- Camera API requires HTTPS (already on Netlify)
- Service workers require HTTPS and registration
- Notification API requires user permission prompt

### Dependencies
- No new npm packages required for Phase 1-3
- Service worker for Phase 5 (background timers)
- Web Audio API built-in (Phase 5)
- Existing Tesseract.js for OCR (Phase 3)

---

## 🔗 Related Resources

### Documentation in ~/Downloads/
1. `COOKING_v3_1_COMPREHENSIVE_MOBILE_UX_ANALYSIS.md` - Complete mobile specs
2. `COOKING_v3_1_MOBILE_UX_COMPLETE_ANALYSIS.md` - Data cleanup details
3. `COOKING_v3_1_CLEANUP_AND_RESPONSIVE_INSTRUCTIONS.md` - Implementation guide

### Infrastructure
- See `~/.claude/global-infrastructure.md` for deployment patterns
- See `FERGI_INFRASTRUCTURE_GUIDE.md` for Netlify/Dropbox setup

---

## ⏱️ Estimated Timeline

**Total Implementation Time:** ~24 hours

- Phase 1 (Mobile Modal): 2 hours ⚡ **DO FIRST**
- Phase 2 (Data Cleanup): 4 hours
- Phase 3 (Camera): 3 hours
- Phase 4 (Three Modes): 8 hours
- Phase 5 (Timers): 4 hours
- Phase 6 (Desktop): 3 hours

**Suggested Approach:**
- Day 1: Phases 1-2 (Fix mobile, cleanup data)
- Day 2: Phase 3 (Add camera)
- Day 3-4: Phase 4 (Cooking modes)
- Day 5: Phases 5-6 (Timers, desktop polish)

---

## ✅ Next Actions

1. **IMMEDIATELY:** Backup to GitHub with commit message: "v3.1.6 - Pre-v4.0 checkpoint"
2. **THEN:** Start Phase 1 - Fix mobile modal (CRITICAL)
3. **AFTER:** Run data cleanup script with backup
4. **CONTINUE:** Implement remaining phases in order

---

**Checkpoint Created:** 2025-11-04
**Created By:** Claude Code (Sonnet 4.5)
**Status:** ✅ Ready for v4.0 implementation
**Context:** 47K/200K tokens (24% used, 76% remaining)

---

## 📞 Questions for Joe (if needed)

1. Should we keep backups of original recipes before cleanup?
2. What to do with book entry - delete or convert?
3. Priority on timer features vs other enhancements?
4. Any specific iOS devices to prioritize for testing?
5. Should cooking mode replace or complement existing cooking.html?
