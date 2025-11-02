"""
Extract batch 2 of Janet Mason recipes (images 8118-8123)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8118_1.JPG': {
        'title': 'Josephinas Bread',
        'description': 'Savory cheese bread perfect as an appetizer or side dish. Easy to make and always a crowd pleaser.',
        'servings': '10',
        'prep_time_minutes': 15,
        'cook_time_minutes': 30,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '4', 'unit': 'ounces', 'name': 'california green chilies', 'preparation': 'diced'},
            {'quantity': '1', 'unit': 'cup', 'name': 'softened butter', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'mayonnaise', 'preparation': None},
        ],
        'instructions': [
            'In a medium bowl, mix chilies, butter, mayonnaise and cheese until blended.',
            'Sauce French bread into thin slices and spread with cheese mixture.',
            'Mix making sure to cover the bread completely and roll about 5-10 minutes.',
            'Serve on large serving platter and garnish with parsley.',
        ]
    },

    'IMG_8118_2.JPG': {
        'title': 'Cheddar Pennies',
        'description': 'Bite-sized cheesy crackers perfect for parties. Crispy and addictive.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 15,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'finely minced green onions', 'preparation': None},
            {'quantity': '1/2', 'unit': 'pound', 'name': 'sharp cheddar cheese', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'butter', 'preparation': None},
        ],
        'instructions': [
            'Leave cheese and butter out at room temp for several hours. Work all ingredients together with clean hands.',
            'If it is too soft, chill a bit. Roll into 1/2 inch diameter logs, put on ungreased cookie sheets and bake 350°F until nicely browned.',
            'Cut desired place a green stuffed olive in center of cheese when rolling.',
        ]
    },

    'IMG_8119_1.JPG': {
        'title': 'Bourbon-Glazed Shrimp',
        'description': 'Elegant shrimp appetizer with a sweet and savory bourbon glaze. Perfect for special occasions.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 15,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'oils', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'clove garlic', 'preparation': 'minced'},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'fresh lemon juice', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'tablespoons bourbon whiskey', 'preparation': None},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'hot pepper sauce', 'preparation': None},
        ],
        'instructions': [
            'In a large saucepan, heat oil.',
            'Add garlic and stir until golden. Remove from heat.',
            'Contents with a long match and let it burn out.',
            'Add bourbon, heat and add butter, one piece by a time stirring to incorporate.',
            'Position racks 3-6 inches away from heat. Meanwhile, if in each shrimp secure with toothpick.',
            'Arrange in a single layer and sprinkle with salt and freshly ground pepper.',
            'Grill well with sauce. Broil 3-4 minutes and brush with sauce.',
            'Discard sauce. Discard sauce.',
        ]
    },

    'IMG_8119_2.JPG': {
        'title': 'Lamb on Skewers with Mint Sauce',
        'description': 'Tender lamb cubes on skewers served with refreshing mint sauce. Mediterranean-inspired appetizer.',
        'servings': '12',
        'prep_time_minutes': 30,
        'cook_time_minutes': 15,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '4', 'unit': 'pounds', 'name': 'lean lamb', 'preparation': 'cut into 1" cubes'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'olive oil', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'wine vinegar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'fresh mint', 'preparation': 'chopped'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'white vinegar', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'pepper', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'mint', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'thyme', 'preparation': None},
        ],
        'instructions': [
            'Put lamb and marinade ingredients in a bowl. Let stand 3 hours or overnight in refrigerator using wood skewers, put three pieces on a bowl.',
            'And meantime add mint and vinegar. The sauce will be thin.',
            'Before serving. Serve in a small bowl along with hot skewers.',
        ]
    },

    'IMG_8121_LEFT.JPG': {
        'title': 'Artichoke Sauces',
        'description': 'Handwritten collection of sauce recipes from "Artichoke Avenue" including Momma\'s Chocolate Sauce and others.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 10,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '2', 'unit': 'oz', 'name': 'unsweetened chocolate', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': 'evaporated milk', 'preparation': '5 oz'},
        ],
        'instructions': [
            'Melt chocolate over low heat.',
            'Add evaporated milk and cook until thickened.',
            'Serve warm over ice cream or desserts.',
        ]
    },

    'IMG_8121_RIGHT.JPG': {
        'title': 'Imperial Rolls',
        'description': 'Asian-style spring rolls or egg rolls. Crispy fried appetizer with savory filling.',
        'servings': '12',
        'prep_time_minutes': 45,
        'cook_time_minutes': 20,
        'calories_per_serving': 150,
        'ingredients': [
            {'quantity': '1', 'unit': 'tsp', 'name': 'soy sauce', 'preparation': None},
            {'quantity': '1', 'unit': 'tsp', 'name': 'salt', 'preparation': None},
            {'quantity': '30', 'unit': None, 'name': 'rice paper wrappers', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'head lettuce', 'preparation': 'torn into sq. pieces'},
            {'quantity': '30', 'unit': None, 'name': 'mint leaves', 'preparation': None},
        ],
        'instructions': [
            'Sauté ingredients in oil to desired doneness in wok basket wrapping.',
            'You can substitute egg roll wrappers for the rice papers.',
            'Assembling: Dip wrapper in warm water and let drain.',
            'Place one lettuce torn, put carrot slices, brewed ham and 1 tsp.',
            'Roll and serve with sauce made with hoisin sauce mixed with rice vinegar.',
        ]
    },

    'IMG_8122.JPG': {
        'title': 'Mojito',
        'description': 'Classic Cuban cocktail with fresh mint, lime juice, and sparkling water. Refreshing summer drink.',
        'servings': '1',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1 3/4', 'unit': 'ounces', 'name': 'blend of lemon or original citrus', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'superfine sugar', 'preparation': None},
        ],
        'instructions': [
            'Using a pestle and mortar, gently crush the mint with lime juice and sugar.',
            'Add plenty of crushed ice.',
            'Shake well and pour into chilled glass.',
            'Stir and top sparkling water or 7up. Stir and garnish with sprig of mint.',
        ]
    },

    'IMG_8123_1.JPG': {
        'title': 'Citrus Sauce for Artichokes',
        'description': 'Bright, tangy sauce perfect for dipping steamed artichokes. Light and refreshing.',
        'servings': '4',
        'prep_time_minutes': 5,
        'cook_time_minutes': 0,
        'calories_per_serving': 90,
        'ingredients': [
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'chopped mint leaves', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'pepper', 'preparation': None},
            {'quantity': '5', 'unit': 'tablespoons', 'name': 'lemon juice', 'preparation': 'freshly squeezed orange juice'},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'freshly squeezed orange juice', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'chopped chives', 'preparation': None},
        ],
        'instructions': [
            'In small bowl, blend shallots and juice.',
            'Add herbs and salt and pepper.',
            'Adjust with salt and pepper and serve with warm artichoke.',
            'Texture. Adjust with salt and pepper and serve with warm artichoke.',
        ]
    },

    'IMG_8123_2.JPG': {
        'title': 'Otis\'s Secret BBQ Sauce',
        'description': 'Family secret barbecue sauce recipe. Sweet, tangy, and perfect for grilling.',
        'servings': '8',
        'prep_time_minutes': 10,
        'cook_time_minutes': 15,
        'calories_per_serving': 80,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'pound', 'name': 'butter', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'ketchup', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'mustard', 'preparation': None},
        ],
        'instructions': [
            'Combine all ingredients in a saucepan and bring to a boil.',
            'Then simmer.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 2 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8118 through IMG_8123")
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
    print(f"BATCH 2 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {12 + success_count} recipes")
    print("=" * 60)

if __name__ == "__main__":
    main()
