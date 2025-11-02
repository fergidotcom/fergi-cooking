"""
Import main folder recipes only (excluding Janet Mason folder)
"""

import os
from database import RecipeDatabase
from recipe_extractor import RecipeExtractor


def main():
    """Import recipes from main folder only"""
    print("="*60)
    print("IMPORTING MAIN FOLDER RECIPES ONLY")
    print("(Excluding Janet Mason folder)")
    print("="*60)
    print()

    # Initialize database
    print("Initializing database...")
    db = RecipeDatabase()
    db.initialize_database()
    print("✓ Database ready\n")

    extractor = RecipeExtractor()
    stats = {
        'total_files': 0,
        'processed': 0,
        'failed': 0
    }

    # Get all recipe files in main directory (excluding subdirectories)
    recipe_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file):  # Only files, not directories
            if any(file.lower().endswith(ext) for ext in extractor.supported_formats):
                if not file.startswith('.'):  # Skip hidden files
                    recipe_files.append(file)

    stats['total_files'] = len(recipe_files)
    print(f"Found {len(recipe_files)} recipe files in main folder\n")

    # Process each file
    for file_path in sorted(recipe_files):
        try:
            print(f"Processing: {file_path}")
            recipe_data = extractor.extract_from_file(file_path)
            recipe_id = db.add_recipe(recipe_data)
            print(f"  ✓ Added as recipe #{recipe_id}: {recipe_data['title']}")
            stats['processed'] += 1
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            stats['failed'] += 1

    # Print summary
    print(f"\n{'='*60}")
    print("IMPORT COMPLETE")
    print(f"{'='*60}")
    print(f"Total files found:     {stats['total_files']}")
    print(f"Successfully imported: {stats['processed']}")
    print(f"Failed:                {stats['failed']}")
    print(f"{'='*60}\n")

    # Get database statistics
    db_stats = db.get_statistics()
    print("Database Statistics:")
    print(f"Total recipes: {db_stats['total_recipes']}")

    if db_stats['by_source']:
        print("\nRecipes by Source:")
        for source in db_stats['by_source']:
            print(f"  {source['source_attribution']}: {source['count']}")

    if db_stats['by_cuisine']:
        print("\nRecipes by Cuisine:")
        for cuisine in db_stats['by_cuisine']:
            print(f"  {cuisine['cuisine_type']}: {cuisine['count']}")

    print()


if __name__ == "__main__":
    main()
