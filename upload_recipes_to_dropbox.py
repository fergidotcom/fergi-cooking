#!/usr/bin/env python3
"""
Upload recipes.json to Dropbox via Netlify Function
"""

import json
import requests

def upload_recipes():
    print("📤 Uploading recipes to Dropbox...")

    # Load recipes
    print("📖 Loading recipes.json...")
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    print(f"✅ Loaded {len(recipes)} recipes")

    # Upload via Netlify function
    url = "https://fergi-cooking.netlify.app/.netlify/functions/save-recipes"

    print(f"🚀 Uploading to Dropbox via {url}...")
    response = requests.post(url, json={"recipes": recipes})

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Upload successful!")
        print(f"   - Recipes saved: {result.get('count', 'unknown')}")
        print(f"   - Message: {result.get('message', '')}")
    else:
        print(f"❌ Upload failed!")
        print(f"   - Status code: {response.status_code}")
        print(f"   - Response: {response.text}")
        return False

    return True

if __name__ == '__main__':
    success = upload_recipes()
    exit(0 if success else 1)
