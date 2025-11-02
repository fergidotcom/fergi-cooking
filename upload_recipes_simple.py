#!/usr/bin/env python3
"""
Simple interactive script to upload recipes.json to Dropbox
"""

import dropbox
import sys
import os

def upload_recipes():
    print("=" * 70)
    print("Fergi Cooking - Upload recipes.json to Dropbox")
    print("=" * 70)
    print()

    # Check if file exists
    if not os.path.exists('recipes.json'):
        print("❌ Error: recipes.json not found in current directory")
        sys.exit(1)

    file_size = os.path.getsize('recipes.json') / 1024
    print(f"✓ Found recipes.json ({file_size:.1f} KB)")
    print()

    print("To upload to Dropbox, you need an access token.")
    print()
    print("Quick setup (2 minutes):")
    print("1. Visit: https://www.dropbox.com/developers/apps")
    print("2. Click on 'Fergi Cooking' app (or create it if needed)")
    print("3. Go to 'Permissions' tab")
    print("   - Enable: files.content.write")
    print("   - Enable: files.content.read")
    print("   - Click 'Submit' to save")
    print("4. Go to 'Settings' tab")
    print("5. Scroll to 'Generated access token'")
    print("6. Click 'Generate' button")
    print("7. Copy the token (starts with 'sl.xxxxx')")
    print()
    print("=" * 70)
    print()

    # Get token from user
    token = input("Paste your access token here (or press Enter to cancel): ").strip()

    if not token:
        print("\n❌ Cancelled - no token provided")
        sys.exit(0)

    print()
    print("Connecting to Dropbox...")

    try:
        dbx = dropbox.Dropbox(token)

        # Test connection
        account = dbx.users_get_current_account()
        print(f"✓ Connected as: {account.name.display_name} ({account.email})")
        print()

        # Read file
        print("Reading recipes.json...")
        with open('recipes.json', 'rb') as f:
            file_data = f.read()

        # Upload
        print(f"Uploading to Dropbox:/recipes.json ({len(file_data) / 1024:.1f} KB)...")
        dbx.files_upload(
            file_data,
            '/recipes.json',
            mode=dropbox.files.WriteMode.overwrite,
            autorename=False
        )

        print()
        print("=" * 70)
        print("✓ SUCCESS! recipes.json uploaded to Dropbox")
        print("=" * 70)
        print()
        print("File location:")
        print("  Dropbox: /Apps/Reference Refinement/recipes.json")
        print("  Mac:     ~/Library/CloudStorage/Dropbox/Apps/Reference Refinement/")
        print()
        print("Note: Uses same Dropbox app as Reference Refinement project")
        print("      Both projects share the /Apps/Reference Refinement/ folder")
        print()
        print("Next steps:")
        print("1. Visit: https://fergi-cooking.netlify.app")
        print("2. Click 'Connect Dropbox'")
        print("3. Authorize the app (same as Reference Refinement)")
        print("4. Your recipes will load automatically!")
        print()

    except dropbox.exceptions.AuthError:
        print()
        print("❌ Authentication failed - invalid token")
        print()
        print("Make sure you:")
        print("- Copied the entire token (including 'sl.' prefix)")
        print("- Enabled required permissions (files.content.write, files.content.read)")
        print("- Generated a new token (old tokens may expire)")
        sys.exit(1)

    except Exception as e:
        print()
        print(f"❌ Upload failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    upload_recipes()
