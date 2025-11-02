"""
Extract recipes from Janet Mason image collection
Uses manual extraction based on image analysis
"""

import sqlite3
from pathlib import Path
from typing import Dict, List

# Recipe data extracted from images
EXTRACTED_RECIPES = {
    'IMG_8111.JPG': {
        'title': 'Baking Powder Biscuits',
        'description': 'Traditional Southern-style biscuits with a tender, flaky texture. Perfect for breakfast or as a side for dinner.',
        'servings': '12',
        'prep_time_minutes': 15,
        'cook_time_minutes': 12,
        'calories_per_serving': 180,
        'source_attribution': 'Janet Mason Cookbook',
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'all-purpose flour', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'baking powder', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'shortening', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'milk', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven to 450°F.',
            'Mix flour, baking powder, and salt in a bowl.',
            'Cut in shortening until mixture resembles coarse crumbs.',
            'Stir in milk until dough forms. Do not overmix.',
            'Turn dough onto a lightly floured surface and knead gently 8-10 times.',
            'Pat or roll dough to 1/2 inch thickness.',
            'Cut with biscuit cutter or glass rim dipped in flour.',
            'Place biscuits on ungreased baking sheet, touching for soft sides or apart for crispy sides.',
            'Bake 10-12 minutes until golden brown.',
            'Brush with melted butter if desired.',
        ]
    },

    'IMG_8115.JPG': {
        'title': 'Chinese Spring Rolls (Fried Paper King)',
        'description': 'Crispy fried spring rolls filled with julienned vegetables and meat. A classic Chinese appetizer from Connie Tang\'s recipe collection.',
        'servings': '24',
        'prep_time_minutes': 45,
        'cook_time_minutes': 20,
        'calories_per_serving': 120,
        'source_attribution': 'Janet Mason Cookbook - Connie Tang',
        'ingredients': [
            {'quantity': '1', 'unit': 'package', 'name': 'spring roll wrappers', 'preparation': 'Mei Onion brand'},
            {'quantity': None, 'unit': None, 'name': 'Esher Ham', 'preparation': 'julienned'},
            {'quantity': None, 'unit': None, 'name': 'carrots', 'preparation': 'julienned'},
            {'quantity': None, 'unit': None, 'name': 'pork', 'preparation': 'julienned'},
            {'quantity': None, 'unit': None, 'name': 'chicken', 'preparation': 'julienned'},
            {'quantity': None, 'unit': None, 'name': 'cabbage', 'preparation': 'julienned, Chinese shiitake mushrooms'},
            {'quantity': None, 'unit': None, 'name': 'sweet onion', 'preparation': 'julienned'},
            {'quantity': None, 'unit': None, 'name': 'ginger', 'preparation': 'fresh'},
            {'quantity': None, 'unit': None, 'name': 'red and white pepper', 'preparation': 'to taste'},
            {'quantity': None, 'unit': None, 'name': 'salt', 'preparation': 'to taste'},
            {'quantity': None, 'unit': None, 'name': 'sesame oil', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'vegetable oil', 'preparation': 'for frying'},
        ],
        'instructions': [
            'Prepare all vegetables and meats by julienning into thin strips.',
            'Cook the filling ingredients together with ginger until tender.',
            'Season with salt, red and white pepper, and sesame oil to taste.',
            'Let filling cool completely before wrapping.',
            'Place a wrapper on work surface with corner pointing toward you.',
            'Add 2-3 tablespoons of filling near the bottom corner.',
            'Fold bottom corner over filling, then fold in sides.',
            'Roll tightly toward top corner, sealing edge with water.',
            'Heat oil in wok or deep fryer to 350°F.',
            'Fry spring rolls in batches until golden brown and crispy, about 3-4 minutes.',
            'Drain on paper towels and serve hot.',
        ]
    },

    'IMG_8120_1.JPG': {
        'title': 'Party Mix by Janet',
        'description': 'A savory snack mix perfect for parties and gatherings. Combines cereals and peanuts with a buttery, seasoned coating.',
        'servings': '20',
        'prep_time_minutes': 15,
        'cook_time_minutes': 60,
        'calories_per_serving': 180,
        'source_attribution': 'Janet Mason',
        'ingredients': [
            {'quantity': None, 'unit': None, 'name': 'cereals', 'preparation': 'various kinds (Rice Chex, Wheat Chex, Cheerios)'},
            {'quantity': None, 'unit': None, 'name': 'peanuts', 'preparation': 'roasted'},
            {'quantity': None, 'unit': None, 'name': 'butter', 'preparation': 'melted'},
            {'quantity': None, 'unit': None, 'name': 'Worcestershire sauce', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'garlic powder', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'onion powder', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'salt', 'preparation': 'to taste'},
        ],
        'instructions': [
            'Mix all the cereals and peanuts in a large flat roasting pan.',
            'Mix seasoning in a small bowl and pour over cereal mixture.',
            'Stir well to coat evenly.',
            'Bake at 250°F for 1 hour, stirring often to mix all.',
            'Cool and store in airtight containers.',
        ]
    },

    'IMG_8120_2.JPG': {
        'title': 'Fried Potatoes with Ginger Dipping Sauce',
        'description': 'Crispy fried potatoes served with a flavorful ginger-based dipping sauce. A perfect appetizer or side dish.',
        'servings': '4-6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 15,
        'calories_per_serving': 220,
        'source_attribution': 'Janet Mason Cookbook',
        'ingredients': [
            {'quantity': '2', 'unit': 'lbs', 'name': 'potatoes', 'preparation': 'peeled, cut into strips or wedges'},
            {'quantity': None, 'unit': None, 'name': 'vegetable oil', 'preparation': 'for deep frying'},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'rice wine vinegar', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'soy sauce', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'fresh ginger', 'preparation': 'grated'},
            {'quantity': '2', 'unit': 'teaspoons', 'name': 'sugar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'water', 'preparation': None},
            {'quantity': '2', 'unit': 'cloves', 'name': 'garlic', 'preparation': 'minced'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'peanut oil', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'cornstarch', 'preparation': 'for thickening'},
        ],
        'instructions': [
            'Heat oil in a saucepan over medium heat.',
            'Add garlic and ginger, sauté until fragrant (about 30 seconds).',
            'Add vinegar, soy sauce, water, and sugar.',
            'Bring to a simmer and cook for 5 minutes.',
            'Mix cornstarch with a little water and add to thicken sauce.',
            'For the potatoes: Heat oil to 350°F for deep frying.',
            'Fry potato strips in batches until golden and crispy.',
            'Drain on paper towels and season with salt.',
            'Serve hot with ginger dipping sauce.',
        ]
    },
}


def update_recipe_in_database(recipe_id: int, recipe_data: Dict, db_path: str = 'recipes.db'):
    """Update an existing recipe with extracted data"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Update recipe metadata
        cursor.execute('''
            UPDATE recipes SET
                title = ?,
                description = ?,
                servings = ?,
                prep_time_minutes = ?,
                cook_time_minutes = ?,
                calories_per_serving = ?,
                source_attribution = ?
            WHERE id = ?
        ''', (
            recipe_data['title'],
            recipe_data['description'],
            recipe_data['servings'],
            recipe_data['prep_time_minutes'],
            recipe_data['cook_time_minutes'],
            recipe_data['calories_per_serving'],
            recipe_data['source_attribution'],
            recipe_id
        ))

        # Delete old ingredients and instructions
        cursor.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        cursor.execute('DELETE FROM instructions WHERE recipe_id = ?', (recipe_id,))

        # Insert new ingredients
        for idx, ingredient in enumerate(recipe_data['ingredients'], 1):
            cursor.execute('''
                INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name, preparation, ingredient_order)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                recipe_id,
                ingredient['quantity'],
                ingredient['unit'],
                ingredient['name'],
                ingredient['preparation'],
                idx
            ))

        # Insert new instructions
        for idx, instruction in enumerate(recipe_data['instructions'], 1):
            cursor.execute('''
                INSERT INTO instructions (recipe_id, step_number, instruction_text)
                VALUES (?, ?, ?)
            ''', (recipe_id, idx, instruction))

        conn.commit()
        print(f"✅ Updated recipe {recipe_id}: {recipe_data['title']}")

    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating recipe {recipe_id}: {e}")
        raise
    finally:
        conn.close()


def find_recipe_by_filename(filename: str, db_path: str = 'recipes.db') -> int:
    """Find recipe ID by original filename"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, title FROM recipes
        WHERE original_filename = ?
    ''', (filename,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    return None


def insert_new_recipe(filename: str, recipe_data: Dict, db_path: str = 'recipes.db'):
    """Insert a new recipe into the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Calculate file path
        file_path = f"Janet Mason/{filename}"

        # Insert recipe
        cursor.execute('''
            INSERT INTO recipes (
                title, description, servings, prep_time_minutes, cook_time_minutes,
                calories_per_serving, source_attribution, original_filename, file_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe_data['title'],
            recipe_data['description'],
            recipe_data['servings'],
            recipe_data['prep_time_minutes'],
            recipe_data['cook_time_minutes'],
            recipe_data['calories_per_serving'],
            recipe_data['source_attribution'],
            filename,
            file_path
        ))

        recipe_id = cursor.lastrowid

        # Insert ingredients
        for idx, ingredient in enumerate(recipe_data['ingredients'], 1):
            cursor.execute('''
                INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name, preparation, ingredient_order)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                recipe_id,
                ingredient['quantity'],
                ingredient['unit'],
                ingredient['name'],
                ingredient['preparation'],
                idx
            ))

        # Insert instructions
        for idx, instruction in enumerate(recipe_data['instructions'], 1):
            cursor.execute('''
                INSERT INTO instructions (recipe_id, step_number, instruction_text)
                VALUES (?, ?, ?)
            ''', (recipe_id, idx, instruction))

        conn.commit()
        print(f"✅ Inserted recipe {recipe_id}: {recipe_data['title']}")
        return recipe_id

    except Exception as e:
        conn.rollback()
        print(f"❌ Error inserting recipe: {e}")
        raise
    finally:
        conn.close()


def main():
    """Extract and insert recipes from Janet Mason images"""
    db_path = 'recipes.db'

    print("=" * 60)
    print("Janet Mason Image Recipe Extraction")
    print("=" * 60)
    print()

    inserted_count = 0
    updated_count = 0
    error_count = 0

    for filename, recipe_data in EXTRACTED_RECIPES.items():
        print(f"Processing: {filename}")
        print(f"  Title: {recipe_data['title']}")

        try:
            # Check if recipe already exists
            recipe_id = find_recipe_by_filename(filename, db_path)

            if recipe_id:
                print(f"  Found existing recipe ID: {recipe_id}")
                update_recipe_in_database(recipe_id, recipe_data, db_path)
                updated_count += 1
            else:
                print(f"  Creating new recipe...")
                insert_new_recipe(filename, recipe_data, db_path)
                inserted_count += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")
            error_count += 1

        print()

    print("=" * 60)
    print(f"Extraction Complete!")
    print(f"  ✅ Inserted: {inserted_count}")
    print(f"  ✅ Updated: {updated_count}")
    if error_count > 0:
        print(f"  ❌ Errors: {error_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
