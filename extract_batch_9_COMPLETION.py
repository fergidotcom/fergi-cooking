"""
FINAL BATCH - Complete Janet Mason Cookbook Extraction!
Images 8191-8195 (The Last 5!)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8191_1.JPG': {
        'title': 'Cheesey Potatoe Casserole',
        'description': 'Rich and creamy potato casserole with cheese. Comfort food classic.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 60,
        'calories_per_serving': 340,
        'ingredients': [
            {'quantity': '2', 'unit': 'pounds', 'name': 'frozen cubed potatoes', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': 'cream of celery soup', 'preparation': None},
            {'quantity': '1/2', 'unit': 'pound', 'name': 'grated cheddar cheese', 'preparation': None},
            {'quantity': '4', 'unit': 'cups', 'name': 'crushed cornflakes', 'preparation': None},
        ],
        'instructions': [
            'Mix together all ingredients except cornflakes and top with cornflakes.',
            'Preheat oven to 350. Mix together all ingredients except cornflakes.',
            'Bake for 1 hour or until top is crunchy.',
        ]
    },

    'IMG_8191_2.JPG': {
        'title': 'Chili Rice with Thai Bowl',
        'description': 'Handwritten recipe for Thai-inspired chili rice dish from Willow Simmons.',
        'servings': '4',
        'prep_time_minutes': 15,
        'cook_time_minutes': 25,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'rice', 'preparation': None},
            {'quantity': '3', 'unit': None, 'name': 'dill onions', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': 'cups', 'name': 'chicken broth', 'preparation': 'fresh Thai basil'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'fresh Thai basil', 'preparation': None},
        ],
        'instructions': [
            'Ingredients and instructions from handwritten Kitchen of Willow Simmons card.',
            'Sauté rice with Thai bowl.',
            'Add broth and cook.',
            'Simmer until done.',
        ]
    },

    'IMG_8192_1.JPG': {
        'title': 'Rice',
        'description': 'Simple rice cooking instructions. Perfect side dish.',
        'servings': '6',
        'prep_time_minutes': 5,
        'cook_time_minutes': 20,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'rice', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'oil', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'water', 'preparation': None},
            {'quantity': '1', 'unit': 'small', 'name': 'can tomato sauce', 'preparation': None},
        ],
        'instructions': [
            'Turn on the stove and put in just enough oil to cover the bottom of the pan. Put rice in and let it brown while stirring. Once it is done so the rice in a colander. Once rice is brown add water.',
            'Boullion, and tomato sauce. The rice gets big (rice fills with water) then turn it down to low and put the top on and wait twenty minutes. Never take off burner but keep the lid on until ready to serve.',
        ]
    },

    'IMG_8192_2.JPG': {
        'title': 'Baked Chili Rellenos',
        'description': 'Easy baked version of chili rellenos. Cheese-filled peppers.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 30,
        'calories_per_serving': 320,
        'ingredients': [
            {'quantity': '7', 'unit': 'ounces', 'name': 'green chile', 'preparation': None},
            {'quantity': '1', 'unit': 'pound', 'name': 'cheddar cheese', 'preparation': 'grated'},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'milk', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'In a casserole left, alternate layers of chiles and cheese. Beat eggs, milk, flour, and salt together.',
            'Pour over chili-cheese layers. Bake 325 about 30 minutes. Good with BBQ meat or mexican food. May be prepared in advance',
        ]
    },

    'IMG_8193_1.JPG': {
        'title': 'Scalloped Potatoes',
        'description': 'Classic scalloped potatoes with creamy sauce.',
        'servings': '8',
        'prep_time_minutes': 25,
        'cook_time_minutes': 90,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '8', 'unit': None, 'name': 'large potato, not peeled', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'large onion, diced', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'can cheddar cheese soup', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'can celery soup', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'milk', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'cups cheddar cheese', 'preparation': None},
            {'quantity': '1/2', 'unit': None, 'name': 'teaspoon pepper', 'preparation': None},
        ],
        'instructions': [
            'Blend together 2 cans of soup and milk and pepper. Put some butter in the bottom of a large Pan dish and sauté onions in the pan then put a layer of potatoes then pour 1/2 of the soup then add up with more onions and a layer of cheese and top with the rest of the soup then bacon then bake for 1 hour at 350 and the last 15 minutes add cheese to the top. Check potatoes for doneness by putting a knife in one.',
        ]
    },

    'IMG_8193_2.JPG': {
        'title': 'Three Colored Pasta',
        'description': 'Colorful pasta dish. Italian Restaurant Style Dressing.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 15,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '1', 'unit': 'bag', 'name': 'three colored pasta, cooked and drained', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'carrots, shredded', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'broccoli, chopped', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'zucchini, sliced', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'cherry tomatoes, halved', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'package four cheese, crumbled', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'can olives, sliced', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'bottle Bernstein Italian Restaurant Style Dressing', 'preparation': None},
        ],
        'instructions': [
            'Toss all ingredients and refrigerate at least 2 hours before serving.',
        ]
    },

    'IMG_8194_1.JPG': {
        'title': 'Creamed Spinach',
        'description': 'Rich and creamy spinach side dish.',
        'servings': '4',
        'prep_time_minutes': 15,
        'cook_time_minutes': 20,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'milk', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'unsalted butter', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'freshly ground nutmeg', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoon', 'name': 'flour', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'freshly ground nutmeg', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': '(10-ounce packages) frozen chopped spinach, thaw and drain', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'sour cream', 'preparation': None},
            {'quantity': '1', 'unit': 'cups', 'name': 'pepper', 'preparation': None},
        ],
        'instructions': [
            'Heat milk to simmer in a small pan over low heat. In a medium pan melt butter over low heat. Stir in sugar and cook until stirring.',
            'It is blended. About 3-5 minutes stirring, add the heated milk and gradually in.',
            'All boil. Continue to cook about 5 minutes. Stir in the nutmeg, garlic and salt to taste. Put in a shallow casserole and top with cheese.',
            'Add spinach. Simmer about 5 minutes stirring.',
            'Pepper to taste. Put in a shallow casserole and top with cheese. Before the cheese in can be made several days in advanced. Top with cheese before baking. May be made several days in advance.',
            'And broil until browned. The creamed spinach can be made several days in advanced. Top with cheese before.',
        ]
    },

    'IMG_8194_2.JPG': {
        'title': 'Mashed Potatoes',
        'description': 'Creamy mashed potatoes. Classic comfort food.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 30,
        'calories_per_serving': 240,
        'ingredients': [
            {'quantity': '5', 'unit': 'pounds', 'name': 'potatoes', 'preparation': 'peeled'},
            {'quantity': '6', 'unit': 'ounces', 'name': 'cream cheese', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sour cream', 'preparation': None},
            {'quantity': '2', 'unit': 'teaspoon', 'name': 'onion salt', 'preparation': None},
        ],
        'instructions': [
            'Peel, potato ingredients/add ingredients and toss with hands. Fold in sour cream and taste. Bake 350 for 30 minutes. These.',
            'Potatoes can be made ahead of time but do not freeze.',
        ]
    },

    'IMG_8195.JPG': {
        'title': 'Potatoes Romanoff',
        'description': 'Gourmet potato casserole with sour cream and cheese.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 320,
        'ingredients': [
            {'quantity': '1', 'unit': 'bag', 'name': 'frozen shredded hash brown potatoes', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'MINCED shallots', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'GRATED white cheddar cheese', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'cups', 'name': 'sour cream', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'GROUND pepper', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'GRATED parmesan cheese', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven 425. Mix together all and pepper and toss with shallots.',
            'Bake until potatoes are hot and cheese is golden.',
            'Cream in 2 additions. Transfer into casserole. Sprinkle remaining cheese on top. Bake until potatoes are hot and cheese is golden brown about 30-45 minutes.',
        ]
    },
}

def main():
    print("=" * 60)
    print("🎉 FINAL BATCH - COMPLETING JANET MASON EXTRACTION! 🎉")
    print("Images: IMG_8191 through IMG_8195 (THE LAST 5!)")
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

    total_extracted = 80 + success_count

    print("=" * 60)
    print(f"FINAL BATCH COMPLETE!")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print()
    print(f"  📊 TOTAL EXTRACTED: {total_extracted} out of 85 recipes")
    print(f"  📈 FINAL PROGRESS: {total_extracted/85*100:.1f}%")
    print()

    if total_extracted >= 85:
        print("  🎉🎉🎉 EXTRACTION COMPLETE! ALL 85 RECIPES SAVED! 🎉🎉🎉")
        print()
        print("  Janet Mason's entire cookbook is now preserved in your database!")
    else:
        remaining = 85 - total_extracted
        print(f"  ⏳ Remaining: {remaining} recipes")

    print("=" * 60)

if __name__ == "__main__":
    main()
