#!/usr/bin/env python3
"""
Remove recipes that cannot be fully interpreted from the database.
Only keep recipes that have either ingredients OR instructions.
"""

import sqlite3
import sys

def cleanup_incomplete_recipes(db_path='recipes.db'):
    """Remove recipes with no ingredients AND no instructions."""

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Find recipes with no ingredients AND no instructions
        cursor.execute("""
            SELECT
                r.id,
                r.title,
                r.original_filename,
                COUNT(DISTINCT i.id) as ingredient_count,
                COUNT(DISTINCT ins.id) as instruction_count
            FROM recipes r
            LEFT JOIN ingredients i ON r.id = i.recipe_id
            LEFT JOIN instructions ins ON r.id = ins.recipe_id
            GROUP BY r.id
            HAVING ingredient_count = 0 AND instruction_count = 0
            ORDER BY r.id
        """)

        incomplete_recipes = cursor.fetchall()

        if not incomplete_recipes:
            print("✓ No incomplete recipes found. Database is clean!")
            return 0

        print(f"\nFound {len(incomplete_recipes)} incomplete recipes to remove:\n")

        # Show what will be deleted
        for recipe_id, title, filename, ing_count, inst_count in incomplete_recipes[:10]:
            print(f"  - ID {recipe_id}: {title} ({filename})")

        if len(incomplete_recipes) > 10:
            print(f"  ... and {len(incomplete_recipes) - 10} more")

        # Ask for confirmation
        print(f"\n⚠️  About to DELETE {len(incomplete_recipes)} recipes from the database.")
        response = input("Continue? (yes/no): ").strip().lower()

        if response != 'yes':
            print("❌ Cancelled. No recipes were deleted.")
            return 0

        # Delete the recipes (CASCADE will handle related tables)
        recipe_ids = [r[0] for r in incomplete_recipes]
        placeholders = ','.join('?' * len(recipe_ids))

        cursor.execute(f"DELETE FROM recipes WHERE id IN ({placeholders})", recipe_ids)
        conn.commit()

        print(f"\n✓ Successfully deleted {len(incomplete_recipes)} incomplete recipes")

        # Show summary of remaining recipes
        cursor.execute("""
            SELECT COUNT(*) FROM recipes
        """)
        remaining = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                COUNT(*)
            FROM recipes r
            INNER JOIN ingredients i ON r.id = i.recipe_id
        """)
        with_ingredients = cursor.fetchone()[0]

        cursor.execute("""
            SELECT
                COUNT(*)
            FROM recipes r
            INNER JOIN instructions ins ON r.id = ins.recipe_id
        """)
        with_instructions = cursor.fetchone()[0]

        print(f"\n📊 Database Summary:")
        print(f"  Total recipes: {remaining}")
        print(f"  With ingredients: {with_ingredients}")
        print(f"  With instructions: {with_instructions}")

        return len(incomplete_recipes)

    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        return -1
    finally:
        conn.close()

if __name__ == '__main__':
    deleted = cleanup_incomplete_recipes()
    sys.exit(0 if deleted >= 0 else 1)
