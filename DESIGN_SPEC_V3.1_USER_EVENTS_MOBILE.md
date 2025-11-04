# Design Specification v3.1 - User Authentication, Event Segregation & Mobile Recipe Reading

**Created:** November 3, 2025
**Status:** SPECIFICATION - Ready for Implementation
**Priority:** HIGH - Janet's mobile cooking experience + multi-user event management

---

## 📊 Context: 47,321 / 200,000 tokens (23.7% used, 76.3% remaining)

---

## Executive Summary

**Three Critical Problems to Solve:**

1. **User Identity Problem:** Contributors need to create and manage their own events separately, requiring user identification without friction
2. **Event Segregation Problem:** Each contributor's events must be completely separate from other contributors' events
3. **Mobile Recipe Reading Problem:** Janet (and all users) need recipes that are **readable while cooking** on smartphones

**Core Design Principle:** ZERO FRICTION, MAXIMUM USABILITY

---

## Problem 1: Mobile Recipe Reading (Janet's Pain Point)

### Current Issues

**What Janet experiences on her phone:**
- Tiny text that's hard to read while standing at the stove
- Too much information crammed into small screen
- Has to pinch-zoom constantly
- Can't quickly glance at next step while stirring
- Buttons and UI elements waste screen space
- Modal scrolling is awkward on mobile
- Two-column print layout doesn't help mobile users

**Critical Use Case:**
> "Janet is cooking at the stove. Her phone is on the counter. She has flour on her hands. She needs to quickly read: 'What's the next step?' and 'How much butter?' without zooming, scrolling excessively, or tapping buttons."

### Solution: Cooking Mode (Mobile-First Recipe Display)

#### Design Philosophy
- **BIG TEXT** - Ingredients and instructions must be readable from 2 feet away
- **SIMPLE LAYOUT** - One column, generous spacing, no clutter
- **QUICK SCANNING** - Clear visual hierarchy, numbered steps, ingredient quantities pop
- **MINIMAL INTERACTION** - Everything visible, minimal scrolling
- **KITCHEN-PROOF** - Large touch targets for dirty hands

#### Specific Design Requirements

**Typography (Mobile):**
```css
Recipe Title: 1.75rem (28px), bold, centered
Ingredients Header: 1.3rem (21px), bold
Ingredient Items: 1.1rem (18px), line-height: 1.8
  - Quantity/Unit: BOLD, slightly larger (1.2rem)
  - Ingredient name: Regular weight
Instructions Header: 1.3rem (21px), bold
Instruction Steps: 1.1rem (18px), line-height: 1.8
  - Step numbers: LARGE (1.4rem), bold, in circle or badge
  - Step text: Clear, generous spacing between steps
```

**Layout (Mobile < 768px):**
- Single column, full width (padding: 1rem)
- NO modal overlay - Full-screen view OR dedicated cooking URL
- Recipe metadata (times, servings) in compact card at top
- Ingredients section: White background, light border, extra padding
  - Each ingredient on its own line
  - Checkboxes to mark off ingredients (optional, nice-to-have)
- Instructions section: Extra spacing between steps
  - Large step numbers (1, 2, 3...) in colored circles
  - Each step clearly separated (border-bottom or margin)
- NO action buttons visible in cooking mode (Edit, Delete, Print, etc.)
- Simple "Back to Recipes" button at bottom

**Visual Hierarchy:**
```
┌─────────────────────────┐
│  RECIPE TITLE           │ ← Big, bold
│  ⏱️ 20 min | 🍽️ 4 serv │ ← Compact meta
├─────────────────────────┤
│  INGREDIENTS            │ ← Bold header
│  □ 2 cups flour        │ ← Big text, quantity bold
│  □ 1 stick butter      │
│  □ 3 eggs              │
├─────────────────────────┤
│  INSTRUCTIONS           │ ← Bold header
│  ①  Preheat oven...    │ ← Big number + text
│                         │
│  ②  Mix flour and...   │ ← Clear separation
│                         │
│  ③  Add eggs one...    │
└─────────────────────────┘
    [Back to Recipes]      ← Bottom, unobtrusive
```

**Special Mobile Features:**
1. **Sticky Ingredient Summary:** Ingredients can "stick" to top when scrolling instructions
2. **Step Highlighting:** Tap a step to highlight it (optional)
3. **Auto-Scroll Mode:** Auto-advance to next step with timer (future enhancement)
4. **Wake Lock:** Keep screen on while in cooking mode (JavaScript Wake Lock API)

**Implementation Options:**

**Option A: Dedicated Cooking Mode (Recommended)**
- Add "👨‍🍳 Cooking Mode" button to recipe detail
- Opens full-screen mobile-optimized view
- URL: `/cooking.html?recipe_id=123` (shareable, bookmarkable)
- Completely different UI from normal recipe view
- Can be PWA-enabled (Add to Home Screen)

**Option B: Responsive CSS Only**
- Heavy CSS media queries for mobile
- Transform existing recipe detail view
- Simpler to implement but less flexible

**Recommendation:** Option A - Dedicated cooking mode gives best UX

---

## Problem 2: User Authentication (Passwordless & Frictionless)

### Current Issues
- Contributors exist, but no way to identify "who is using the app right now"
- Can't segregate events by contributor
- No way to know "whose event is this?"

### Solution: Email-Based Identity (No Passwords)

**Core Principle:** Identity without impediment

#### How It Works

**First-Time User Flow:**
```
1. User visits app → Sees "Who are you?" prompt
2. Enters email address (e.g., janet@example.com)
3. App sends 6-digit code to email (via Netlify Function + email service)
4. User enters code in app
5. App stores identity in localStorage + session cookie
6. User is "logged in" - can create events, import recipes, etc.
```

**Returning User Flow:**
```
1. User visits app → localStorage has email
2. App shows "Welcome back, Janet!"
3. User can continue immediately (no re-auth needed)
4. Can switch users via "Not you?" link
```

**Session Management:**
- Store in `localStorage`: `{ user_email, user_name, verified_at, session_token }`
- Sessions persist indefinitely on device (like WhatsApp Web)
- Can "log out" and switch users anytime
- No server-side session management needed

#### Technical Implementation

**Email Verification Service Options:**
1. **SendGrid API** (Free tier: 100 emails/day)
2. **AWS SES** (Cheap, reliable)
3. **Resend.com** (Developer-friendly, 3000 emails/month free)
4. **Mailgun** (Reliable, 5000 emails/month free on trial)

**Recommended:** Resend.com (best DX, generous free tier)

**Netlify Function:** `send-verification-code.js`
```javascript
// POST { email }
// Generates 6-digit code
// Stores in Dropbox: /verification-codes.json (with expiry)
// Sends email with code
// Returns: { success: true, code_sent: true }
```

**Netlify Function:** `verify-code.js`
```javascript
// POST { email, code }
// Checks code in Dropbox verification-codes.json
// If valid, generates session_token
// Returns: { success: true, session_token, user }
```

**Email Template:**
```
Subject: Your Fergi Cooking verification code

Hi there!

Your verification code is: 123456

This code expires in 10 minutes.

If you didn't request this, you can safely ignore this email.

Happy Cooking!
- Fergi Cooking App
```

**UI Components:**

**Login Modal (First Visit):**
```
┌───────────────────────────────┐
│  Welcome to Fergi Cooking!    │
│                               │
│  Who are you?                 │
│                               │
│  [email input              ]  │
│  [Continue]                   │
│                               │
│  Or browse recipes as guest   │
└───────────────────────────────┘
```

**Verification Modal:**
```
┌───────────────────────────────┐
│  Check your email!            │
│                               │
│  We sent a code to:           │
│  janet@example.com            │
│                               │
│  Enter code: [  ][  ][  ]     │
│              [  ][  ][  ]     │
│                               │
│  [Verify]  [Resend Code]      │
└───────────────────────────────┘
```

**User Status (Header):**
```
┌───────────────────────────────┐
│  Fergi Cooking    👤 Janet ▼  │ ← Dropdown
└───────────────────────────────┘
     Dropdown menu:
     - My Events
     - My Recipes
     - Settings
     - Not you? Switch User
```

**Guest Mode:**
- Can browse and view recipes
- Can respond to event invitations (existing feature)
- CANNOT create events or import recipes
- Sees "Sign in to create events" prompt

---

## Problem 3: Event Segregation by User

### Current Issues
- All events are in one big list (`events.json`)
- No ownership or filtering by contributor
- Anyone can edit/delete any event

### Solution: User-Owned Events

**Data Model Change:**

**events.json structure (NEW):**
```json
{
  "events": [
    {
      "id": "evt_001",
      "title": "Janet's Holiday Dinner",
      "date": "2025-12-25",
      "time": "18:00",
      "location": "Janet's House",
      "description": "Annual Christmas dinner",
      "owner_email": "janet@example.com",  ← NEW
      "owner_name": "Janet Mason",          ← NEW
      "created_by": "janet@example.com",    ← NEW
      "created_at": "2025-11-03T10:30:00Z",
      "recipes": [1, 5, 12],
      "guest_selections": {...}
    },
    {
      "id": "evt_002",
      "title": "Joe's BBQ Party",
      "owner_email": "joe@fergi.com",       ← Different owner
      "owner_name": "Joe Ferguson",
      "recipes": [22, 33],
      ...
    }
  ]
}
```

**Access Control (Simple Rules):**
1. **View Events:** Anyone can view events (public access)
2. **Create Events:** Must be logged in (verified email)
3. **Edit Events:** Only the owner (matching `owner_email`)
4. **Delete Events:** Only the owner
5. **Generate Invitations:** Only the owner
6. **Add Recipes to Event:** Only the owner

**UI Changes:**

**Events Page (`events.html`):**
- Header: "My Events" (when logged in) or "All Events" (guest)
- Filter tabs: `[My Events] [All Events]` (when logged in)
- Event cards show owner: "Created by Janet Mason"
- Edit/Delete buttons only visible for owned events
- Guest users see "Sign in to create events" message

**Event Creation:**
- Automatically sets `owner_email` and `owner_name` from current user
- No manual selection needed

**Email Invitations:**
- Subject line: "You're invited to Janet's Holiday Dinner"
- From name: "Janet Mason (via Fergi Cooking)"
- Reply-to: Janet's email (owner_email)

**Event Dashboard (`event-detail.html`):**
- Shows "Created by [Name]" at top
- Owner sees all controls (add recipes, generate email, etc.)
- Non-owners see read-only view
- Guests can still respond (existing feature)

---

## Implementation Plan

### Phase 1: Mobile Cooking Mode (High Priority - Janet's Issue)
**Effort:** 4-6 hours
**Files to Create/Modify:**
- Create: `cooking.html` (mobile-optimized recipe view)
- Create: `cooking.css` (mobile-first styles)
- Create: `netlify/functions/get-recipe-for-cooking.js` (simplified API)
- Modify: `index.html` (add "Cooking Mode" button to recipe detail)

**Deliverables:**
- ✅ Mobile-optimized recipe reading interface
- ✅ Large text, clear hierarchy
- ✅ Shareable cooking URLs
- ✅ Wake Lock API to keep screen on
- ✅ Responsive for all phone sizes

### Phase 2: Email-Based Authentication (Medium Priority)
**Effort:** 6-8 hours
**Files to Create/Modify:**
- Create: `netlify/functions/send-verification-code.js`
- Create: `netlify/functions/verify-code.js`
- Modify: `index.html` (add login modal and user status)
- Modify: `events.html` (add login prompt)
- Modify: `add-recipe.html` (require login)
- Add: Email service integration (Resend.com or SendGrid)

**Environment Variables (Netlify):**
- `EMAIL_SERVICE_API_KEY` - Resend.com API key
- `EMAIL_FROM_ADDRESS` - noreply@fergi.com (or similar)

**Deliverables:**
- ✅ Passwordless email authentication
- ✅ 6-digit verification codes
- ✅ Session persistence (localStorage)
- ✅ User switching capability
- ✅ Guest mode (browse-only)

### Phase 3: Event Segregation (Medium Priority)
**Effort:** 4-5 hours
**Files to Create/Modify:**
- Modify: `netlify/functions/create-event.js` (add owner_email)
- Modify: `netlify/functions/get-events.js` (add filtering)
- Modify: `events.html` (show ownership, filter controls)
- Modify: `event-detail.html` (show owner, access control)
- Modify: `netlify/functions/generate-email.js` (owner's name in email)

**Data Migration:**
- Run one-time script to assign `owner_email` to existing events (default to Joe/Fergi)

**Deliverables:**
- ✅ Events owned by creators
- ✅ "My Events" filtering
- ✅ Access control (edit/delete)
- ✅ Personalized invitation emails
- ✅ Multi-user event management

---

## User Experience Flow (Complete)

### Scenario: Janet wants to cook Beef Stroganoff

**Desktop/Tablet:**
```
1. Opens https://fergi-cooking.netlify.app
2. Sees "Welcome back, Janet!" in header
3. Searches "stroganoff"
4. Clicks recipe card
5. Clicks "👨‍🍳 Cooking Mode" button
6. Phone: Opens cooking.html?recipe=5 in mobile view
7. Phone is in kitchen, recipe is READABLE, large text
8. Cooks successfully! ⭐
```

**Mobile Direct:**
```
1. Opens app on phone
2. Searches "stroganoff"
3. Clicks recipe
4. Already in mobile view, but...
5. Clicks "👨‍🍳 Cooking Mode" for EXTRA-LARGE text
6. Full-screen cooking interface appears
7. Can quickly glance at ingredients and steps while cooking
8. Screen stays on (Wake Lock API)
```

### Scenario: Nancy wants to create an event

**First-Time User:**
```
1. Opens app
2. Clicks "Events"
3. Sees "Sign in to create events"
4. Clicks "Sign In"
5. Enters email: nancy@example.com
6. Receives code: 789456
7. Enters code, verified! ✓
8. Now sees "Create Event" button
9. Creates "Nancy's Brunch" event
10. Adds recipes from collection
11. Generates invitation email
12. Copies and sends to guests
```

**Returning User:**
```
1. Opens app
2. Header shows "👤 Nancy ▼"
3. Clicks "Events" → Goes directly to "My Events"
4. Sees only Nancy's events (not Janet's or Joe's)
5. Clicks event, manages recipes, generates invitations
```

### Scenario: Guest receives invitation

**No Change (Existing Feature):**
```
1. Receives email invitation from Nancy
2. Clicks link to respond.html?event=evt_123&guest=guest@example.com
3. Selects recipe preferences
4. Indicates "will bring" or "prefer"
5. Submits (no login required for guests!)
```

---

## Technical Architecture Summary

### Authentication Flow
```
User → Enter Email → Netlify Function (send-verification-code.js)
     → Email Service (Resend.com) → User receives code
     → User enters code → Netlify Function (verify-code.js)
     → Session token generated → Stored in localStorage
     → User identified for all future requests
```

### Event Ownership Flow
```
User creates event → owner_email auto-filled from localStorage
→ Saved to Dropbox events.json
→ get-events.js filters by owner_email when "My Events" requested
→ UI shows edit/delete only for matching owner_email
```

### Mobile Cooking Flow
```
User views recipe → Clicks "Cooking Mode"
→ Opens cooking.html?recipe_id=X
→ Loads recipe via get-recipe.js
→ Displays with mobile-first CSS
→ Wake Lock API keeps screen on
→ User cooks with readable text! 🎉
```

---

## Database Changes

### New Collections in Dropbox

**verification-codes.json:**
```json
{
  "codes": [
    {
      "email": "janet@example.com",
      "code": "123456",
      "created_at": "2025-11-03T10:30:00Z",
      "expires_at": "2025-11-03T10:40:00Z",
      "verified": false
    }
  ]
}
```

**users.json (optional, for future):**
```json
{
  "users": [
    {
      "email": "janet@example.com",
      "name": "Janet Mason",
      "created_at": "2025-11-03T10:30:00Z",
      "last_login": "2025-11-03T14:22:00Z",
      "session_token": "tok_abc123xyz",
      "preferences": {
        "default_view": "my_events",
        "email_notifications": true
      }
    }
  ]
}
```

### Modified Collections

**events.json:** Add `owner_email`, `owner_name`, `created_by` fields
**recipes.json:** No changes needed (contributor field already exists)

---

## Security Considerations

### What We DO:
✅ Email verification (proves email ownership)
✅ Session tokens (random, unpredictable)
✅ Access control (owner-only edit/delete)
✅ Code expiration (10 minutes)
✅ HTTPS everywhere (Netlify default)

### What We DON'T:
❌ No passwords (reduced attack surface)
❌ No password resets (nothing to reset)
❌ No user registration forms (email only)
❌ No 2FA (overkill for recipe app)
❌ No rate limiting (Netlify handles this)

### Privacy:
- Emails stored in Dropbox (Joe's account)
- No third-party tracking
- No analytics (optional: privacy-friendly analytics later)
- Guest mode available (no login required to browse)

---

## Open Questions / Decisions Needed

### 1. Email Service Choice
**Options:**
- Resend.com (Recommended: best DX, 3000/month free)
- SendGrid (Reliable, 100/day free)
- AWS SES (Cheapest at scale, requires AWS setup)
- Mailgun (Good, but complex pricing)

**Decision:** Resend.com unless you prefer AWS SES

### 2. User Name Handling
**Question:** Where does "Janet Mason" come from?
**Options:**
- A) Ask during first verification ("What's your name?")
- B) Look up from contributors list by email domain matching
- C) Infer from email (janet@example.com → "Janet")
- D) Let user set in profile later

**Recommendation:** Option A (ask during verification)

### 3. Cooking Mode URL Structure
**Options:**
- A) `/cooking.html?recipe_id=123` (separate page)
- B) `/recipe.html?id=123&mode=cooking` (mode parameter)
- C) Same page, just CSS (no separate URL)

**Recommendation:** Option A (cleanest, most flexible)

### 4. Contributor vs User Relationship
**Question:** Is a "contributor" the same as a "user"?
**Current:**
- Contributors: Janet Mason, Fergi, Nancy, Lauren, The Cooks
- Users: (new concept, anyone who logs in)

**Options:**
- A) Contributors and Users are separate concepts
  - Contributors = recipe creators (curated list)
  - Users = anyone who logs in (can create events)
- B) Contributors automatically become Users (email-based matching)
- C) All Users are Contributors (add to list on first login)

**Recommendation:** Option A (separation of concerns)
- Contributors remain a curated list for recipe attribution
- Users are anyone who logs in (broader)
- A user CAN be a contributor, but not required

---

## Success Metrics

### Mobile Cooking Mode Success:
✅ Janet can read recipes on phone without zooming
✅ Text is large enough to read from 2 feet away
✅ All cooking information visible with minimal scrolling
✅ Screen stays on while cooking
✅ No complaints about readability

### Authentication Success:
✅ Users can log in within 30 seconds
✅ No password frustration
✅ Sessions persist between visits
✅ Clear indication of "who you are"

### Event Segregation Success:
✅ Each user sees only their events in "My Events"
✅ Users can't accidentally edit others' events
✅ Invitation emails come "from" event owner
✅ Multiple family members can use app independently

---

## Timeline Estimate

**Phase 1 (Mobile Cooking):** 1-2 days (4-6 hours active work)
**Phase 2 (Authentication):** 2-3 days (6-8 hours active work)
**Phase 3 (Event Segregation):** 1-2 days (4-5 hours active work)

**Total:** 4-7 days (14-19 hours) for complete implementation

**Priority Order:**
1. **Mobile Cooking Mode** (Janet's immediate pain point)
2. **Authentication** (enables event segregation)
3. **Event Segregation** (completes multi-user functionality)

---

## Design Mockups (Text-Based)

### Mobile Cooking Mode (iPhone 13 Mini, 375px wide)

```
┌─────────────────────────────────────┐
│ ← Fergi Cooking                     │ ← Header, fixed
├─────────────────────────────────────┤
│                                     │
│     BEEF STROGANOFF                 │ ← 28px, bold
│                                     │
│  ⏱️ 30 min | 🍽️ 4 servings         │ ← 16px, gray
│                                     │
├─────────────────────────────────────┤
│  INGREDIENTS                        │ ← 21px, bold
│                                     │
│  2 lbs beef sirloin, sliced        │ ← 18px
│  1 stick butter                     │   Generous
│  1 large onion, diced              │   Line spacing
│  8 oz mushrooms, sliced            │   (1.8x)
│  2 cups beef broth                 │
│  1 cup sour cream                  │
│  2 tbsp flour                      │
│                                     │
├─────────────────────────────────────┤
│  INSTRUCTIONS                       │ ← 21px, bold
│                                     │
│  ① Slice beef into thin strips     │ ← 18px text
│     against the grain.              │   Big number
│                                     │   (22px, bold)
│  ───────────────────────────────   │
│                                     │
│  ② Heat butter in large skillet    │
│     over medium-high heat.          │
│                                     │
│  ───────────────────────────────   │
│                                     │
│  ③ Add beef and cook until         │
│     browned, about 5 minutes.       │
│                                     │
│  ───────────────────────────────   │
│                                     │
│  (more steps...)                    │
│                                     │
├─────────────────────────────────────┤
│         [Back to Recipes]           │ ← Bottom, 1rem padding
└─────────────────────────────────────┘
```

**Key Features:**
- ✅ BIG text (18px base, up from typical 14-16px)
- ✅ Bold quantities automatically stand out
- ✅ Clear step separation (lines between steps)
- ✅ Numbered steps in large circles/badges
- ✅ No wasted space on buttons or UI chrome
- ✅ Everything readable from 2 feet away

---

## Next Steps

### Immediate Actions (Today):
1. ✅ Review and approve this design spec
2. Decide on:
   - Email service (Resend.com recommended)
   - User name handling (ask during verification recommended)
   - Cooking mode URL structure (separate page recommended)
   - Contributor vs User relationship (separate concepts recommended)

### Implementation Order:
1. **Start with Phase 1** (Mobile Cooking Mode) - solves Janet's immediate problem
2. **Then Phase 2** (Authentication) - enables multi-user features
3. **Finally Phase 3** (Event Segregation) - completes the vision

### Questions for You:
- Does this solve the three core problems?
- Any concerns about the passwordless email approach?
- Should we add any other mobile cooking features?
- Timeline acceptable? (4-7 days total)

---

**Status:** ✅ DESIGN COMPLETE - Ready for implementation approval
**Next:** Get approval on decisions, then start Phase 1 (Mobile Cooking Mode)

---

📊 **Context: 47,321 / 200,000 tokens (23.7% used, 76.3% remaining)**
