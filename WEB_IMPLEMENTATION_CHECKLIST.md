# Web Implementation Checklist - Phase 1 Critical Fixes

**Project:** Fergi Cooking Mobile-First Redesign
**Session:** November 9, 2025
**For:** Web Claude
**Priority:** HIGH - Critical mobile UX fixes

---

## Pre-Implementation Setup

### Environment Check
- [ ] Read `WEB_SESSION_BRIEF.md` completely
- [ ] Review `mobile_ux_research_report.md` (comprehensive research)
- [ ] Understand current codebase structure
- [ ] Verify `recipes.json` available (128 recipes, 507KB)
- [ ] Review current files to modify:
  - `index.html` - Recipe browsing
  - `events.html` - Event management
  - `event-detail.html` - Event dashboard
  - `add-recipe.html` - **CRITICAL FIX** (two-column breaks on mobile)
  - `cooking.html` - Cooking mode (increase fonts)
  - `respond.html` - Guest responses

### Design System Review
- [ ] Review color system (v4.0 - already good, maintain)
- [ ] Review typography scale (need to implement)
- [ ] Review spacing system (8px base)
- [ ] Review touch target standards (48 × 48px minimum)
- [ ] Review breakpoints (mobile-first: 768px primary)

---

## Phase 1: Critical Fixes Implementation

### 1. Typography System Setup

**Create CSS Variables (All Pages):**

```css
:root {
  /* Base font sizes */
  --font-size-base: 16px;           /* Body text, form inputs - CRITICAL */
  --font-size-lg: 18px;             /* Large body text */
  --font-size-xl: 20px;

  /* Headings */
  --font-size-h1: 28px;
  --font-size-h2: 24px;
  --font-size-h3: 20px;

  /* Small */
  --font-size-sm: 14px;
  --font-size-xs: 12px;

  /* Interactive */
  --font-size-button: 16px;
  --font-size-input: 16px;          /* CRITICAL - prevents iOS zoom */

  /* Cooking mode overrides */
  --cooking-title: 28px;
  --cooking-ingredients: 20px;
  --cooking-instructions: 22px;
  --cooking-step-number: 56px;      /* Up from 40px */
  --cooking-metadata: 14px;

  /* Line heights */
  --line-height-tight: 1.2;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.6;

  /* Touch targets */
  --touch-min: 44px;                /* iOS minimum */
  --touch-recommended: 48px;        /* Android, better for all */
  --touch-primary: 56px;            /* Bottom nav */

  /* Spacing (8px base) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Border radius */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
  --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
}
```

**Checklist:**
- [ ] Add `:root` variables to each HTML file's `<style>` section
- [ ] OR create shared `mobile-design-system.css` and import

**Apply Typography:**
```css
/* CRITICAL: All form inputs must be 16px minimum */
input, textarea, select {
  font-size: var(--font-size-input); /* 16px - prevents iOS zoom */
  min-height: var(--touch-recommended); /* 48px */
  padding: 12px 16px;
  border-radius: var(--radius-md);
  width: 100%;
}

/* Body text */
body {
  font-size: var(--font-size-base);
  line-height: var(--line-height-normal);
}

/* Headings */
h1 { font-size: var(--font-size-h1); }
h2 { font-size: var(--font-size-h2); }
h3 { font-size: var(--font-size-h3); }

/* Buttons */
button, .button {
  font-size: var(--font-size-button);
  min-height: var(--touch-recommended);
  padding: 12px 16px;
  border-radius: var(--radius-md);
}
```

**Checklist:**
- [ ] Apply to `index.html`
- [ ] Apply to `events.html`
- [ ] Apply to `event-detail.html`
- [ ] Apply to `add-recipe.html`
- [ ] Apply to `cooking.html` (with cooking overrides)
- [ ] Apply to `respond.html`

---

### 2. Bottom Navigation Implementation

**Create Bottom Nav Component:**

```html
<!-- Add to ALL pages (except cooking.html - optional) -->
<nav class="bottom-nav" aria-label="Main navigation">
  <a href="index.html" class="nav-item active" aria-label="Home">
    <span class="nav-icon" aria-hidden="true">🏠</span>
    <span class="nav-label">Home</span>
  </a>

  <a href="events.html" class="nav-item" aria-label="Events">
    <span class="nav-icon" aria-hidden="true">📅</span>
    <span class="nav-label">Events</span>
  </a>

  <a href="add-recipe.html" class="nav-item primary" aria-label="Add Recipe">
    <span class="nav-icon" aria-hidden="true">+</span>
    <span class="nav-label">Add</span>
  </a>

  <a href="cooking.html" class="nav-item" aria-label="Cooking Mode">
    <span class="nav-icon" aria-hidden="true">👨‍🍳</span>
    <span class="nav-label">Cooking</span>
  </a>

  <a href="#" class="nav-item" aria-label="More options" onclick="showMoreMenu(); return false;">
    <span class="nav-icon" aria-hidden="true">≡</span>
    <span class="nav-label">More</span>
  </a>
</nav>

<!-- Add body padding to prevent content overlap -->
<style>
body {
  padding-bottom: 90px; /* 56px nav + 34px safe area */
}
</style>
```

**Bottom Nav Styles:**

```css
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  padding-bottom: calc(8px + env(safe-area-inset-bottom)); /* iPhone safe area */
  background: white;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-around;
  align-items: center;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
  z-index: 1000;
}

.bottom-nav .nav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-width: var(--touch-primary); /* 56px */
  min-height: var(--touch-primary);
  color: #6b7280; /* Gray - inactive */
  text-decoration: none;
  transition: color 0.2s, transform 0.1s;
  -webkit-tap-highlight-color: rgba(59, 130, 246, 0.1);
}

.bottom-nav .nav-item:active {
  transform: scale(0.95); /* Subtle press feedback */
}

.bottom-nav .nav-item.active {
  color: #3b82f6; /* Primary color */
}

.bottom-nav .nav-item.primary {
  color: #f59e0b; /* Accent - "Add" button */
  font-weight: 600;
}

.bottom-nav .nav-icon {
  font-size: 24px;
  margin-bottom: 2px;
}

.bottom-nav .nav-label {
  font-size: 11px;
  font-weight: 500;
}

/* Active state: larger icon, bold label */
.bottom-nav .nav-item.active .nav-icon {
  font-size: 26px;
}

.bottom-nav .nav-item.active .nav-label {
  font-weight: 600;
}
```

**Checklist:**
- [ ] Add bottom nav HTML to `index.html`
- [ ] Add bottom nav HTML to `events.html`
- [ ] Add bottom nav HTML to `event-detail.html`
- [ ] Add bottom nav HTML to `add-recipe.html`
- [ ] Add bottom nav HTML to `respond.html`
- [ ] (Optional) Add to `cooking.html` (or keep minimal)
- [ ] Add bottom nav CSS to each page
- [ ] Add body padding to prevent overlap
- [ ] Add `showMoreMenu()` function (opens modal or navigates)
- [ ] Test active state changes on navigation
- [ ] Test one-handed reachability

---

### 3. Simplify Top Bar

**Minimal Top Bar Structure:**

```html
<header class="top-bar">
  <!-- Left: Back button OR Logo -->
  <div class="top-bar-left">
    <a href="index.html" class="back-button" aria-label="Back to home">←</a>
  </div>

  <!-- Center: Page Title -->
  <div class="top-bar-center">
    <h1 class="page-title">Recipe Browser</h1>
  </div>

  <!-- Right: Search + Status (minimal) -->
  <div class="top-bar-right">
    <button class="icon-button" aria-label="Search" onclick="showSearch()">🔍</button>
    <span class="status-indicator online">Online</span>
  </div>
</header>

<!-- Add body padding for fixed header -->
<style>
body {
  padding-top: 56px; /* Top bar height */
  padding-bottom: 90px; /* Bottom nav + safe area */
}
</style>
```

**Top Bar Styles:**

```css
.top-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 56px;
  padding-top: env(safe-area-inset-top); /* iPhone notch */
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  padding-left: var(--space-md);
  padding-right: var(--space-md);
  z-index: 999;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.top-bar-left,
.top-bar-right {
  flex: 0 0 auto;
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.top-bar-center {
  flex: 1;
  text-align: center;
  padding: 0 var(--space-md);
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.back-button,
.icon-button {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  background: none;
  border: none;
  color: #374151;
  cursor: pointer;
  border-radius: var(--radius-md);
  transition: background 0.2s;
}

.back-button:hover,
.icon-button:hover {
  background: #f3f4f6;
}

.back-button:active,
.icon-button:active {
  background: #e5e7eb;
}

.status-indicator {
  font-size: 11px;
  padding: 4px 8px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  white-space: nowrap;
}

.status-indicator.offline {
  background: #fef2f2;
  color: #dc2626;
}

.status-indicator.online {
  background: #f0fdf4;
  color: #16a34a;
}
```

**Checklist:**
- [ ] Update top bar in `index.html`
- [ ] Update top bar in `events.html`
- [ ] Update top bar in `event-detail.html`
- [ ] Update top bar in `add-recipe.html`
- [ ] Update top bar in `cooking.html` (keep minimal)
- [ ] Update top bar in `respond.html`
- [ ] Add top bar CSS to each page
- [ ] Add body padding for fixed header
- [ ] Test on mobile (no overlap, no cramped text)

---

### 4. Fix Add Recipe Page (CRITICAL)

**Current Problem:**
- Two-column layout (form | preview) breaks on mobile
- Text overlaps, labels cut off, horizontal scrolling

**Mobile Solution (<768px): Single Column**

```html
<!-- Add Recipe Container -->
<div class="add-recipe-container">
  <!-- Mobile: Toggle Preview Button -->
  <button class="toggle-preview" onclick="togglePreview()">
    <span id="toggle-text">Show Preview</span>
  </button>

  <!-- Form Section (Full Width on Mobile) -->
  <div class="recipe-form">
    <!-- All form fields here -->
    <!-- Ensure all inputs have font-size: 16px minimum! -->
  </div>

  <!-- Preview Section (Collapsible on Mobile) -->
  <div class="recipe-preview" id="recipe-preview" style="display: none;">
    <!-- Recipe preview here -->
  </div>
</div>
```

**Add Recipe Styles:**

```css
/* Mobile: Single column, preview collapsible */
.add-recipe-container {
  display: flex;
  flex-direction: column;
  padding: var(--space-md);
  max-width: 100%;
}

.toggle-preview {
  width: 100%;
  min-height: var(--touch-recommended);
  margin-bottom: var(--space-md);
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: var(--radius-md);
  font-size: var(--font-size-button);
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.toggle-preview:hover {
  background: #e5e7eb;
}

.toggle-preview:active {
  background: #d1d5db;
}

.recipe-form {
  width: 100%;
}

.recipe-preview {
  width: 100%;
  padding: var(--space-md);
  border-top: 1px solid #e5e7eb;
  margin-top: var(--space-md);
  background: #f9fafb;
  border-radius: var(--radius-lg);
}

/* Form fields */
.form-field {
  margin-bottom: var(--space-md);
}

.form-field label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 6px;
  color: #374151;
}

.form-field input,
.form-field textarea,
.form-field select {
  font-size: 16px !important; /* CRITICAL - prevent iOS zoom */
  min-height: var(--touch-recommended);
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: var(--radius-md);
  width: 100%;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-field input:focus,
.form-field textarea:focus,
.form-field select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Tablet/Desktop: Side-by-side */
@media (min-width: 768px) {
  .add-recipe-container {
    flex-direction: row;
    gap: var(--space-lg);
  }

  .toggle-preview {
    display: none; /* Always visible on tablet/desktop */
  }

  .recipe-form {
    width: 50%;
  }

  .recipe-preview {
    width: 50%;
    border-top: none;
    border-left: 1px solid #e5e7eb;
    margin-top: 0;
    position: sticky;
    top: 72px; /* Top bar + spacing */
    max-height: calc(100vh - 72px);
    overflow-y: auto;
    display: block !important; /* Override inline style */
  }
}
```

**Toggle Preview JavaScript:**

```javascript
function togglePreview() {
  const preview = document.getElementById('recipe-preview');
  const toggleText = document.getElementById('toggle-text');

  if (preview.style.display === 'none') {
    preview.style.display = 'block';
    toggleText.textContent = 'Hide Preview';
    // Scroll to preview
    preview.scrollIntoView({ behavior: 'smooth', block: 'start' });
  } else {
    preview.style.display = 'none';
    toggleText.textContent = 'Show Preview';
  }
}
```

**Checklist:**
- [ ] Update `add-recipe.html` layout structure
- [ ] Add toggle preview button (mobile only)
- [ ] Ensure single column on mobile (<768px)
- [ ] Ensure side-by-side on tablet (768px+)
- [ ] Set ALL input font-size to 16px minimum
- [ ] Test on iPhone simulator (Safari)
- [ ] Test preview toggle works
- [ ] Test no text overlap or cut-off
- [ ] Test no horizontal scrolling
- [ ] Verify sticky preview on desktop

---

### 5. Fix Recipe Detail Modal

**Current Problem:**
- Not optimized for mobile (should be full-screen)
- Fonts too small (14-16px body)
- Action buttons cramped

**Mobile: Full-Screen Modal**

```css
/* Mobile (<768px): Full-screen */
.recipe-detail-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: white;
  z-index: 1001;
  display: none; /* Hidden by default */
  flex-direction: column;
  transform: translateX(100%);
  transition: transform 0.3s ease;
}

.recipe-detail-modal.active {
  display: flex;
  transform: translateX(0);
}

/* Modal Header */
.modal-header {
  flex: 0 0 auto;
  height: 56px;
  display: flex;
  align-items: center;
  padding: 0 var(--space-md);
  border-bottom: 1px solid #e5e7eb;
  background: white;
}

.modal-header .close-button {
  width: var(--touch-recommended);
  height: var(--touch-recommended);
  font-size: 28px;
  line-height: 1;
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
}

.modal-header .close-button:hover {
  background: #f3f4f6;
}

.modal-header .close-button:active {
  background: #e5e7eb;
}

.modal-header .recipe-title {
  flex: 1;
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  margin: 0 var(--space-md);
}

/* Modal Content */
.modal-content {
  flex: 1 1 auto;
  overflow-y: auto;
  padding: var(--space-md);
  font-size: var(--font-size-base); /* 16px minimum */
  line-height: var(--line-height-normal);
}

.modal-content h2 {
  font-size: var(--font-size-h2);
  margin-top: var(--space-lg);
  margin-bottom: var(--space-md);
}

.modal-content h3 {
  font-size: var(--font-size-h3);
}

/* Modal Actions */
.modal-actions {
  flex: 0 0 auto;
  padding: var(--space-md);
  border-top: 1px solid #e5e7eb;
  background: white;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.modal-actions button {
  width: 100%;
  min-height: var(--touch-recommended);
  font-size: var(--font-size-button);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  border: 1px solid #d1d5db;
  background: white;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.modal-actions button:hover {
  background: #f3f4f6;
}

.modal-actions button.primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.modal-actions button.primary:hover {
  background: #2563eb;
}

/* Tablet/Desktop (768px+): Centered modal */
@media (min-width: 768px) {
  .recipe-detail-modal {
    width: 80%;
    max-width: 900px;
    height: auto;
    max-height: 90vh;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0.9);
    opacity: 0;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-2xl);
  }

  .recipe-detail-modal.active {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }

  .modal-actions {
    flex-direction: row;
    justify-content: flex-end;
  }

  .modal-actions button {
    width: auto;
    min-width: 120px;
  }
}
```

**Checklist:**
- [ ] Update `index.html` modal styles
- [ ] Ensure full-screen on mobile (<768px)
- [ ] Ensure centered on desktop (768px+)
- [ ] Increase body font to 16-18px
- [ ] Close button 48 × 48px
- [ ] Action buttons stack on mobile
- [ ] Action buttons row on desktop
- [ ] Test opening/closing animation
- [ ] Test scrolling with long content

---

### 6. Update Cooking Mode

**Current Problem:**
- Base font 1.1rem (17.6px) too small
- Step numbers 40px too small
- Not optimized for distance reading (2+ feet)

**Cooking Mode Updates:**

```css
.cooking-mode {
  font-size: 1.125rem; /* 18px base - up from 17.6px */
  line-height: var(--line-height-relaxed); /* 1.6 */
  padding: var(--space-md);
}

.cooking-mode .recipe-title {
  font-size: var(--cooking-title); /* 28px */
  font-weight: 700;
  margin-bottom: var(--space-lg);
  text-align: center;
}

.cooking-mode .section-heading {
  font-size: var(--font-size-h2); /* 24px */
  font-weight: 600;
  margin-top: var(--space-lg);
  margin-bottom: var(--space-md);
}

.cooking-mode .ingredients {
  font-size: var(--cooking-ingredients); /* 20px */
  line-height: 1.6;
}

.cooking-mode .instructions {
  font-size: var(--cooking-instructions); /* 22px */
  line-height: 1.6;
}

.cooking-mode .step-number {
  width: var(--cooking-step-number); /* 56px - up from 40px */
  height: var(--cooking-step-number);
  font-size: 2rem; /* 32px */
  font-weight: 700;
  border-radius: var(--radius-full);
  background: #3b82f6;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: var(--space-md);
  flex-shrink: 0;
}

/* Ingredient Checkboxes - Larger Tap Targets */
.cooking-mode .ingredient-item {
  display: flex;
  align-items: center;
  margin-bottom: var(--space-md);
}

.cooking-mode .ingredient-checkbox {
  width: 24px; /* Visual size */
  height: 24px;
  margin: 0; /* Remove default margin */
}

/* Wrap checkbox in larger tap target */
.cooking-mode .checkbox-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: var(--touch-recommended); /* 48px tap target */
  min-height: var(--touch-recommended);
  margin-right: var(--space-sm);
}

/* Checked state: strikethrough + fade */
.cooking-mode .ingredient-item.checked {
  opacity: 0.5;
  text-decoration: line-through;
}

/* Metadata (less critical) */
.cooking-mode .metadata {
  font-size: var(--cooking-metadata); /* 14px */
  color: #6b7280;
  margin-bottom: var(--space-lg);
  text-align: center;
}

/* Landscape Tablet: Two-Column Layout */
@media (min-width: 768px) and (orientation: landscape) {
  .cooking-mode {
    display: flex;
    gap: var(--space-lg);
  }

  .cooking-ingredients-section {
    width: 40%;
    position: sticky;
    top: 0;
    max-height: 100vh;
    overflow-y: auto;
    border-right: 2px solid #e5e7eb;
    padding-right: var(--space-md);
  }

  .cooking-instructions-section {
    width: 60%;
  }
}

/* Phone Landscape: Stay Single Column */
@media (max-width: 767px) and (orientation: landscape) {
  .cooking-mode {
    flex-direction: column;
  }
}
```

**Checklist:**
- [ ] Update `cooking.html` font sizes
- [ ] Increase base to 18px (from 17.6px)
- [ ] Increase ingredients to 20px
- [ ] Increase instructions to 22px
- [ ] Increase step numbers to 56px (from 40px)
- [ ] Increase checkbox tap targets to 48 × 48px
- [ ] Add checked state (strikethrough + fade)
- [ ] Implement two-column landscape (tablet only)
- [ ] Test readability from 2-3 feet distance
- [ ] Test ingredient checkboxes easy to tap

---

## Testing Checklist

### Desktop Testing (1024px+)
- [ ] All pages load without errors
- [ ] Layout looks good
- [ ] Bottom nav visible and functional
- [ ] Top bar not cramped
- [ ] Modals centered properly
- [ ] Add recipe side-by-side layout works
- [ ] Recipe detail modal centered

### Tablet Testing (768-1024px)
- [ ] All pages responsive
- [ ] Bottom nav still accessible
- [ ] Add recipe side-by-side works
- [ ] Recipe cards layout appropriate
- [ ] Cooking mode landscape two-column works (optional)
- [ ] Touch targets still 48 × 48px

### Mobile Testing (<768px)
**Critical Tests:**
- [ ] **Add recipe page works without text overlap**
- [ ] **All form inputs 16px minimum (no iOS zoom)**
- [ ] **Preview toggle button works**
- [ ] **Recipe detail modal full-screen**
- [ ] **Bottom nav reachable one-handed**
- [ ] **All touch targets minimum 48 × 48px**
- [ ] **No horizontal scrolling on any page**
- [ ] **Cooking mode readable from 2+ feet**

**Detailed Mobile Tests:**

**index.html (Recipe Browsing):**
- [ ] Recipe cards display correctly
- [ ] Search works
- [ ] Filters work (contributor, etc.)
- [ ] Recipe detail opens full-screen
- [ ] Bottom nav visible, active state works
- [ ] Top bar not cramped
- [ ] No text overlap or cut-off

**events.html (Event Management):**
- [ ] Event list displays correctly
- [ ] Create event button easy to tap
- [ ] Bottom nav visible
- [ ] Top bar clear

**event-detail.html (Event Dashboard):**
- [ ] Event details display
- [ ] Recipe assignment works
- [ ] Guest list readable
- [ ] Bottom nav visible

**add-recipe.html (CRITICAL):**
- [ ] Page loads without text overlap
- [ ] Single column layout on mobile
- [ ] Form inputs all 16px minimum
- [ ] No iOS auto-zoom on input focus
- [ ] Preview toggle button visible and works
- [ ] All touch targets 48 × 48px minimum
- [ ] 4-step wizard flows smoothly
- [ ] File upload works
- [ ] Vision API extraction works
- [ ] No horizontal scrolling

**cooking.html (Cooking Mode):**
- [ ] Recipe title readable (28px)
- [ ] Ingredients readable from 2+ feet (20px)
- [ ] Instructions readable from 2+ feet (22px)
- [ ] Step numbers large and clear (56px)
- [ ] Ingredient checkboxes easy to tap (48 × 48px)
- [ ] Checkboxes persist state
- [ ] Checked items strikethrough + fade
- [ ] Prev/Next buttons easy to tap
- [ ] Screen stays on (Wake Lock)

**respond.html (Guest Responses):**
- [ ] Form displays correctly
- [ ] All inputs 16px minimum
- [ ] Submit button easy to tap
- [ ] Bottom nav visible

### Accessibility Testing
- [ ] Color contrast > 4.5:1 (use Lighthouse)
- [ ] All touch targets > 44 × 44px
- [ ] All images have alt text
- [ ] Buttons have aria-labels where appropriate
- [ ] Tab order logical
- [ ] Focus indicators visible
- [ ] Test with VoiceOver (iOS)

### Performance Testing
- [ ] Initial page load < 3 seconds (Lighthouse)
- [ ] Recipe list renders smoothly (128 recipes)
- [ ] Scrolling 60 FPS (no jank)
- [ ] Modals open/close smoothly
- [ ] No memory leaks after extended use

---

## Deployment Checklist

### Pre-Deployment
- [ ] All Phase 1 tasks completed
- [ ] All tests pass (desktop, tablet, mobile)
- [ ] No console errors
- [ ] recipes.json bundled with functions
- [ ] All 21 Netlify Functions unchanged

### Local Testing
```bash
# Test locally with Netlify Dev
netlify dev

# Open browser to http://localhost:8888
# Test all pages thoroughly
# Test on mobile simulator (Safari, Chrome DevTools)
```

- [ ] Tested locally with `netlify dev`
- [ ] All pages work correctly
- [ ] All functions work correctly
- [ ] Offline mode still works

### Production Deployment
```bash
# Deploy to production
netlify deploy --prod --dir="." --message="Phase 1: Mobile-first redesign - critical fixes"

# Visit live site
# https://fergi-cooking.netlify.app
```

- [ ] Deployed to production
- [ ] Live site tested on desktop
- [ ] Live site tested on tablet (iPad simulator)
- [ ] Live site tested on actual iPhone (Janet's device if possible)

### Post-Deployment
- [ ] All pages load correctly
- [ ] All functions work correctly
- [ ] Offline mode works
- [ ] Create session summary for Mac
- [ ] Document any issues or improvements needed

---

## Success Criteria

**After completing this checklist, the app should:**

✅ **Add Recipe Page:**
- Works perfectly on iPhone (no overlap, no cut-off text)
- Single column on mobile, side-by-side on tablet
- All inputs prevent iOS zoom (16px minimum)
- Preview section collapsible on mobile

✅ **Navigation:**
- Bottom nav bar with 5 items, all reachable one-handed
- Active state clearly visible
- Top bar simplified (minimal)

✅ **Recipe Detail:**
- Full-screen on mobile, centered on desktop
- All fonts readable (16-18px body)
- Action buttons prominent and easy to tap
- Close button 48 × 48px

✅ **Typography:**
- No fonts below 16px on mobile
- All form inputs 16px minimum (no iOS zoom)
- Cooking mode 18-22px (readable from distance)

✅ **Touch Targets:**
- All interactive elements minimum 48 × 48px
- Proper spacing between buttons (8px+)
- Easy to tap on actual device

✅ **No Mobile UX Issues:**
- No horizontal scrolling
- No text overlap or cut-off
- No tiny buttons
- No iOS auto-zoom on inputs

---

## Files to Modify

### HTML Files (6 total):
1. **index.html** - Recipe browsing
   - Add bottom nav
   - Simplify top bar
   - Update recipe detail modal
   - Add CSS variables

2. **events.html** - Event management
   - Add bottom nav
   - Simplify top bar
   - Add CSS variables

3. **event-detail.html** - Event dashboard
   - Add bottom nav
   - Simplify top bar
   - Add CSS variables

4. **add-recipe.html** - **CRITICAL FIX**
   - Single-column mobile layout
   - Add preview toggle
   - All inputs 16px minimum
   - Add bottom nav
   - Simplify top bar

5. **cooking.html** - Cooking mode
   - Increase all fonts
   - Larger step numbers (56px)
   - Larger checkbox tap targets
   - Two-column landscape (tablet)
   - (Optional) Add bottom nav

6. **respond.html** - Guest responses
   - Add bottom nav
   - Simplify top bar
   - Add CSS variables

### Files NOT to Modify:
- ❌ All 21 Netlify Functions (backend working perfectly)
- ❌ `offline-manager.js` (working great)
- ❌ `recipes.json` (database ready)
- ❌ `netlify.toml` (config correct)

---

## Notes for Web Claude

**Time Estimate:**
- Claude.ai said "Week 1" but you can do this in a single session!
- Focus on mobile-first approach
- Test frequently as you work
- Don't try to be perfect, ship and iterate

**Key Principles:**
1. **Mobile-first CSS:** Write for mobile, enhance for desktop
2. **16px minimum inputs:** Prevents iOS auto-zoom (critical!)
3. **48 × 48px touch targets:** Better than minimum (44px)
4. **Bottom nav:** 5 items max, easy reach
5. **Full-screen modals on mobile:** Better UX than centered

**If You Get Stuck:**
- Check `mobile_ux_research_report.md` for detailed explanations
- All recommendations are research-backed
- iOS HIG and Material Design standards applied
- Tested patterns from NYT, Paprika, Mela

**Remember:**
- Janet (primary user) can't use Add Recipe on iPhone right now
- Cooking mode fonts too small to read from counter
- This is HIGH IMPACT work!

**Good luck! 🚀**

---

**Checklist prepared by:** Mac Claude Code
**For:** Web Claude Implementation
**Date:** November 9, 2025
**Version:** Phase 1 Critical Fixes
