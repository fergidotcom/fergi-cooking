"""
Batch import script - processes all recipe files and populates database
"""

import os
from pathlib import Path
from typing import List
from database import RecipeDatabase
from recipe_extractor import RecipeExtractor


class RecipeImporter:
    """Batch import recipes from file system"""

    def __init__(self, db_path: str = "recipes.db"):
        self.db = RecipeDatabase(db_path)
        self.extractor = RecipeExtractor()
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'failed': 0,
            'skipped': 0
        }

    def scan_directory(self, directory: str, recursive: bool = True) -> List[str]:
        """Scan directory for recipe files"""
        recipe_files = []

        if recursive:
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in self.extractor.supported_formats):
                        # Skip system files
                        if not file.startswith('.'):
                            recipe_files.append(os.path.join(root, file))
        else:
            for file in os.listdir(directory):
                if any(file.lower().endswith(ext) for ext in self.extractor.supported_formats):
                    if not file.startswith('.'):
                        recipe_files.append(os.path.join(directory, file))

        return recipe_files

    def import_file(self, file_path: str, override_source: str = None) -> bool:
        """Import a single recipe file"""
        try:
            print(f"Processing: {Path(file_path).name}")

            # Extract recipe data
            recipe_data = self.extractor.extract_from_file(file_path)

            # Override source if specified (e.g., for Janet Mason folder)
            if override_source:
                recipe_data['source_attribution'] = override_source

            # Add to database
            recipe_id = self.db.add_recipe(recipe_data)

            print(f"  ✓ Added as recipe #{recipe_id}: {recipe_data['title']}")
            self.stats['processed'] += 1
            return True

        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            self.stats['failed'] += 1
            return False

    def import_directory(self, directory: str, override_source: str = None):
        """Import all recipes from a directory"""
        print(f"\n{'='*60}")
        print(f"Scanning directory: {directory}")
        if override_source:
            print(f"Attribution: {override_source}")
        print(f"{'='*60}\n")

        recipe_files = self.scan_directory(directory, recursive=False)
        self.stats['total_files'] += len(recipe_files)

        print(f"Found {len(recipe_files)} recipe files\n")

        for file_path in recipe_files:
            self.import_file(file_path, override_source)

    def import_all(self, base_directory: str = "."):
        """Import all recipes from base directory and subdirectories"""
        # Initialize database
        print("Initializing database...")
        self.db.initialize_database()
        print("✓ Database ready\n")

        # Import from main directory
        self.import_directory(base_directory)

        # Import from Janet Mason subdirectory
        janet_mason_dir = os.path.join(base_directory, "Janet Mason")
        if os.path.exists(janet_mason_dir):
            self.import_directory(janet_mason_dir, override_source="Janet")

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print import statistics"""
        print(f"\n{'='*60}")
        print("IMPORT COMPLETE")
        print(f"{'='*60}")
        print(f"Total files found:    {self.stats['total_files']}")
        print(f"Successfully imported: {self.stats['processed']}")
        print(f"Failed:               {self.stats['failed']}")
        print(f"Skipped:              {self.stats['skipped']}")
        print(f"{'='*60}\n")

        # Get database statistics
        db_stats = self.db.get_statistics()
        print("Database Statistics:")
        print(f"Total recipes: {db_stats['total_recipes']}")
        print(f"Favorites: {db_stats['favorites']}")

        if db_stats['by_source']:
            print("\nRecipes by Source:")
            for source in db_stats['by_source']:
                print(f"  {source['source_attribution']}: {source['count']}")

        if db_stats['by_cuisine']:
            print("\nRecipes by Cuisine:")
            for cuisine in db_stats['by_cuisine']:
                print(f"  {cuisine['cuisine_type']}: {cuisine['count']}")

        print()


def main():
    """Main import function"""
    import argparse

    parser = argparse.ArgumentParser(description='Import recipes into database')
    parser.add_argument('--directory', '-d', default='.',
                       help='Base directory to scan (default: current directory)')
    parser.add_argument('--file', '-f',
                       help='Import single file')
    parser.add_argument('--source', '-s',
                       help='Override source attribution')
    parser.add_argument('--db', default='recipes.db',
                       help='Database file path (default: recipes.db)')

    args = parser.parse_args()

    importer = RecipeImporter(args.db)

    if args.file:
        # Import single file
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            return

        print(f"Importing single file: {args.file}")
        importer.db.initialize_database()
        success = importer.import_file(args.file, args.source)

        if success:
            print("\n✓ Import successful!")
        else:
            print("\n✗ Import failed!")

    else:
        # Import all from directory
        if not os.path.exists(args.directory):
            print(f"Error: Directory not found: {args.directory}")
            return

        importer.import_all(args.directory)


if __name__ == "__main__":
    main()
