# Create Fergi Cooking Dropbox App

**Action Required:** Create a dedicated Dropbox app for Fergi Cooking (2 minutes)

---

## Why a Dedicated App?

Reference Refinement has its own app folder (`/Apps/Reference Refinement/`), and Fergi Cooking should have its own (`/Apps/Fergi Cooking/`). This keeps the projects separate and organized.

---

## Step-by-Step Instructions

### 1. Go to Dropbox Developers Console

Visit: **https://www.dropbox.com/developers/apps**

### 2. Create New App

Click **"Create app"** button

### 3. Choose Settings:

**Choose an API:**
- Select: ☑️ **"Scoped access"**

**Choose the type of access you need:**
- Select: ☑️ **"App folder"** (not Full Dropbox)
  - This creates `/Apps/Fergi Cooking/` folder
  - App can only access files in this folder
  - More secure and organized

**Name your app:**
- Enter: **"Fergi Cooking"**
- Note: Must be unique across all Dropbox apps
- If taken, try: "Fergi Cooking Recipes" or "Fergi Recipe Manager"

Click **"Create app"**

### 4. Configure Permissions

You'll be on the app settings page.

**Go to "Permissions" tab:**
- Enable: ☑️ **files.content.write**
- Enable: ☑️ **files.content.read**
- Click **"Submit"** button at bottom

### 5. Get App Credentials

**Go back to "Settings" tab:**

Find these values:

**App key:** (example: `abc123xyz456`)
- This is your `DROPBOX_APP_KEY`
- Copy this - you'll need it!

**App secret:** (click "Show" to reveal)
- This is your `DROPBOX_APP_SECRET`
- Copy this - you'll need it!

---

## What You'll Have:

```
DROPBOX_APP_KEY=abc123xyz456          ← From Settings tab
DROPBOX_APP_SECRET=your_secret_here   ← From Settings tab (click Show)
```

---

## Update Configuration (Next Steps)

Once you have these values:

1. **Tell me the App Key:**
   - Share the `DROPBOX_APP_KEY` value
   - I'll update the code with it

2. **Set App Secret in Netlify:**
   ```bash
   netlify env:set DROPBOX_APP_SECRET "your_secret_here"
   ```

3. **Redeploy:**
   - I'll redeploy with the new configuration
   - Ready to use!

---

## App Folder Location

Once created, your recipes will be stored at:

**In Dropbox:**
- `/Apps/Fergi Cooking/recipes.json`

**On Your Mac (synced):**
- `~/Library/CloudStorage/Dropbox/Apps/Fergi Cooking/recipes.json`

This is completely separate from Reference Refinement:
- `/Apps/Reference Refinement/decisions.txt` ← Reference Refinement
- `/Apps/Fergi Cooking/recipes.json` ← Fergi Cooking (NEW)

---

## Security Notes

**App Folder Access:**
- Fergi Cooking app can ONLY access `/Apps/Fergi Cooking/`
- Cannot see or modify other folders
- Cannot see Reference Refinement's folder
- Most secure option for app data

**Access Control:**
- You control the app
- You can revoke access anytime at dropbox.com/account/connected_apps
- OAuth tokens expire and refresh automatically

---

## Troubleshooting

### "Name already taken"
- Try: "Fergi Cooking Recipes"
- Or: "Fergi Recipe Manager"
- Or: "Fergi Kitchen"

### "Can't find Permissions tab"
- Make sure you selected "Scoped access" (not OAuth 1)
- Refresh the page
- Try a different browser

### "App secret not showing"
- Click the "Show" button next to it
- Copy the entire value
- Don't share this secret publicly

---

## Ready?

Create the app now, then share the **App Key** with me and I'll update the code!

The **App Secret** needs to be set in Netlify:
```bash
netlify env:set DROPBOX_APP_SECRET "your_secret_value"
```

---

**This is a one-time setup** - once configured, it works forever! 🚀
