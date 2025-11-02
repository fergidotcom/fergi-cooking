"""
Batch extraction script for Janet Mason cookbook images
Processes images and tracks progress
"""

import sqlite3
import json
from pathlib import Path

# Progress tracking file
PROGRESS_FILE = "janet_extraction_progress.json"

def load_progress():
    """Load extraction progress"""
    if Path(PROGRESS_FILE).exists():
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {
        'completed': [],
        'skipped': [],
        'errors': [],
        'total_processed': 0
    }

def save_progress(progress):
    """Save extraction progress"""
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def get_pending_images():
    """Get list of images that still need processing"""
    janet_dir = Path("Janet Mason")
    all_images = sorted([f.name for f in janet_dir.glob("*.JPG")])

    progress = load_progress()
    processed = set(progress['completed'] + progress['skipped'] + progress['errors'])

    pending = [img for img in all_images if img not in processed]
    return pending

def check_if_recipe_exists(filename, db_path='recipes.db'):
    """Check if recipe already exists in database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM recipes WHERE original_filename = ?', (filename,))
    result = cursor.fetchone()
    conn.close()
    return result

def insert_recipe(filename, recipe_data, db_path='recipes.db'):
    """Insert a new recipe into the database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        file_path = f"Janet Mason/{filename}"

        # Insert recipe
        cursor.execute('''
            INSERT INTO recipes (
                title, description, servings, prep_time_minutes, cook_time_minutes,
                calories_per_serving, source_attribution, original_filename, file_path
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            recipe_data['title'],
            recipe_data.get('description', ''),
            recipe_data.get('servings', ''),
            recipe_data.get('prep_time_minutes'),
            recipe_data.get('cook_time_minutes'),
            recipe_data.get('calories_per_serving'),
            'Janet Mason Cookbook',
            filename,
            file_path
        ))

        recipe_id = cursor.lastrowid

        # Insert ingredients
        for idx, ingredient in enumerate(recipe_data.get('ingredients', []), 1):
            cursor.execute('''
                INSERT INTO ingredients (recipe_id, quantity, unit, ingredient_name, preparation, ingredient_order)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                recipe_id,
                ingredient.get('quantity'),
                ingredient.get('unit'),
                ingredient.get('name'),
                ingredient.get('preparation'),
                idx
            ))

        # Insert instructions
        for idx, instruction in enumerate(recipe_data.get('instructions', []), 1):
            cursor.execute('''
                INSERT INTO instructions (recipe_id, step_number, instruction_text)
                VALUES (?, ?, ?)
            ''', (recipe_id, idx, instruction))

        conn.commit()
        return recipe_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def mark_completed(filename):
    """Mark a file as completed"""
    progress = load_progress()
    if filename not in progress['completed']:
        progress['completed'].append(filename)
        progress['total_processed'] = len(progress['completed'])
        save_progress(progress)

def mark_skipped(filename, reason=""):
    """Mark a file as skipped"""
    progress = load_progress()
    if filename not in progress['skipped']:
        progress['skipped'].append(filename)
        save_progress(progress)

def mark_error(filename, error):
    """Mark a file as error"""
    progress = load_progress()
    progress['errors'].append({'filename': filename, 'error': str(error)})
    save_progress(progress)

def show_progress():
    """Display current progress"""
    progress = load_progress()
    pending = get_pending_images()

    print("=" * 60)
    print("JANET MASON COOKBOOK EXTRACTION PROGRESS")
    print("=" * 60)
    print(f"✅ Completed: {len(progress['completed'])}")
    print(f"⏭️  Skipped: {len(progress['skipped'])}")
    print(f"❌ Errors: {len(progress['errors'])}")
    print(f"⏳ Pending: {len(pending)}")
    print(f"📊 Total Images: 85")
    print(f"📈 Progress: {len(progress['completed'])/85*100:.1f}%")
    print("=" * 60)

    if pending:
        print(f"\nNext to process: {pending[0]}")
    else:
        print("\n🎉 All images processed!")

if __name__ == "__main__":
    show_progress()
