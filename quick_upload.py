#!/usr/bin/env python3
"""
Quick upload script - paste your token directly in the code
"""
import dropbox
import sys

# PASTE YOUR DROPBOX ACCESS TOKEN HERE (between the quotes):
TOKEN = ""

if not TOKEN:
    print("ERROR: Please edit this file and paste your Dropbox token on line 9")
    print("Open quick_upload.py and set TOKEN = 'your_token_here'")
    sys.exit(1)

try:
    print("Connecting to Dropbox...")
    dbx = dropbox.Dropbox(TOKEN)

    # Test connection
    account = dbx.users_get_current_account()
    print(f"✓ Connected as: {account.name.display_name} ({account.email})")

    # Read and upload file
    print("Reading recipes.json...")
    with open('recipes.json', 'rb') as f:
        file_data = f.read()

    print(f"Uploading {len(file_data) / 1024:.1f} KB to Dropbox...")
    dbx.files_upload(
        file_data,
        '/recipes.json',
        mode=dropbox.files.WriteMode.overwrite,
        autorename=False
    )

    print("\n" + "=" * 70)
    print("✓ SUCCESS! recipes.json uploaded to Dropbox")
    print("=" * 70)
    print("\nFile location: /Apps/Reference Refinement/recipes.json")
    print("\nNow refresh https://fergi-cooking.netlify.app to see your recipes!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    sys.exit(1)
