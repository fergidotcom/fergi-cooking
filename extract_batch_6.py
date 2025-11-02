"""
Extract batch 6 of Janet Mason recipes (images 8139-8143)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8139_1.JPG': {
        'title': 'Southwestern Soup',
        'description': 'Hearty southwestern soup with corn, beans, and spices.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 30,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '1', 'unit': 'jar', 'name': 'salsa verde', 'preparation': None},
            {'quantity': '32', 'unit': 'ounces', 'name': 'chicken broth', 'preparation': None},
            {'quantity': '2', 'unit': 'cans', 'name': 'white beans', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': 'rotel tomatoes', 'preparation': None},
        ],
        'instructions': [
            'Put all ingredients in a pot and heat. Can be served with diced onions, avocado, cheese, sour cream or anything you want.',
        ]
    },

    'IMG_8139_2.JPG': {
        'title': 'Corn Chowder with Chilies',
        'description': 'Creamy corn chowder with green chilies and cheese. Southwestern comfort food.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 35,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '32', 'unit': 'ounces', 'name': 'chicken broth', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'cups', 'name': 'heavy whipping cream', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'hot sauce', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'cornmeal or masa', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'water', 'preparation': None},
        ],
        'instructions': [
            'Cook bacon then add onion and sauté until translucent. Then add chilies.',
            'Stir in corn and both kinds of chilies.',
            'Bring to a boil and blend in cornmeal.',
            'Add to soup to thicken and cook 15 minutes.',
            'If you prefer chowder thicken. Add another tablespoon or 15 minutes longer.',
            'On low heat. If you prefer chowder thicker, add chili powder thicker.',
            'Of cornmeal and cook 10 minutes longer.',
        ]
    },

    'IMG_8140_1.JPG': {
        'title': 'Spiced Lentil Soup',
        'description': 'Hearty lentil soup with Italian sausage and vegetables.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 60,
        'calories_per_serving': 260,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'pound', 'name': 'Italian sausages', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'chopped parsley', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': '15 ounce garbonzo beans', 'preparation': 'with juice'},
            {'quantity': '1', 'unit': 'pound', 'name': 'fresh spinach or 2 boxes frozen', 'preparation': None},
            {'quantity': '12', 'unit': 'ounces', 'name': 'jar salsa mild or medium', 'preparation': None},
        ],
        'instructions': [
            'Barley and garlic. Remove from heat and put in soup pot. Add chicken stock, lentils, uncooked butternut.',
            'In soup pot. Add chicken with beans, spinach and salsa.',
            'Parsley. Simmer uncovered 45 minutes to 1 hour until beans are tender.',
            'Simmer basic to pot with beans, spinach and serve.',
            'Hot and serve.',
        ]
    },

    'IMG_8140_2.JPG': {
        'title': 'White Bean and Spinach Soup',
        'description': 'Healthy soup with white beans, spinach, and chicken. Light and nutritious.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 25,
        'calories_per_serving': 200,
        'ingredients': [
            {'quantity': '2', 'unit': 'cans', 'name': 'white beans', 'preparation': None},
            {'quantity': '2', 'unit': 'stalks', 'name': 'celery', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'onions', 'preparation': 'diced'},
            {'quantity': '1', 'unit': 'medium', 'name': 'onions', 'preparation': 'diced'},
            {'quantity': '6', 'unit': 'pounds', 'name': 'ground beef', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
        ],
        'instructions': [
            'Usage. Add carrots, celery onion.',
            'Add chicken broth, pepper, rice and spices. Bring to boil.',
            'Boil and cook over low for 1 hour.',
            'Add spinach and water and add to soup to thicken and cook 15 minutes. Serve.',
            'And simmer for 10 minutes. Serve.',
        ]
    },

    'IMG_8141_1.JPG': {
        'title': 'Popovers',
        'description': 'Light and airy popovers. Classic bread accompaniment.',
        'servings': '8',
        'prep_time_minutes': 10,
        'cook_time_minutes': 40,
        'calories_per_serving': 140,
        'ingredients': [
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'oils', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'milk', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'melted butter', 'preparation': None},
        ],
        'instructions': [
            'Put 1/8 teaspoon oil in each cup. Put in oven and turn to 450. Put all other ingredients in blender and blend on high until smooth. Fill heated cups 1/2 full only and bake for 30 minutes.',
        ]
    },

    'IMG_8141_2.JPG': {
        'title': 'Pita Crisp',
        'description': 'Seasoned pita chips. Perfect snack or appetizer.',
        'servings': '8',
        'prep_time_minutes': 10,
        'cook_time_minutes': 15,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '1', 'unit': None, 'name': 'pita bread', 'preparation': None},
            {'quantity': '6', 'unit': None, 'name': 'garlic butter', 'preparation': None},
            {'quantity': None, 'unit': None, 'name': 'garlic salt', 'preparation': None},
        ],
        'instructions': [
            'Cut each pita into triangles and split segments apart. Melt butter and add garlic salt to taste.',
            'Dip triangles into melted butter and layer them on a cookie sheet. Bake at 325 until crisp about 15 minutes.',
            'Watch closely. Do not brown or over toast.',
        ]
    },

    'IMG_8142_1.JPG': {
        'title': 'Herb Rolls',
        'description': 'Savory herb-flavored dinner rolls.',
        'servings': '12',
        'prep_time_minutes': 90,
        'cook_time_minutes': 15,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cups', 'name': 'butter', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'teaspoons', 'name': 'parsley flakes', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'dill', 'preparation': None},
        ],
        'instructions': [
            'In a 7x10" glass baking dish combine butter, parsley, dill weed and minced dried onions. Place in microwave until butter is melted. Add cheese and stir until evenly distributed on the bottom of the pan.',
            'When all are placed in pan turn over making sure each is coated well. Bake 425 for 12-15 minutes.',
        ]
    },

    'IMG_8142_2.JPG': {
        'title': 'Beer Bread',
        'description': 'Quick and easy beer bread. No yeast required.',
        'servings': '8',
        'prep_time_minutes': 10,
        'cook_time_minutes': 60,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '3', 'unit': 'cups', 'name': 'self-rising flour', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'brown sugar', 'preparation': None},
            {'quantity': '1', 'unit': '12-ounce', 'name': 'can beer', 'preparation': None},
        ],
        'instructions': [
            'Mix together ingredients. Dough will be real stiff. Put in well greased bread pan. Bake 350 for 30-40 minutes. Serve warm.',
        ]
    },

    'IMG_8143_1.JPG': {
        'title': 'Herb Rolls (Alternative)',
        'description': 'Another version of herb rolls with parsley and dill.',
        'servings': '12',
        'prep_time_minutes': 90,
        'cook_time_minutes': 15,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cups', 'name': 'butter', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'teaspoons', 'name': 'parsley flakes', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'dill', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'dried minced onion', 'preparation': None},
            {'quantity': '2', 'unit': 'cans', 'name': 'refrigerator biscuits', 'preparation': 'small cans work best'},
        ],
        'instructions': [
            'In a 7x10" glass baking dish combine butter, parsley, dill weed and minced dried onions. Place in microwave until butter is melted. Add cheese and stir until evenly distributed on the bottom of the pan. Open the biscuit cans and cut the biscuits in half, making sure each is coated well. Bake 425 for 12-15 minutes.',
        ]
    },

    'IMG_8143_2.JPG': {
        'title': 'Beer Bread (Alternative)',
        'description': 'Second version of quick beer bread recipe.',
        'servings': '8',
        'prep_time_minutes': 10,
        'cook_time_minutes': 60,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '3', 'unit': 'cups', 'name': 'self-rising flour', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'brown sugar', 'preparation': None},
            {'quantity': '1', 'unit': '12-ounce', 'name': 'can beer', 'preparation': None},
        ],
        'instructions': [
            'Mix together ingredients. Dough will be real stiff. Put in well greased bread pan. Bake 350 for 30-40 minutes. Serve warm.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 6 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8139 through IMG_8143")
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
    print(f"BATCH 6 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {51 + success_count} recipes")
    print(f"  📈 Progress: {(51 + success_count)/85*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
