"""
Extract batch 5 of Janet Mason recipes (images 8134-8138)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8134_1.JPG': {
        'title': 'Autumn Salad',
        'description': 'Fall-inspired salad with lettuce, pecans, and seasonal flavors.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '1', 'unit': 'head', 'name': 'lettuce', 'preparation': None},
            {'quantity': '1', 'unit': 'head', 'name': 'romaine lettuce', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'glazed pecans', 'preparation': 'chopped'},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'red onions', 'preparation': 'sliced'},
            {'quantity': '2', 'unit': 'cups', 'name': 'red cabbage apples', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': 'cups', 'name': 'raisins', 'preparation': None},
        ],
        'instructions': [
            'Glazed pecans: 1/4 cup butter, 1/4 cup light corn syrup, 2 Tbsp water, 1 teaspoon salt.',
            'Boil, add pecans, line cookie sheet with foil. Bake pecans @250 for 1 hour. Toss and serve.',
        ]
    },

    'IMG_8134_2.JPG': {
        'title': 'Berry Mandarin Tossed Salad',
        'description': 'Sweet and tangy salad with berries, mandarin oranges, and celery.',
        'servings': '6',
        'prep_time_minutes': 15,
        'cook_time_minutes': 0,
        'calories_per_serving': 140,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'ground mustard', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'onion juice', 'preparation': 'minced red onion'},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'celery seeds', 'preparation': None},
            {'quantity': '1', 'unit': 'dash', 'name': 'salt', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'oil', 'preparation': None},
        ],
        'instructions': [
            'Mix salad ingredient: 8 oz torn lettuce leaves, 2 c fresh strawberries sliced, 1 can mandarin oranges-drained, 1 medium red onion sliced, 1/3 c toasted almonds, 4 strips bacon cooked and crumbled.',
            'In a bowl microwave first nine ingredients for 2 minutes. Stir until sugar dissolves. Whisk in oil.',
            'Toss with dressing and serve immediately.',
        ]
    },

    'IMG_8135_1.JPG': {
        'title': 'Carrot Salad',
        'description': 'Simple shredded carrot salad with raisins and vinegar dressing.',
        'servings': '6',
        'prep_time_minutes': 15,
        'cook_time_minutes': 0,
        'calories_per_serving': 120,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cup', 'name': 'raisins', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'cider vinegar', 'preparation': None},
            {'quantity': '2-3', 'unit': None, 'name': 'chopped green onions', 'preparation': None},
            {'quantity': '3', 'unit': 'cups', 'name': 'grated carrots', 'preparation': None},
            {'quantity': '3', 'unit': 'cups', 'name': 'olive oil', 'preparation': None},
        ],
        'instructions': [
            'Soak raisins in vinegar for 30 minutes.',
            'Drain and reserve vinegar. Mix oil with vinegar, salt and nutmeg. Toss.',
            'This is my personal favorite carrot salad recipe and is from Martha Stewart.',
        ]
    },

    'IMG_8135_2.JPG': {
        'title': 'Bloody Mary Salad',
        'description': 'Savory salad inspired by the classic Bloody Mary cocktail flavors.',
        'servings': '4',
        'prep_time_minutes': 20,
        'cook_time_minutes': 0,
        'calories_per_serving': 160,
        'ingredients': [
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'olive oil', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'minced shallots', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'lime juice', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'spicy V-8 juice', 'preparation': None},
            {'quantity': '1/2', 'unit': 'small can', 'name': 'worcestershire sauce', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'worcestershire sauce', 'preparation': None},
        ],
        'instructions': [
            'Heat oil and sauté shallots until soft. About 3 minutes. Deglaze with worcestershire vinegar, lime, and juice of a lemon.',
            'Boil 5 minutes. Then season with salt and pepper.',
            'Add lettuce tomatoes and celery. Season with homemade croutons seed.',
            'Worcestershire vinegar mustard sugar horseradish celery seed. Advanced toss remaining ingredients and season with salt and pepper.',
            'Divide among plates and serve with a shot glass of dressing.',
        ]
    },

    'IMG_8136_1.JPG': {
        'title': 'Taco Soup',
        'description': 'Hearty Mexican-inspired soup with beef, beans, and taco seasonings.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 45,
        'calories_per_serving': 320,
        'ingredients': [
            {'quantity': '1', 'unit': 'lb', 'name': 'ground chuck', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'large onion', 'preparation': 'chopped'},
            {'quantity': '15', 'unit': 'oz', 'name': 'black beans', 'preparation': 'undrained'},
            {'quantity': '15', 'unit': 'oz', 'name': 'corn', 'preparation': 'undrained'},
            {'quantity': '15', 'unit': 'oz', 'name': 'tomato sauce', 'preparation': None},
            {'quantity': '14', 'unit': 'oz', 'name': 'diced tomatoes', 'preparation': 'undrained'},
            {'quantity': '1', 'unit': 'envelope', 'name': 'ranch style dressing mix', 'preparation': None},
            {'quantity': '1', 'unit': 'envelope', 'name': 'taco seasoning', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'cups', 'name': 'water', 'preparation': None},
        ],
        'instructions': [
            'Cook beef and onions until brown. Then drain and return to pot.',
            'Brown the onion. Add beans, undrained.',
            'Bring to boil. Reduce heat and simmer uncovered for 15 minutes. And simmer uncovered for about 10 to 15 minutes stirring occasionally.',
            'Top with cheese and top with cheese and corn chips.',
        ]
    },

    'IMG_8136_2.JPG': {
        'title': 'Tortilla Soup',
        'description': 'Classic Mexican tortilla soup with chicken, tomatoes, and crispy tortilla strips.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '2', 'unit': None, 'name': 'white onions', 'preparation': 'quartered'},
            {'quantity': '5', 'unit': None, 'name': 'tomato', 'preparation': 'unpeeled'},
            {'quantity': '4', 'unit': None, 'name': 'cloves garlic', 'preparation': 'chopped'},
            {'quantity': '1/4', 'unit': 'oz', 'name': 'can chicken broth', 'preparation': None},
            {'quantity': '3', 'unit': None, 'name': 'chicken breast', 'preparation': 'bone-in no skin'},
            {'quantity': '6', 'unit': None, 'name': 'corn tortillas', 'preparation': 'cut into pieces'},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'cumin', 'preparation': 'ground'},
            {'quantity': '1', 'unit': None, 'name': 'bay leaf', 'preparation': None},
        ],
        'instructions': [
            'Preheat griddle in high. Rub onions and tomatoes with oil and add chicken breast and tomatoes. Put in a large pot and add chicken breast and chili.',
            'You may need to do this in several batches. Put tomatoes that are blackened and tomatoes will not brown. Finish with a vegetable peeler.',
            'Strain and cut chicken in a large pot. Add chicken back and chicken and simmer for 30 minutes.',
            'Remove chicken and allow to a boil. Simmer for 30 minutes. Remove chicken and cool.',
            'Shred the chicken and bring to a boil and cut into large chicken and cool shreds.',
            'And tortilla strips and simmer for 30 minutes. Add seasonings. Stir and cook 2 minutes. Add seasonings.',
            'To slice avocado etc on top with a vegetable peeler and top with avocado, cheese and enjoy.',
        ]
    },

    'IMG_8137_LEFT.JPG': {
        'title': 'Chicken Gorgonzola Salad',
        'description': 'Gourmet salad with grilled chicken, gorgonzola cheese, and handwritten recipe card.',
        'servings': '4',
        'prep_time_minutes': 25,
        'cook_time_minutes': 15,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '4', 'unit': None, 'name': 'chicken breasts', 'preparation': 'cooked and shredded'},
            {'quantity': '4', 'unit': 'cups', 'name': 'spring mix', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'walnuts', 'preparation': None},
            {'quantity': '1/4', 'unit': 'pound', 'name': 'gorgonzola', 'preparation': None},
        ],
        'instructions': [
            'Cook the chicken. From the handwritten recipe card.',
            'Toss salad mix with the chicken.',
            'Add walnuts and gorgonzola.',
        ]
    },

    'IMG_8137_RIGHT.JPG': {
        'title': 'Bacon Dressing Salad with White Wine',
        'description': 'Salad with warm bacon dressing and white wine vinegar.',
        'servings': '6',
        'prep_time_minutes': 15,
        'cook_time_minutes': 10,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '1/4', 'unit': 'lb', 'name': 'bacon', 'preparation': 'chopped'},
            {'quantity': '1', 'unit': None, 'name': 'chicken', 'preparation': 'broiled, chopped'},
            {'quantity': '1/2', 'unit': 'tsp', 'name': 'ground', 'preparation': 'pepper'},
            {'quantity': '1/2', 'unit': None, 'name': 'ground ginger', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'cucumber', 'preparation': 'peeled + sliced'},
            {'quantity': '1/8', 'unit': 'c', 'name': 'raisins', 'preparation': None},
        ],
        'instructions': [
            'Fry bacon and chicken together.',
            'Set to one side and brown. Finish with ground ginger.',
            'Add cucumber and raisins.',
            'Sprinkle with pepper.',
        ]
    },

    'IMG_8138_1.JPG': {
        'title': 'Mushroom Soup',
        'description': 'Creamy wild mushroom soup with sherry and herbs.',
        'servings': '6',
        'prep_time_minutes': 20,
        'cook_time_minutes': 30,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '1', 'unit': 'ounce', 'name': 'dry wild mushrooms', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'sherry', 'preparation': None},
            {'quantity': '4', 'unit': 'tablespoons', 'name': 'unsalted butter', 'preparation': None},
            {'quantity': '4', 'unit': None, 'name': 'medium onions', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': None, 'name': 'medium onions', 'preparation': 'chopped'},
        ],
        'instructions': [
            'Rinse wild mushrooms well then soak. Trim in sherry for 1 hour.',
            'Drain the mushrooms and reserve. Leave mushrooms, fresh and preserved.',
            'Whole chop coarsely. Melt the butter in a soup coarsely and reserve.',
            'Flour and cook and stir 2 minutes add wild mushrooms.',
            'Sherry and bring the soup to a boil. Stir in flour and mushroom.',
            'Mushrooms are very tender. Add the seasonings. Taste and adjust the seasoning.',
            'Remove from heat and let stand 5-10 minutes before stirring the seasoning.',
            'Cream. Serve and buo.',
        ]
    },

    'IMG_8138_2.JPG': {
        'title': 'Bushnell Vegetarian Chili',
        'description': 'Hearty vegetarian chili with beans, peppers, and spices.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 240,
        'ingredients': [
            {'quantity': '1', 'unit': None, 'name': 'large onion', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': None, 'name': 'large stalks of celery', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'green peppers', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': None, 'name': 'cloves garlic', 'preparation': 'chopped'},
            {'quantity': '2', 'unit': None, 'name': 'chopped jalapeño', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': '15-ounce cans pinto beans', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': '15-ounce cans black beans', 'preparation': 'drained and rinsed'},
            {'quantity': '1', 'unit': None, 'name': '15-ounce cans red beans', 'preparation': 'drain and rinse'},
            {'quantity': '2', 'unit': 'cans', 'name': 'water', 'preparation': None},
        ],
        'instructions': [
            'Sauté green peppers, celery onion, jalapeño, and garlic in oil over medium high heat.',
            'About 5 minutes on until tender, then add drained pinto beans.',
            'Medium high heat. About 5 minutes. And beans and blend meat and beans with top on stirring occasionally.',
            'Ingredients and blend meat and beans with top on stirring occasionally.',
            'So it does not burn. Let it simmer overnight and season with salt and pepper to taste.',
            'Occasionally so it does not burn until hot. Let it mellow overnight if possible and pepper to taste.',
            'With salsa and add pepper to taste. Let it mellow overnight or around meat seasoned with chili for the non-vegetarians.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 5 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8134 through IMG_8138")
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
    print(f"BATCH 5 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {41 + success_count} recipes")
    print(f"  📈 Progress: {(41 + success_count)/85*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
