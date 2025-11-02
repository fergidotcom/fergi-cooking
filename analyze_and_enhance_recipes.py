#!/usr/bin/env python3
"""
Analyze and enhance all main recipes with:
1. Elegant descriptions
2. Prep/cook times, servings, calorie estimates
3. Enhanced instructions with inline ingredient quantities
"""

import sqlite3
import json
from pathlib import Path

def get_main_recipes():
    """Get all non-Janet recipes"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, description, source_attribution,
               prep_time_minutes, cook_time_minutes, servings
        FROM recipes
        WHERE source_attribution != 'Janet' OR source_attribution IS NULL
        ORDER BY title
    """)

    recipes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return recipes

def get_recipe_details(recipe_id):
    """Get full recipe details including ingredients and instructions"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get recipe
    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = dict(cursor.fetchone())

    # Get ingredients
    cursor.execute("""
        SELECT quantity, unit, ingredient_name, preparation
        FROM ingredients
        WHERE recipe_id = ?
        ORDER BY id
    """, (recipe_id,))
    recipe['ingredients'] = [dict(row) for row in cursor.fetchall()]

    # Get instructions
    cursor.execute("""
        SELECT step_number, instruction_text
        FROM instructions
        WHERE recipe_id = ?
        ORDER BY step_number
    """, (recipe_id,))
    recipe['instructions'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return recipe

if __name__ == '__main__':
    recipes = get_main_recipes()
    print(f"Found {len(recipes)} main recipes")
    print("\nRecipes:")
    for r in recipes:
        print(f"  {r['id']:3d}. {r['title']}")
