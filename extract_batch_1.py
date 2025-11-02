"""
Extract batch 1 of Janet Mason recipes (images 8112-8117)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8112_1.JPG': {
        'title': 'Mango and Roasted Corn Salsa',
        'description': 'Fresh, vibrant salsa combining sweet mangoes with roasted corn. Perfect as a dip or topping for grilled meats.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 10,
        'calories_per_serving': 80,
        'ingredients': [
            {'quantity': '1 1/2', 'unit': 'cups', 'name': 'ears fresh corn', 'preparation': 'kernels cut off'},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'corn oil', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'cumin', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'ripe mangoes', 'preparation': 'peeled and diced'},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'red onion', 'preparation': 'diced'},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven to 400°F.',
            'Combine corn, oil, and salt in a foil-lined cookie sheet and bake for 15 minutes.',
            'Cool. Combine corn with remaining ingredients.',
            'Toss gently. Chill and serve.',
        ]
    },

    'IMG_8112_2.JPG': {
        'title': 'Walking Fondue',
        'description': 'Fun, portable bread and cheese appetizer. Perfect for parties and gatherings.',
        'servings': '10',
        'prep_time_minutes': 15,
        'cook_time_minutes': 25,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '1', 'unit': 'pound', 'name': 'Swiss cheese', 'preparation': 'cut into strips'},
            {'quantity': '1', 'unit': 'round', 'name': 'sourdough French bread', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'lemon juice', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'dijon mustard', 'preparation': None},
            {'quantity': '1', 'unit': 'pound', 'name': 'butter', 'preparation': None},
        ],
        'instructions': [
            'Cut loaf of bread into 1-inch cubes all over bread making sure you do not cut all the way through the bread.',
            'Cut swiss cheese into flat rectangles and place pieces into each and every crack.',
            'Mix well, butter and add remaining ingredients.',
            'Mix well. Place bread on a cookie sheet and pour butter and add remaining ingredients.',
            'Bake 25 minutes at 350°F.',
        ]
    },

    'IMG_8113.JPG': {
        'title': 'Spinach Artichoke Dip',
        'description': 'Creamy, cheesy dip with spinach and artichokes. A classic party favorite.',
        'servings': '10',
        'prep_time_minutes': 15,
        'cook_time_minutes': 25,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'crumbled chicken bouillon', 'preparation': 'or cubes'},
            {'quantity': '1 1/2', 'unit': 'tablespoons', 'name': 'lemon juice', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sour cream', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'cream', 'preparation': None},
            {'quantity': '1', 'unit': 'ounce', 'name': 'can artichoke bottoms', 'preparation': 'drained'},
            {'quantity': '1', 'unit': 'ounce', 'name': 'jar cheese', 'preparation': 'any kind cheese, finely shredded'},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'garlic', 'preparation': 'finely chopped'},
            {'quantity': '1', 'unit': None, 'name': 'pkg frozen chopped spinach', 'preparation': 'thawed and well drained'},
            {'quantity': '1/2', 'unit': 'cups', 'name': 'heavy cream', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'fresh parmesan cheese', 'preparation': 'grated'},
        ],
        'instructions': [
            'In a large sauce pan, warm the olive oil and butter.',
            'In a large sauce pan, warm the olive oil and butter. When hot, add onions and cook, stirring frequently, for 5 minutes.',
            'Sprinkle in the flour and continue cooking, stirring constantly for 1-2 minutes.',
            'When mixture begins to simmer, add onions and cook, stirring constantly.',
            'When mixture begins to thicken, add the spinach, artichokes, and jack cheese and stir until cheese is melted.',
            'Serve warm with tortilla chips.',
        ]
    },

    'IMG_8114_1.JPG': {
        'title': 'Fresh Tomato Bruschetta',
        'description': 'Classic Italian appetizer with fresh tomatoes, garlic, basil, and olive oil on toasted bread.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 5,
        'calories_per_serving': 140,
        'ingredients': [
            {'quantity': '4', 'unit': None, 'name': 'large tomatoes', 'preparation': 'diced'},
            {'quantity': '1', 'unit': 'cup', 'name': 'shredded mozzarella cheese', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'chopped fresh basil', 'preparation': None},
            {'quantity': '3', 'unit': None, 'name': 'large garlic cloves', 'preparation': 'minced'},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'olive oil', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1/2', 'unit': None, 'name': 'teaspoon pepper', 'preparation': None},
            {'quantity': '1/2', 'unit': None, 'name': 'large French bread baguette', 'preparation': None},
            {'quantity': '3', 'unit': None, 'name': 'large garlic cloves', 'preparation': 'cut in half'},
        ],
        'instructions': [
            'Cut tomatoes in half and scoop out all seeds and let drain well. Dice finely and drain well. Combine with cheese, basil, garlic, olive oil, salt, pepper, and mix well.',
            'Toast thinly sliced baguette slices and mix with garlic halves. Serve.',
        ]
    },

    'IMG_8116_1.JPG': {
        'title': 'Cowboy Caviar',
        'description': 'Southwestern bean and vegetable salsa. Perfect as a dip or side dish.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 110,
        'ingredients': [
            {'quantity': '1 1/2', 'unit': 'ounce', 'name': 'can black-eyed peas and drained', 'preparation': 'rinsed'},
            {'quantity': '1', 'unit': 'can', 'name': 'sweet corn', 'preparation': 'drained'},
            {'quantity': '1', 'unit': 'can', 'name': 'chopped avocado', 'preparation': None},
            {'quantity': '2 1/3', 'unit': 'cup', 'name': 'chopped green onions', 'preparation': None},
            {'quantity': '2/3', 'unit': 'cup', 'name': 'chopped red pepper', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cups', 'name': 'fresh chopped drained tomatoes', 'preparation': None},
        ],
        'instructions': [
            'Mix first five ingredients and make into balls or small balls or red items.',
            'Combine areas 4 ingredients and pour over meat. Cook on Low for 10-12 hours if doing balls or at 325 for 1-1/2 hours if using loaves.',
        ]
    },

    'IMG_8116_2.JPG': {
        'title': 'Chicken Wings',
        'description': 'Baked chicken wings with a flavorful marinade. Great party appetizer.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 60,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'dry mustard', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': 'pineapple juice', 'preparation': 'small'},
            {'quantity': '3', 'unit': 'pounds', 'name': 'chicken wings', 'preparation': None},
        ],
        'instructions': [
            'Boil first five ingredients. Remove from heat. Add wings and marinate for several hours. Fry or bake in marinade.',
            'Marinate for several hours at least. Then boil up again with marinade. Bake uncovered a little then frozen or freeze or serve. May be served hot or cold.',
        ]
    },

    'IMG_8117_1.JPG': {
        'title': 'Pork and Beef Loaf',
        'description': 'Hearty meatloaf made with ground beef and pork. Comfort food classic.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 90,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '2', 'unit': 'pounds', 'name': 'sausage', 'preparation': 'ground beef'},
            {'quantity': '2', 'unit': None, 'name': 'pounds ground', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'egg whites', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'graham cracker crumbs', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'saltine cracker crumbs', 'preparation': None},
        ],
        'instructions': [
            'Mix first five ingredients and make into balls or small loaves.',
            'Place in crockpot if doing small balls or large crockpot if using loaves.',
            'Combine areas 4 ingredients and pour over meat. Cook on Low for 10-12 hours if doing balls or at 325 for 1-1/2 hours if using loaves.',
        ]
    },

    'IMG_8117_2.JPG': {
        'title': 'Spinach Filled Mushrooms',
        'description': 'Elegant stuffed mushroom appetizer with spinach, cheese, and seasonings.',
        'servings': '8',
        'prep_time_minutes': 25,
        'cook_time_minutes': 15,
        'calories_per_serving': 160,
        'ingredients': [
            {'quantity': '3', 'unit': 'pounds', 'name': 'fresh spinach', 'preparation': 'or 2 10 ounce frozen'},
            {'quantity': '36', 'unit': None, 'name': 'large fresh mushrooms', 'preparation': None},
            {'quantity': '3', 'unit': 'cloves', 'name': 'garlic', 'preparation': 'crushed'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'fine bread crumbs', 'preparation': None},
        ],
        'instructions': [
            'In medium sauce pan cook spinach unsalted water until wilted.',
            'Drain and squeeze out excess water. Puree spinach for smooth texture.',
            'Add cheese, melt and transfer and add garlic. Dip corn melted butter and add parmesan cheese. Spread on mushroom caps.',
            'Bake preheated oven 375°F for 5 minutes. Top and crumbs.',
            'Minutes until very soft. Add parmesan and bread crumbs.',
            'Stir until very soft. Add parmesan and bread crumbs and serve. Serve warm garnished with parsley.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 1 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8112 through IMG_8117")
    print("=" * 60)
    print()

    success_count = 0
    error_count = 0

    for filename, recipe_data in RECIPES.items():
        # Get the base filename (remove the _1 or _2 suffix for tracking)
        base_filename = filename.split('_')[0] + '_' + filename.split('_')[1] + '.JPG'

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
    print(f"BATCH 1 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print("=" * 60)

if __name__ == "__main__":
    main()
