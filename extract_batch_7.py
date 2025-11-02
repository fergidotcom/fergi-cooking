"""
Extract batch 7 of Janet Mason recipes (images 8144-8148)
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8144_1.JPG': {
        'title': 'Napkin Rolls',
        'description': 'Easy bread rolls shaped like napkins. Fun presentation.',
        'servings': '18',
        'prep_time_minutes': 90,
        'cook_time_minutes': 15,
        'calories_per_serving': 160,
        'ingredients': [
            {'quantity': '1', 'unit': 'packet', 'name': 'yeast', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'sugar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'warm water', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'milk', 'preparation': None},
            {'quantity': '3', 'unit': 'eggs', 'preparation': None},
            {'quantity': '4', 'unit': 'cups', 'name': 'flour', 'preparation': 'generous'},
        ],
        'instructions': [
            'Crinkle yeast add 1 tablespoon sugar and 1/2 cup warm water. Leave. Place 1/2 cup sugar, salt and 1/2 cup milk (can use low heat until the milk scales) the butter. Let rise in a warm place for 60 minutes. Cover top of dough with melted butter and let rise in a warm place no matter at all. It takes about an hour.',
            'Roll and cut in wedges and roll up the widest to the point as for rolls. Remove and punch in a warm place. Bake 400 for 8-10 minutes.',
        ]
    },

    'IMG_8144_2.JPG': {
        'title': 'Banana Nut Bread',
        'description': 'Classic moist banana bread with nuts.',
        'servings': '8',
        'prep_time_minutes': 15,
        'cook_time_minutes': 60,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'baking soda', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'butter', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'count', 'preparation': None},
            {'quantity': '3', 'unit': None, 'name': 'bananas - over rippened', 'preparation': None},
        ],
        'instructions': [
            'Mix all ingredients together and pour into a greased loaf pan or 3 small loaf pans. Bake 350 for 1 hour shorter if in small pans.',
        ]
    },

    'IMG_8145_1.JPG': {
        'title': 'Blueberry-Banana Bread',
        'description': 'Sweet bread combining blueberries and bananas.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 60,
        'calories_per_serving': 300,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'fresh blueberries', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '3/4', 'unit': 'teaspoon', 'name': 'baking soda', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'oatmeal', 'preparation': 'dried banana chips'},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'brown sugar', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'butter', 'preparation': 'cut into chunks'},
        ],
        'instructions': [
            'Preheat oven 350. In a small bowl. Gently toss blueberries with 1 tablespoon flour. Combine flour, sugar, baking powder and soda, salt and cinnamon. In third bowl combine butter and eggs. Mash in bananas and chips.',
            'Gently stir in blueberries. Spread batter in buttered 5x9 loaf pan. Mash butterscotch chips and nuts. Onto batter. Combine chips and butter.',
            'By combining hours and his and crisps sugar and butter and raisins. Baked 60-70 minutes until toothpick comes out.',
            'And invert and cool. 45 minutes and invert and cool 45 minutes.',
        ]
    },

    'IMG_8145_2.JPG': {
        'title': 'Pumpkin Ginger Scones',
        'description': 'Seasonal scones with pumpkin and crystallized ginger.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 20,
        'calories_per_serving': 240,
        'ingredients': [
            {'quantity': '5', 'unit': 'tablespoons', 'name': 'butter', 'preparation': None},
            {'quantity': '2', 'unit': 'eggs', 'name': 'pumpkins', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'sour cream', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'chopped crystallized ginger', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'chopped raisins', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven to 425. Reserve a tablespoon of sugar. Combine remaining and flour, cinnamon, baking powder, baking soda and salt.',
            'Remove cut flour. Flour cinnamon and mixture resembles coarse crumbs. Beat egg in a small bowl. Add pumpkin mixture.',
            'Stir into flour mixture. Resembles course crumbs.',
            'Led to combine then stir in dried pumpkin mixture. Stir in candied ginger and raisins.',
            'Knead 5 times. Pat out into a circle and cut into pie wedges.',
            'And scones and sprinkle with reserved sugar and bake and brush on oil.',
            'Scones and sprinkle with reserved sugar. Bake 10-12 minutes until golden brown.',
        ]
    },

    'IMG_8146_1.JPG': {
        'title': 'Quick Caramel Coffee Cake',
        'description': 'Easy coffee cake with caramel topping.',
        'servings': '10',
        'prep_time_minutes': 15,
        'cook_time_minutes': 30,
        'calories_per_serving': 320,
        'ingredients': [
            {'quantity': '1/2', 'unit': 'cup', 'name': 'butter', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'firmly packed brown sugar', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'firmly packed brown sugar', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'cans refrigerator flaky biscuits', 'preparation': None},
        ],
        'instructions': [
            'Heat oven 375. In small sauce pan melt butter, brown sugar and water. Bring to a boil. Add nuts, grease the sides and bottom of 12 inch bundt pan. Pour the butter mixture into the bottom. Take biscuits and cut in your bees. Place over the caramel sauce get over the biscuits. Some in pan and drizzle half of the caramel sauce over the biscuits. Invert immediately onto waxed paper and remove from pan.',
        ]
    },

    'IMG_8146_2.JPG': {
        'title': 'Nutty Baked French Toast',
        'description': 'Overnight French toast casserole with nuts and cinnamon.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 340,
        'ingredients': [
            {'quantity': '1', 'unit': 'loaf', 'name': 'white bread', 'preparation': 'sliced'},
            {'quantity': '8', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'of butter', 'preparation': None},
            {'quantity': '3', 'unit': 'tablespoons', 'name': 'dark corn syrup', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'chopped nuts', 'preparation': None},
        ],
        'instructions': [
            'Generously grease 9x13 pan. Fill pan with bread slices to within 1/2".',
            'Of top. Blend egg, milk, half and half. Vanilla, nutmeg and cinnamon.',
            'Combine last 1/2 ingredients and set aside. Spread topping over french toast.',
            'Bake 350 for 50 minutes until puffed and golden brown. Cover with foil if it gets to brown.',
        ]
    },

    'IMG_8147_1.JPG': {
        'title': 'Kansas Coffee Cake',
        'description': 'Traditional coffee cake with yellow cake mix and vanilla pudding.',
        'servings': '12',
        'prep_time_minutes': 15,
        'cook_time_minutes': 45,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '1', 'unit': 'package', 'name': 'yellow cake mix', 'preparation': 'no pudding(small)'},
            {'quantity': '1', 'unit': 'box', 'name': 'instant vanilla pudding(small)', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'water', 'preparation': None},
            {'quantity': '4', 'unit': None, 'name': 'eggs', 'preparation': None},
        ],
        'instructions': [
            'Blend cake mix, pudding(dry), oil and water. Mix well at medium speed. Add eggs one at a time. Beating well after each. Mix nuts, sugar and cinnamon.',
            'Pour 1/3 of the nut mixture in bottom of well greased 10 inch bundt pan. Fold the rest into cake batter. Bake at 350 for 50 min. Let stand 5-10 min. Before inverting onto a plate.',
        ]
    },

    'IMG_8147_2.JPG': {
        'title': 'Strawberry Crunch Coffee Cake',
        'description': 'Sweet coffee cake with strawberries and crumb topping.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 360,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '13', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '3/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '3/4', 'unit': 'teaspoon', 'name': 'baking powder', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'milk', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven 425. Mix together first 4 ingredients. Cut in 1/3 cup butter to resemble come crumbs. Mix together milk and eggs. Stir into crumb mixture. Spread into greased 9x13 pan. Cover with strawberry mixture. Spread with topping.',
            'Bake 50 for 50 minutes. Bake 50 minutes until puffed and golden brown. Cover with topping.',
            'Last three ingredients and sprinkle over berries and bake 35-40 minutes.',
        ]
    },

    'IMG_8148_1.JPG': {
        'title': 'Pancakes',
        'description': 'Classic homemade pancakes.',
        'servings': '4',
        'prep_time_minutes': 10,
        'cook_time_minutes': 15,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'egg', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'egg', 'preparation': 'buttermilk'},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'sugar', 'preparation': None},
            {'quantity': '2', 'unit': 'tablespoons', 'name': 'oil', 'preparation': None},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'Mix all ingredients; add any extras you want and pour onto a hot griddle and cook until light brown on both sides.',
        ]
    },

    'IMG_8148_2.JPG': {
        'title': 'Brown Butter Streusel Crumb Cakes',
        'description': 'Rich coffee cake with brown butter and streusel topping.',
        'servings': '12',
        'prep_time_minutes': 25,
        'cook_time_minutes': 35,
        'calories_per_serving': 420,
        'ingredients': [
            {'quantity': '1 1/3', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'firmly packed brown sugar', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': '1/2', 'name': 'teaspoons', 'preparation': 'vanilla extract'},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven 350. Grease pan. Heavily flour. Brown butter. Firmly brown.',
            'To golden and solids are golden and melt looks and solids.',
            'Set aside. In a another bowl. Blend buttermilk and vanilla and set.',
            'In a mother bowl. Blend buttermilk. Butter into bowl. Into bowl.',
            'To batter until golden bits. Add butter until melt bits and brown. Add sugar and buttermilk.',
            'Shakes finger tips mix texture to resemblable come crumbs set inside melt 5.',
            'Butter until melt. In a mother bowl. Blend buttermilk mixture alternately with buttermilk mixture.',
            'And add flour mixture alternately with buttermilk mixture and top.',
            'Batter and melt butter mix ture alternately with buttermilk mixture and top.',
            'Bake topping. Bake 10-12 toothpick comes out.',
            'Sprinkle cool mixture with baking clean. Cool 15 minutes then remove from pan.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 7 EXTRACTION - Janet Mason Recipes")
    print("Images: IMG_8144 through IMG_8148")
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
    print(f"BATCH 7 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {61 + success_count} recipes")
    print(f"  📈 Progress: {(61 + success_count)/85*100:.1f}%")
    print("=" * 60)

if __name__ == "__main__":
    main()
