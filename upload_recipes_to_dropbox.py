#!/usr/bin/env python3
"""
Upload recipes.json to Dropbox root directory
This is a one-time setup script to initialize the Dropbox storage
"""

import dropbox
import sys

# You'll need to get an access token from:
# https://www.dropbox.com/developers/apps
# Create an app, generate an access token with files.content.write permission

def upload_recipes():
    # Get access token from command line or environment
    if len(sys.argv) < 2:
        print("Usage: python3 upload_recipes_to_dropbox.py <DROPBOX_ACCESS_TOKEN>")
        print("\nTo get a token:")
        print("1. Go to https://www.dropbox.com/developers/apps")
        print("2. Create/select 'Fergi Cooking' app")
        print("3. Go to 'Permissions' tab")
        print("4. Enable 'files.content.write' and 'files.content.read'")
        print("5. Go to 'Settings' tab")
        print("6. Generate access token")
        print("7. Run: python3 upload_recipes_to_dropbox.py <TOKEN>")
        sys.exit(1)

    access_token = sys.argv[1]

    # Initialize Dropbox client
    dbx = dropbox.Dropbox(access_token)

    # Read recipes.json
    print("Reading recipes.json...")
    with open('recipes.json', 'rb') as f:
        file_data = f.read()

    print(f"File size: {len(file_data) / 1024:.1f} KB")

    # Upload to Dropbox root
    print("Uploading to Dropbox:/recipes.json...")
    try:
        dbx.files_upload(
            file_data,
            '/recipes.json',
            mode=dropbox.files.WriteMode.overwrite,
            autorename=False
        )
        print("✓ Upload successful!")
        print("\nThe file is now available at Dropbox:/recipes.json")
        print("Your Fergi Cooking website can now load recipes from Dropbox!")

    except Exception as e:
        print(f"✗ Upload failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    upload_recipes()
