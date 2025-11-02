"""
Export recipes database to JSON format for Netlify deployment
This creates a single JSON file that can be easily accessed by serverless functions
"""

import sqlite3
import json
from pathlib import Path

def export_database_to_json(db_path='recipes.db', output_path='recipes.json'):
    """Export complete database to JSON"""

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all recipes
    cursor.execute("""
        SELECT * FROM recipes
        ORDER BY id
    """)
    recipes = []

    for recipe_row in cursor.fetchall():
        recipe = dict(recipe_row)
        recipe_id = recipe['id']

        # Get ingredients
        cursor.execute("""
            SELECT * FROM ingredients
            WHERE recipe_id = ?
            ORDER BY ingredient_order
        """, (recipe_id,))
        recipe['ingredients'] = [dict(row) for row in cursor.fetchall()]

        # Get instructions
        cursor.execute("""
            SELECT * FROM instructions
            WHERE recipe_id = ?
            ORDER BY step_number
        """, (recipe_id,))
        recipe['instructions'] = [dict(row) for row in cursor.fetchall()]

        # Get tags
        cursor.execute("""
            SELECT t.tag_name FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
        """, (recipe_id,))
        recipe['tags'] = [row['tag_name'] for row in cursor.fetchall()]

        # Get images
        cursor.execute("""
            SELECT * FROM recipe_images
            WHERE recipe_id = ?
            ORDER BY display_order
        """, (recipe_id,))
        recipe['images'] = [dict(row) for row in cursor.fetchall()]

        recipes.append(recipe)

    conn.close()

    # Write to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported {len(recipes)} recipes to {output_path}")
    print(f"📊 File size: {Path(output_path).stat().st_size / 1024:.1f} KB")

    return len(recipes)


if __name__ == '__main__':
    count = export_database_to_json()
    print(f"\n🎉 Export complete! {count} recipes ready for deployment.")
