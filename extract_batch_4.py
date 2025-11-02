"""
Extract batch 4 of Janet Mason recipes (images 8129-8133)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8129_1.JPG': {
        'title': 'Cabernet Peppercorn Sauce',
        'description': 'Rich wine-based sauce with peppercorns. Perfect for steaks and beef dishes.',
        'servings': '6',
        'prep_time_minutes': 10,
        'cook_time_minutes': 15,
        'calories_per_serving': 90,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'beef broth', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'cabernet sauvignon', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'green peppercorns', 'preparation': 'crushed'},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'butter', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'tablespoons', 'name': 'peppercorns', 'preparation': 'crushed'},
        ],
        'instructions': [
            'In a medium pan, melt butter then add mushrooms and sauté 3 minutes.',
            'Stir in broth and wine and boil over medium heat stirring occasionally for 5 minutes.',
            'Reduce thickness and wine. Makes 1 1/2 cups.',
        ]
    },

    'IMG_8129_2.JPG': {
        'title': 'Teriyaki Sauce',
        'description': 'Classic Japanese-style teriyaki sauce. Great for marinades and stir-fries.',
        'servings': '8',
        'prep_time_minutes': 5,
        'cook_time_minutes': 10,
        'calories_per_serving': 50,
        'ingredients': [
            {'quantity': '1', 'unit': 'cups', 'name': 'soy sauce', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'brown sugar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'pineapple juice', 'preparation': 'small can'},
        ],
        'instructions': [
            'Boil all ingredients and cool.',
            'Then marinate your meat the longer the better.',
        ]
    },

    'IMG_8130_1.JPG': {
        'title': 'Joy\'s Dressing',
        'description': 'Sweet and tangy white vinegar dressing. Versatile salad dressing.',
        'servings': '8',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 90,
        'ingredients': [
            {'quantity': '5', 'unit': 'tablespoons', 'name': 'oils', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'white vinegar', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'Lawrys seasoning salt', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'garlic salt', 'preparation': None},
        ],
        'instructions': [
            'Blend well and serve.',
        ]
    },

    'IMG_8130_2.JPG': {
        'title': 'Italian Tomato Sauce',
        'description': 'Classic Italian tomato sauce with herbs and garlic. Perfect for pasta.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 45,
        'calories_per_serving': 80,
        'ingredients': [
            {'quantity': '2', 'unit': None, 'name': 'onion', 'preparation': 'chopped'},
            {'quantity': '4', 'unit': 'cloves', 'name': 'garlic', 'preparation': 'chopped'},
            {'quantity': '1', 'unit': None, 'name': 'olive oil', 'preparation': None},
            {'quantity': '2', 'unit': 'pounds', 'name': 'ground beef', 'preparation': None},
            {'quantity': '4', 'unit': 'cans', 'name': 'crushed tomatoes', 'preparation': None},
            {'quantity': '4', 'unit': 'cans', 'name': 'Italian tomatoes', 'preparation': None},
            {'quantity': '2', 'unit': 'cans', 'name': 'tomato paste', 'preparation': None},
        ],
        'instructions': [
            'Sauté onions and garlic in hot oil. Brown meat and sausage, drain fat.',
            'Add tomatoes and paste. Add seasonings last 5 minutes.',
            'Stir in parmesan and serve over noodles or anything.',
        ]
    },

    'IMG_8131_1.JPG': {
        'title': 'Tomato and Basil Soup',
        'description': 'Fresh tomato soup with basil. Comfort food classic.',
        'servings': '6',
        'prep_time_minutes': 15,
        'cook_time_minutes': 30,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '1', 'unit': None, 'name': 'medium onions', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'olive oil', 'preparation': None},
            {'quantity': '2', 'unit': 'large cans', 'name': 'tomatoes', 'preparation': None},
        ],
        'instructions': [
            'Sauté onions in oil and cook until soft about 7 minutes.',
            'Add and pepper, bring to a boil and reduce soup mixture.',
            'Lower heat and reduce soup mixture about 1/4.',
            'Puree soup mixture. Bring to a boil and blend.',
            'Add heavy cream. Serve with basil garnish. Also can be served cold.',
        ]
    },

    'IMG_8131_2.JPG': {
        'title': 'Albondigas Soup',
        'description': 'Mexican meatball soup with vegetables. Hearty and flavorful.',
        'servings': '8',
        'prep_time_minutes': 30,
        'cook_time_minutes': 60,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '2', 'unit': 'pounds', 'name': 'lean ground beef', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'rice', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'chopped onions', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'chopped parsley', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'tablespoon dried oregano', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'whole or crisp chillies', 'preparation': None},
        ],
        'instructions': [
            'Mix beef rice, onion, 1/4 cup cilantro, oregano, eggs, salt and pepper.',
            'Bring broth to boil and meatballs, bring to a boil and add meatballs.',
            'Along with green onions, cilantro onions, simmer 45 minutes to 1 hour or until rice is tender. Serve with hot tortillas.',
        ]
    },

    'IMG_8132_1.JPG': {
        'title': 'Chicken Curried Salad',
        'description': 'Curried chicken salad with mayonnaise. Perfect for sandwiches or lettuce cups.',
        'servings': '10',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 240,
        'ingredients': [
            {'quantity': '5', 'unit': 'cups', 'name': 'cooked chicken', 'preparation': 'diced'},
            {'quantity': '2', 'unit': 'cups', 'name': 'drained pineapple chunks', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'sliced almonds or cashews', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'raisins', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'diced celery', 'preparation': None},
        ],
        'instructions': [
            'Mix mayonnaise, sour cream, salt and curry powder until blended.',
            'Stir chicken, pineapple, celery and grapes then add dressing and top.',
            'With nuts. Serve cold.',
        ]
    },

    'IMG_8132_2.JPG': {
        'title': 'Asparagus, Leek and Potato Soup',
        'description': 'Creamy vegetable soup with asparagus, leeks, and potatoes. Elegant and comforting.',
        'servings': '8',
        'prep_time_minutes': 25,
        'cook_time_minutes': 40,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1/3', 'unit': 'cup', 'name': 'minced fresh parsley', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'unsalted butter', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '6', 'unit': None, 'name': 'extra chicken stock or broth', 'preparation': None},
            {'quantity': '1', 'unit': 'pound', 'name': 'asparagus spears', 'preparation': None},
        ],
        'instructions': [
            'Mix first 7 ingredients in a small bowl.',
            'Can be prepared 2 days ahead. Cover and refrigerate.',
            'Melt 1/4 cup butter in a large pot over low heat.',
            'Add onion and leeks, cook until tender about 15 minutes.',
            'The stock. Bring to boil. Mix in stock and potatoes and bring to a boil.',
            'Reduce heat and simmer. Add asparagus. Cover about 3 minutes and simmer.',
            'To boil. Add and leeks and simmer until crisp tender. About 3 minutes.',
            'Discard bay leaf and season to taste with salt and pepper.',
            'Minutes. Discard about 3 crispest from the held. Simmer until the point in blender.',
            'Serve vegetables are fresh from the held. Sometimes put in blender or different texture. More like a cream of asparagus soup.',
        ]
    },

    'IMG_8133_1.JPG': {
        'title': 'Oriental Chicken Salad',
        'description': 'Asian-inspired chicken salad with crispy noodles and sesame dressing.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cup', 'name': 'butter', 'preparation': None},
            {'quantity': '2', 'unit': 'packages', 'name': 'top ramen noodles', 'preparation': 'without seasoning'},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'sesame seeds', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'rice vinegar', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'soy sauce', 'preparation': None},
        ],
        'instructions': [
            'Melt margarine, add noodles (broken into small pieces), almonds and sesame seeds. Stir until lightly browned.',
            'Cool. Make dressing, mix sugar, oil and soy sauce in a small jar.',
            'Lightly browned. Cool. Make dressing. Add mandarine oranges if desired.',
        ]
    },

    'IMG_8133_2.JPG': {
        'title': 'Broccoli Onion Salad',
        'description': 'Fresh broccoli salad with crispy bacon and sweet dressing.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '1', 'unit': None, 'name': 'cups mayonnaise', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'apple cider vinegar', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'sugar', 'preparation': None},
            {'quantity': '2', 'unit': 'bundles', 'name': 'broccoli', 'preparation': None},
        ],
        'instructions': [
            'Mix first 3 ingredients then combine next 5 ingredients and pour dressing over and mix lightly.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 4 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8129 through IMG_8133")
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
    print(f"BATCH 4 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {31 + success_count} recipes")
    print(f"  📈 Progress: {(31 + success_count)/85*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
