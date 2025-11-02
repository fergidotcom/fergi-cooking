"""
Extract batch 3 of Janet Mason recipes (images 8124-8128)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8124_1.JPG': {
        'title': 'Asparagus Sauce',
        'description': 'Simple sauce for steaming asparagus with butter and balsamic vinegar.',
        'servings': '4',
        'prep_time_minutes': 5,
        'cook_time_minutes': 10,
        'calories_per_serving': 80,
        'ingredients': [
            {'quantity': '2', 'unit': 'pounds', 'name': 'asparagus', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'butter', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'tablespoons', 'name': 'balsamic vinegar', 'preparation': None},
            {'quantity': '3/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
        ],
        'instructions': [
            'Steam asparagus while steaming melt butter and balsamic.',
            'While steaming and cook asparagus add salt and pepper to taste and pour over steamed asparagus and serve.',
        ]
    },

    'IMG_8124_2.JPG': {
        'title': 'Vegetable Custard Casserole',
        'description': 'Creamy baked vegetable casserole with corn, zucchini, and cheese.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '6', 'unit': 'slices', 'name': 'firm white bread', 'preparation': None},
            {'quantity': '4', 'unit': 'cups', 'name': 'jack cheese', 'preparation': 'finely shredded'},
            {'quantity': '2', 'unit': 'cups', 'name': 'milk', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'zucchini', 'preparation': 'sliced'},
            {'quantity': '1', 'unit': 'can', 'name': 'whole kernel corn', 'preparation': 'drained'},
            {'quantity': '2', 'unit': 'cups', 'name': 'sliced zucchini', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
        ],
        'instructions': [
            'Trim off crust. Spread butter evenly on bread and arrange butter side down in a 9x13 pan.',
            'Distribute the corn in even layer over bread.',
            'Shed over bread and top with cheese and zucchini.',
            'Beat eggs slightly, then add milk, salt, and pepper. Pour over cheese.',
            'Bake uncovered 45 for 30-40 minutes or until lightly browned and set up.',
            'Before serving.',
        ]
    },

    'IMG_8125_1.JPG': {
        'title': 'Genoese Pesto',
        'description': 'Traditional Italian basil pesto sauce. Perfect for pasta, bread, and more.',
        'servings': '6',
        'prep_time_minutes': 15,
        'cook_time_minutes': 0,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1/2', 'unit': None, 'name': 'small bunches basil', 'preparation': None},
            {'quantity': '4', 'unit': None, 'name': 'cloves garlic', 'preparation': None},
            {'quantity': '2 1/3', 'unit': 'cup', 'name': 'pine nuts', 'preparation': None},
            {'quantity': '1 1/3', 'unit': 'cup', 'name': 'chopped walnuts', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'ounce grated Pecorino cheese', 'preparation': 'grated'},
            {'quantity': '1', 'unit': None, 'name': 'tablespoons olive oil', 'preparation': None},
            {'quantity': '2', 'unit': 'ounces', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'Wash basil and dry. Put salt.',
            'Together. Add cheese and oil.',
            'Together in a blender or mixer.',
            'Green. Put one tablespoon of boiling pasta water per person into a large bowl.',
            'Boiling pasta water. Stir and blend to make it smooth.',
        ]
    },

    'IMG_8125_2.JPG': {
        'title': 'Shrimp Cocktail Sauce',
        'description': 'Classic tangy cocktail sauce for shrimp and seafood.',
        'servings': '6',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 40,
        'ingredients': [
            {'quantity': '3/4', 'unit': None, 'name': 'cup ketchup', 'preparation': None},
            {'quantity': '1/4', 'unit': None, 'name': 'chili sauce', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'horseradish', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'cayenne pepper', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'lemon juice', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'worcestershire sauce', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'teaspoon hot chili sauce', 'preparation': None},
            {'quantity': '1/4', 'unit': None, 'name': 'cup water', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'cup flat beer', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'Combine first 6 items and chill. Bring water and beer to a boil, then add shrimp and cook until pink 2-3 min.',
            'Drain and chill.',
        ]
    },

    'IMG_8126_1.JPG': {
        'title': 'Parmesan Balsamic Vinaigrette',
        'description': 'Light vinaigrette dressing with fresh basil and parmesan.',
        'servings': '6',
        'prep_time_minutes': 10,
        'cook_time_minutes': 0,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'fresh minced basil', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'finely grated parmesan cheese', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'fresh lemon juice', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'olive oil', 'preparation': None},
        ],
        'instructions': [
            'Mince garlic and mash to a paste with vinegar, lemon juice, basil, parmesan and oil.',
            'Together with vinegar, lemon juice, basil, parmesan and oil in a slow stream, whisking until well blended.',
        ]
    },

    'IMG_8126_2.JPG': {
        'title': 'Lemon-Garlic Vinaigrette',
        'description': 'Fresh and zesty vinaigrette with lemon, garlic, and herbs.',
        'servings': '6',
        'prep_time_minutes': 10,
        'cook_time_minutes': 0,
        'calories_per_serving': 140,
        'ingredients': [
            {'quantity': '2', 'unit': None, 'name': 'cloves garlic', 'preparation': 'crushed and peeled'},
            {'quantity': 'Zest 1', 'unit': None, 'name': 'large lemon', 'preparation': 'in large pieces'},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'kosher salt', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'dijon mustard', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'lemon juice', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'champagne vinegar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'canola oil', 'preparation': 'or a light oil'},
        ],
        'instructions': [
            'Using a mortar and pestle, grind or crush garlic, lemon zest and salt to a fine paste.',
            'Combine lemon juice, vinegar, water.',
            'Add to the garlic paste and then whisk in oil slowly. Add pepper to taste.',
        ]
    },

    'IMG_8127_1.JPG': {
        'title': 'Salad Parmesan',
        'description': 'Simple parmesan cheese salad dressing.',
        'servings': '4',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 100,
        'ingredients': [
            {'quantity': '4', 'unit': None, 'name': 'cloves garlic', 'preparation': 'pressed'},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'parmesan cheese', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'dijon mustard', 'preparation': None},
            {'quantity': '4', 'unit': 'tablespoons', 'name': 'lemon juice', 'preparation': None},
        ],
        'instructions': [
            'Blend in blender and chill.',
        ]
    },

    'IMG_8127_2.JPG': {
        'title': 'Blue Cheese Vinegar Dressing',
        'description': 'Tangy blue cheese dressing with vinegar base.',
        'servings': '6',
        'prep_time_minutes': 10,
        'cook_time_minutes': 0,
        'calories_per_serving': 140,
        'ingredients': [
            {'quantity': '2 1/2', 'unit': 'ounces', 'name': 'blue cheese', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'dry mustard', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'salad supreme', 'preparation': 'scallions'},
            {'quantity': '2', 'unit': 'cups', 'name': 'oil', 'preparation': None},
        ],
        'instructions': [
            'Mix well and toss on salad.',
        ]
    },

    'IMG_8128_1.JPG': {
        'title': 'Honey Mustard Dressing',
        'description': 'Sweet and tangy honey mustard dressing.',
        'servings': '6',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cup', 'name': 'grapefruit juice', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'dijon style mustard', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'honey', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'dijon style mustard', 'preparation': None},
        ],
        'instructions': [
            'In a small bowl, whisk grapefruit juice and oil and honey, mustard and garlic until blended. Stir in a small bowl.',
            'Cover and chill. Serve on salad greens, fruit or sliced avocados.',
        ]
    },

    'IMG_8128_2.JPG': {
        'title': 'Easy Caesar Salad Dressing',
        'description': 'Quick and easy Caesar dressing for salads.',
        'servings': '6',
        'prep_time_minutes': 10,
        'cook_time_minutes': 0,
        'calories_per_serving': 150,
        'ingredients': [
            {'quantity': '1', 'unit': None, 'name': 'bottle regular grade caesar dressing', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'large head romaine', 'preparation': None},
        ],
        'instructions': [
            'Pour dressing in a bowl. Add fresh pressed garlic.',
            'Stir grating until thick. Use as much cheese to get the consistency you want. Chill.',
            'Over fresh grating and toss romaine lettuce and garnish with croutons.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 3 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8124 through IMG_8128")
    print("=" * 60)
    print()

    success_count = 0
    error_count = 0

    for filename, recipe_data in RECIPES.items():
        print(f"Processing: {filename}")
        print(f"  Title: {recipe_data['title']}")

        try:
            recipe_id = insert_recipe(filename, recipe_data)
            print(f"  ✅ Inserted as recipe #{recipe_id}")
            success_count += 1

        except Exception as e:
            print(f"  ❌ Error: {e}")
            mark_error(filename, str(e))
            error_count += 1

        print()

    print("=" * 60)
    print(f"BATCH 3 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {21 + success_count} recipes")
    print(f"  📈 Progress: {(21 + success_count)/85*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
