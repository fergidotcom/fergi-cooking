#!/usr/bin/env python3
import dropbox, sys
token = sys.argv[1] if len(sys.argv) > 1 else ""
if not token: print("Usage: python3 upload.py YOUR_TOKEN"); sys.exit(1)
dbx = dropbox.Dropbox(token)
print(f"Connected as: {dbx.users_get_current_account().name.display_name}")
with open('recipes.json', 'rb') as f: data = f.read()
print(f"Uploading {len(data)/1024:.0f}KB...")
dbx.files_upload(data, '/recipes.json', mode=dropbox.files.WriteMode.overwrite)
print("✓ SUCCESS! Refresh https://fergi-cooking.netlify.app")
