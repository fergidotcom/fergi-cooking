"""
Import Janet Mason recipes with special handling
These will be imported with placeholder titles that can be edited later
"""

import os
from database import RecipeDatabase
from pathlib import Path


def main():
    """Import Janet Mason recipes"""
    print("="*60)
    print("IMPORTING JANET MASON RECIPES")
    print("(Imported with placeholder titles for manual review)")
    print("="*60)
    print()

    db = RecipeDatabase()

    # Database should already be initialized
    # db.initialize_database()

    janet_dir = "Janet Mason"
    stats = {
        'total_files': 0,
        'processed': 0,
        'failed': 0
    }

    # Get all JPG files in Janet Mason directory
    janet_files = []
    for file in sorted(os.listdir(janet_dir)):
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            janet_files.append(os.path.join(janet_dir, file))

    stats['total_files'] = len(janet_files)
    print(f"Found {len(janet_files)} image files in Janet Mason folder\n")

    # Manual mapping for known recipes (from vision analysis)
    known_titles = {
        'IMG_8111.JPG': 'Baking Powder Biscuits',
        'IMG_8112.JPG': 'Mango and Roasted Corn Salsa / Walking Fondue',
        'IMG_8113.JPG': 'Spinach Artichoke Dip',
        'IMG_8114.JPG': 'Fresh Tomato Bruschetta',
        'IMG_8115.JPG': 'Chinese Spring Rolls',
        'IMG_8116.JPG': 'Cowboy Caviar / Chicken Wings',
        'IMG_8117.JPG': 'Pork Beef Loaf / Spinach Filled Mushrooms',
        'IMG_8118.JPG': 'Josephinas Bread / Cheddar Pennies',
        'IMG_8119.JPG': 'Bourbon-Glazed Shrimp / Lamb on Skewers',
        'IMG_8120.JPG': 'Party Mix',
        'IMG_8121.JPG': 'Imperial Rolls',
        'IMG_8122.JPG': 'Mojito',
        # More can be added as they're identified
    }

    # Process each file
    for file_path in janet_files:
        try:
            filename = Path(file_path).name

            # Get title from known mapping or use placeholder
            if filename in known_titles:
                title = known_titles[filename]
                needs_review = 0
            else:
                title = f"Janet's Recipe - {filename.replace('.JPG', '').replace('_', ' ')} (NEEDS TITLE)"
                needs_review = 1

            print(f"Processing: {filename}")

            recipe_data = {
                'title': title,
                'original_filename': filename,
                'file_path': file_path,
                'source_attribution': 'Janet',
                'description': f'Cookbook image from Janet Mason collection. Original file: {filename}',
                'notes': 'Review needed: Update title and extract recipe details from image' if needs_review else 'Recipe extracted from cookbook image',
                'ingredients': [],
                'instructions': [],
                'tags': ['Janet Mason', 'Cookbook', 'Needs Review'] if needs_review else ['Janet Mason', 'Cookbook'],
                'images': [file_path],
                'difficulty': 'Unknown'
            }

            recipe_id = db.add_recipe(recipe_data)
            status = "(needs review)" if needs_review else ""
            print(f"  ✓ Added as recipe #{recipe_id}: {title} {status}")
            stats['processed'] += 1

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            stats['failed'] += 1

    # Print summary
    print(f"\n{'='*60}")
    print("JANET MASON IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"Total files found:     {stats['total_files']}")
    print(f"Successfully imported: {stats['processed']}")
    print(f"Failed:                {stats['failed']}")
    print(f"{'='*60}\n")

    # Get database statistics
    db_stats = db.get_statistics()
    print("Updated Database Statistics:")
    print(f"Total recipes: {db_stats['total_recipes']}")

    print("\nRecipes by Source:")
    for source in db_stats['by_source']:
        print(f"  {source['source_attribution']}: {source['count']}")

    print("\n")
    print("NEXT STEPS:")
    print("1. Open the web interface: http://127.0.0.1:5000")
    print("2. Browse Janet's recipes (filter by source = Janet)")
    print("3. Edit each recipe to update the title from the image")
    print("4. Add ingredients and instructions as needed")
    print()


if __name__ == "__main__":
    main()
