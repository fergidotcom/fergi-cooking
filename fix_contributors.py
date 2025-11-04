#!/usr/bin/env python3
"""
Fix Contributor Assignments
- Change all "Janet Mason" to "Janet"
- Assign "Fergi" as contributor for all recipes without a contributor
"""

import json
import sys

def fix_contributors():
    print("🔧 Starting contributor fix...")

    # Load recipes
    print("📖 Loading recipes.json...")
    with open('recipes.json', 'r', encoding='utf-8') as f:
        recipes = json.load(f)

    print(f"✅ Loaded {len(recipes)} recipes")

    # Track changes
    janet_count = 0
    fergi_count = 0
    no_contributor_count = 0

    # Update recipes
    for recipe in recipes:
        # Check if recipe has contributor field
        if 'contributor' not in recipe or recipe['contributor'] is None or recipe['contributor'] == '':
            # Check if it's a Janet Mason recipe (by source_attribution or file_path)
            is_janet = False
            if recipe.get('source_attribution'):
                is_janet = 'Janet Mason' in recipe['source_attribution']
            if not is_janet and recipe.get('file_path'):
                is_janet = recipe['file_path'].startswith('Janet Mason/')

            if is_janet:
                recipe['contributor'] = 'Janet'
                janet_count += 1
            else:
                recipe['contributor'] = 'Fergi'
                fergi_count += 1
            no_contributor_count += 1
        elif recipe['contributor'] == 'Janet Mason':
            # Change "Janet Mason" to "Janet"
            recipe['contributor'] = 'Janet'
            janet_count += 1

    # Save updated recipes
    print("\n💾 Saving updated recipes...")
    with open('recipes.json', 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Update complete!")
    print(f"📊 Statistics:")
    print(f"   - Total recipes: {len(recipes)}")
    print(f"   - Recipes updated: {no_contributor_count}")
    print(f"   - Assigned to Janet: {janet_count}")
    print(f"   - Assigned to Fergi: {fergi_count}")

    # Count current contributors
    contributor_counts = {}
    for recipe in recipes:
        contrib = recipe.get('contributor', 'Unknown')
        contributor_counts[contrib] = contributor_counts.get(contrib, 0) + 1

    print(f"\n📈 Contributor breakdown:")
    for contrib, count in sorted(contributor_counts.items()):
        print(f"   - {contrib}: {count} recipes")

if __name__ == '__main__':
    fix_contributors()
