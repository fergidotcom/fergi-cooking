# Bug Fix: Contributor Filter Error

**Date:** November 4, 2025
**Version:** v3.1.3
**Status:** ✅ Fixed and Deployed

## Problem

When selecting "Janet Mason" (or any contributor) from the contributor dropdown filter, users received this error:

```
Error filtering recipes: The string did not match the expected pattern.
```

## Root Cause

The `filterByContributor()` function in `index.html` was calling `/api/get-recipes`, but the Netlify redirect rules in `netlify.toml` only had a redirect for `/api/recipes`, not `/api/get-recipes`.

**Code Issue (line 1721 in index.html):**
```javascript
let url = `${this.apiUrl}/get-recipes`;  // ❌ No redirect rule for this!
```

**Available Redirect Rule (netlify.toml lines 24-27):**
```toml
[[redirects]]
  from = "/api/recipes"
  to = "/.netlify/functions/get-recipes"
  status = 200
```

## Solution

Changed the `filterByContributor()` function to use `/api/recipes` instead of `/api/get-recipes`:

```javascript
let url = `${this.apiUrl}/recipes`;  // ✅ Uses existing redirect rule
```

## Changes Made

**File Modified:**
- `index.html` - Line 1723: Changed URL from `/api/get-recipes` to `/api/recipes`

**Additional Improvements:**
- Added stats section hiding when filtering (consistent with other filter functions)
- Added console log to show number of filtered recipes
- Version bumped to v3.1.3

## Testing

✅ Local testing with `netlify dev` confirmed fix works
✅ Deployed to production at https://fergi-cooking.netlify.app
✅ Contributor filter now works correctly

## Related Files

- `index.html` (line 1723) - Frontend filter function
- `netlify.toml` (lines 24-27) - Redirect configuration
- `netlify/functions/get-recipes.js` (lines 87-92) - Backend filtering logic

## Deployment

```bash
netlify deploy --prod --dir="." --message="v3.1.3 - Fix contributor filter URL"
```

**Live URL:** https://fergi-cooking.netlify.app
**Deploy Time:** November 4, 2025

---

**Status:** ✅ Fixed and verified working in production
