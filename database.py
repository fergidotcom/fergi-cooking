"""
Database management module for recipe database
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import json


class RecipeDatabase:
    """Handles all database operations for recipes"""

    def __init__(self, db_path: str = "recipes.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """Connect to the database"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        self.cursor = self.conn.cursor()

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

    def initialize_database(self, schema_file: str = "schema.sql"):
        """Initialize database with schema"""
        self.connect()
        with open(schema_file, 'r') as f:
            schema = f.read()
        self.cursor.executescript(schema)
        self.conn.commit()
        print(f"Database initialized: {self.db_path}")
        self.disconnect()

    def add_recipe(self, recipe_data: Dict) -> int:
        """Add a new recipe to database"""
        self.connect()

        # Insert main recipe
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO recipes (
                title, description, prep_time_minutes, cook_time_minutes,
                total_time_minutes, servings, difficulty, cuisine_type,
                meal_type, source_attribution, source_url, original_filename,
                file_path, notes, rating, favorite, vegetarian, vegan,
                gluten_free, dairy_free
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            recipe_data.get('title'),
            recipe_data.get('description'),
            recipe_data.get('prep_time_minutes'),
            recipe_data.get('cook_time_minutes'),
            recipe_data.get('total_time_minutes'),
            recipe_data.get('servings'),
            recipe_data.get('difficulty', 'Unknown'),
            recipe_data.get('cuisine_type'),
            recipe_data.get('meal_type'),
            recipe_data.get('source_attribution'),
            recipe_data.get('source_url'),
            recipe_data.get('original_filename'),
            recipe_data.get('file_path'),
            recipe_data.get('notes'),
            recipe_data.get('rating'),
            recipe_data.get('favorite', 0),
            recipe_data.get('vegetarian', 0),
            recipe_data.get('vegan', 0),
            recipe_data.get('gluten_free', 0),
            recipe_data.get('dairy_free', 0)
        ))

        recipe_id = cursor.lastrowid

        # Insert ingredients
        if 'ingredients' in recipe_data:
            for idx, ingredient in enumerate(recipe_data['ingredients']):
                cursor.execute("""
                    INSERT INTO ingredients (
                        recipe_id, ingredient_order, quantity, unit,
                        ingredient_name, preparation, ingredient_group
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    recipe_id,
                    idx + 1,
                    ingredient.get('quantity'),
                    ingredient.get('unit'),
                    ingredient.get('name'),
                    ingredient.get('preparation'),
                    ingredient.get('group')
                ))

        # Insert instructions
        if 'instructions' in recipe_data:
            for idx, instruction in enumerate(recipe_data['instructions']):
                if isinstance(instruction, str):
                    instruction_text = instruction
                    instruction_group = None
                else:
                    instruction_text = instruction.get('text', instruction.get('instruction', ''))
                    instruction_group = instruction.get('group')

                cursor.execute("""
                    INSERT INTO instructions (
                        recipe_id, step_number, instruction_text, instruction_group
                    ) VALUES (?, ?, ?, ?)
                """, (recipe_id, idx + 1, instruction_text, instruction_group))

        # Insert tags
        if 'tags' in recipe_data:
            for tag_name in recipe_data['tags']:
                # Insert tag if it doesn't exist
                cursor.execute(
                    "INSERT OR IGNORE INTO tags (tag_name) VALUES (?)",
                    (tag_name,)
                )
                # Get tag id
                cursor.execute("SELECT id FROM tags WHERE tag_name = ?", (tag_name,))
                tag_id = cursor.fetchone()[0]
                # Link recipe to tag
                cursor.execute(
                    "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                    (recipe_id, tag_id)
                )

        # Insert images
        if 'images' in recipe_data:
            for idx, image_path in enumerate(recipe_data['images']):
                cursor.execute("""
                    INSERT INTO recipe_images (
                        recipe_id, image_path, image_type, display_order
                    ) VALUES (?, ?, ?, ?)
                """, (recipe_id, image_path, 'original', idx))

        self.conn.commit()
        self.disconnect()

        return recipe_id

    def get_recipe(self, recipe_id: int) -> Optional[Dict]:
        """Get complete recipe by ID"""
        self.connect()

        # Get main recipe data
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe_row = self.cursor.fetchone()

        if not recipe_row:
            self.disconnect()
            return None

        recipe = dict(recipe_row)

        # Get ingredients
        self.cursor.execute("""
            SELECT * FROM ingredients
            WHERE recipe_id = ?
            ORDER BY ingredient_order
        """, (recipe_id,))
        recipe['ingredients'] = [dict(row) for row in self.cursor.fetchall()]

        # Get instructions
        self.cursor.execute("""
            SELECT * FROM instructions
            WHERE recipe_id = ?
            ORDER BY step_number
        """, (recipe_id,))
        recipe['instructions'] = [dict(row) for row in self.cursor.fetchall()]

        # Get tags
        self.cursor.execute("""
            SELECT t.tag_name FROM tags t
            JOIN recipe_tags rt ON t.id = rt.tag_id
            WHERE rt.recipe_id = ?
        """, (recipe_id,))
        recipe['tags'] = [row['tag_name'] for row in self.cursor.fetchall()]

        # Get images
        self.cursor.execute("""
            SELECT * FROM recipe_images
            WHERE recipe_id = ?
            ORDER BY display_order
        """, (recipe_id,))
        recipe['images'] = [dict(row) for row in self.cursor.fetchall()]

        self.disconnect()
        return recipe

    def get_all_recipes(self, limit: Optional[int] = None, offset: int = 0) -> List[Dict]:
        """Get all recipes (summary view)"""
        self.connect()

        query = """
            SELECT id, title, description, cuisine_type, meal_type,
                   source_attribution, rating, favorite, prep_time_minutes,
                   cook_time_minutes, date_added, date_modified
            FROM recipes
            ORDER BY date_modified DESC
        """

        if limit:
            query += f" LIMIT {limit} OFFSET {offset}"

        self.cursor.execute(query)
        recipes = [dict(row) for row in self.cursor.fetchall()]

        self.disconnect()
        return recipes

    def search_recipes(self, search_term: str) -> List[Dict]:
        """Search recipes by title, description, ingredients"""
        self.connect()

        search_pattern = f"%{search_term}%"

        self.cursor.execute("""
            SELECT DISTINCT r.id, r.title, r.description, r.cuisine_type,
                   r.source_attribution, r.rating, r.favorite
            FROM recipes r
            LEFT JOIN ingredients i ON r.id = i.recipe_id
            LEFT JOIN instructions inst ON r.id = inst.recipe_id
            WHERE r.title LIKE ?
               OR r.description LIKE ?
               OR i.ingredient_name LIKE ?
               OR inst.instruction_text LIKE ?
            ORDER BY r.title
        """, (search_pattern, search_pattern, search_pattern, search_pattern))

        recipes = [dict(row) for row in self.cursor.fetchall()]

        self.disconnect()
        return recipes

    def update_recipe(self, recipe_id: int, recipe_data: Dict) -> bool:
        """Update existing recipe"""
        self.connect()
        cursor = self.conn.cursor()

        # Update main recipe data
        update_fields = []
        update_values = []

        for field in ['title', 'description', 'prep_time_minutes', 'cook_time_minutes',
                     'total_time_minutes', 'servings', 'difficulty', 'cuisine_type',
                     'meal_type', 'source_attribution', 'source_url', 'notes',
                     'rating', 'favorite', 'vegetarian', 'vegan', 'gluten_free', 'dairy_free']:
            if field in recipe_data:
                update_fields.append(f"{field} = ?")
                update_values.append(recipe_data[field])

        if update_fields:
            update_values.append(recipe_id)
            cursor.execute(f"""
                UPDATE recipes
                SET {', '.join(update_fields)}
                WHERE id = ?
            """, update_values)

        # Update ingredients if provided
        if 'ingredients' in recipe_data:
            cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            for idx, ingredient in enumerate(recipe_data['ingredients']):
                cursor.execute("""
                    INSERT INTO ingredients (
                        recipe_id, ingredient_order, quantity, unit,
                        ingredient_name, preparation, ingredient_group
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    recipe_id, idx + 1,
                    ingredient.get('quantity'),
                    ingredient.get('unit'),
                    ingredient.get('name'),
                    ingredient.get('preparation'),
                    ingredient.get('group')
                ))

        # Update instructions if provided
        if 'instructions' in recipe_data:
            cursor.execute("DELETE FROM instructions WHERE recipe_id = ?", (recipe_id,))
            for idx, instruction in enumerate(recipe_data['instructions']):
                if isinstance(instruction, str):
                    instruction_text = instruction
                    instruction_group = None
                else:
                    instruction_text = instruction.get('text', instruction.get('instruction', ''))
                    instruction_group = instruction.get('group')

                cursor.execute("""
                    INSERT INTO instructions (
                        recipe_id, step_number, instruction_text, instruction_group
                    ) VALUES (?, ?, ?, ?)
                """, (recipe_id, idx + 1, instruction_text, instruction_group))

        # Update tags if provided
        if 'tags' in recipe_data:
            cursor.execute("DELETE FROM recipe_tags WHERE recipe_id = ?", (recipe_id,))
            for tag_name in recipe_data['tags']:
                cursor.execute("INSERT OR IGNORE INTO tags (tag_name) VALUES (?)", (tag_name,))
                cursor.execute("SELECT id FROM tags WHERE tag_name = ?", (tag_name,))
                tag_id = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO recipe_tags (recipe_id, tag_id) VALUES (?, ?)",
                    (recipe_id, tag_id)
                )

        self.conn.commit()
        self.disconnect()
        return True

    def delete_recipe(self, recipe_id: int) -> bool:
        """Delete a recipe"""
        self.connect()
        self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        self.conn.commit()
        self.disconnect()
        return True

    def get_statistics(self) -> Dict:
        """Get database statistics"""
        self.connect()

        stats = {}

        # Total recipes
        self.cursor.execute("SELECT COUNT(*) as count FROM recipes")
        stats['total_recipes'] = self.cursor.fetchone()['count']

        # Recipes by source
        self.cursor.execute("""
            SELECT source_attribution, COUNT(*) as count
            FROM recipes
            GROUP BY source_attribution
            ORDER BY count DESC
        """)
        stats['by_source'] = [dict(row) for row in self.cursor.fetchall()]

        # Recipes by cuisine
        self.cursor.execute("""
            SELECT cuisine_type, COUNT(*) as count
            FROM recipes
            WHERE cuisine_type IS NOT NULL
            GROUP BY cuisine_type
            ORDER BY count DESC
        """)
        stats['by_cuisine'] = [dict(row) for row in self.cursor.fetchall()]

        # Favorite recipes
        self.cursor.execute("SELECT COUNT(*) as count FROM recipes WHERE favorite = 1")
        stats['favorites'] = self.cursor.fetchone()['count']

        self.disconnect()
        return stats


if __name__ == "__main__":
    # Initialize database
    db = RecipeDatabase()
    db.initialize_database()
    print("Database initialized successfully!")
