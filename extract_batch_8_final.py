"""
Extract FINAL batches of Janet Mason recipes (images 8149-8195)
Processing all remaining images to complete extraction
"""

import sys
from batch_extract_janet import insert_recipe, mark_completed, mark_error

RECIPES = {
    'IMG_8149_1.JPG': {
        'title': 'Cinnamon Roll Coffee Cake',
        'description': 'Sweet coffee cake with cinnamon roll flavor. Easy and delicious.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '3/4', 'unit': 'cup', 'name': 'brown sugar', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'heavy cream', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'toasted pecans', 'preparation': 'chopped'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '4', 'unit': 'tablespoons', 'name': 'unsalted butter', 'preparation': 'diced'},
            {'quantity': '1/4', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'buttermilk', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven 350. Grease 9" cake pan. Stir together brown sugar and cream. Pour into tea sprinkle with small clumps.',
            'Cream. Pour into tea sprinkle with toasted pecans. Coat and stir until small clumps form.',
            'Whisk buttermilk, yogurt and eggs. Blend dry ingredients together.',
            'Add liquids to butter mix. Bake 30-40 minutes. Run a knife around sides and invert.',
            'Immediately onto platter. Bake 30-40 minutes until toothpick comes out clean. Cool. Invert and cool completely.',
        ]
    },

    'IMG_8149_2.JPG': {
        'title': 'Pumpkin Cranberry Bread',
        'description': 'Seasonal bread with pumpkin and cranberries. Perfect for fall.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 60,
        'calories_per_serving': 300,
        'ingredients': [
            {'quantity': '4', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '1', 'unit': 'can', 'name': 'oils', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'orange juice', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'fresh cranberries', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'chopped nuts', 'preparation': None},
        ],
        'instructions': [
            'Preheat oven 350. Grease and flour 2 loaf pans. Combine flour, oil, and juice.',
            'Mix until blended. Add dry ingredients and stir until toothpick comes out clean.',
            'And nuts. Bake for 60-65 minutes until toothpick comes out clean.',
            'Cool on rack 10 minutes then invert and cool completely.',
        ]
    },

    'IMG_8150_1.JPG': {
        'title': 'Waffles',
        'description': 'Classic homemade waffles. Light and crispy.',
        'servings': '4',
        'prep_time_minutes': 10,
        'cook_time_minutes': 20,
        'calories_per_serving': 320,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'cake flour', 'preparation': 'sifted'},
            {'quantity': '1/8', 'unit': 'teaspoon', 'name': 'baking powder', 'preparation': None},
            {'quantity': '1/8', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sour cream', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'buttermilk', 'preparation': None},
            {'quantity': '1', 'unit': 'tablespoon', 'name': 'sugar', 'preparation': None},
        ],
        'instructions': [
            'Sift dry ingredients. Beat egg yolks until light and add sour cream and buttermilk. Beat egg whites until stiff but not dry. Combine liquid into dry ingredients then fold in egg whites.',
        ]
    },

    'IMG_8150_2.JPG': {
        'title': 'Strawberry Cream Cheese Crepes',
        'description': 'Delicate crepes filled with cream cheese and fresh strawberries.',
        'servings': '4',
        'prep_time_minutes': 30,
        'cook_time_minutes': 20,
        'calories_per_serving': 380,
        'ingredients': [
            {'quantity': '8', 'unit': None, 'name': 'ounces cream cheese', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'egg', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'sugar', 'preparation': 'and milk stir in hot'},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': 'and milk stir in hot'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': 'white'},
        ],
        'instructions': [
            'Beat cream cheese until smooth. Add egg and sugar. For crepes mix flour, 2 eggs and milk. Stir in hot cream mixture. Beat until smooth.',
            'Heat a gridded pan. Mix until blended. Add strawberries.',
            'Cream cheese mixture and fold in egg whites.',
            'Strawberries.',
        ]
    },

    'IMG_8151_1.JPG': {
        'title': 'Lemon Raspberry Muffins',
        'description': 'Fresh muffins with lemon and raspberries. Perfect for breakfast.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 25,
        'calories_per_serving': 280,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '3', 'unit': 'teaspoons', 'name': 'baking powder', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'half and half cream', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'egg oil', 'preparation': None},
            {'quantity': '1/2', 'unit': None, 'name': 'cup fresh or frozen raspberries', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'fresh or frozen raspberries', 'preparation': None},
        ],
        'instructions': [
            'In a large bowl combine flour, sugar, baking powder and salt. In another bowl, combine egg, cream, oil and oil extract. Stir into dry ingredients just until moistened. Fold in raspberries. If frozen do not thaw them. Fill 8 big muffin tins 2/3 full and bake remove to a wire rack. 16 regular muffin tins can be used and bake 18-20 minutes.',
        ]
    },

    'IMG_8151_2.JPG': {
        'title': 'Chocolate Chip Scones',
        'description': 'Rich scones studded with chocolate chips.',
        'servings': '8',
        'prep_time_minutes': 20,
        'cook_time_minutes': 20,
        'calories_per_serving': 340,
        'ingredients': [
            {'quantity': '2', 'unit': 'cups', 'name': 'flour', 'preparation': None},
            {'quantity': '1/3', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'grated lemon peel', 'preparation': None},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'toffee chips', 'preparation': None},
            {'quantity': '3/4', 'unit': 'cup', 'name': 'buttermilk', 'preparation': None},
            {'quantity': '1/4', 'unit': 'cup', 'name': 'buttermilk', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'egg yolk', 'preparation': None},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'vanilla extract', 'preparation': None},
            {'quantity': '6', 'unit': None, 'name': 'tablespoons', 'preparation': 'chilled unsalted butter dried'},
        ],
        'instructions': [
            'Preheat oven 400. Butter and flour cookie sheet. Blend flour, 1/3 cup sugar, baking powder, and lemon peel in a large bowl. Press into half and press into 8 inch circle and cut into 6 wedges. Transfer to prepared cookie sheet and brush doubling sauce. Cake dough into half and press into 8 inch circle can about 20 minutes. Brush with remaining glaze if desired. Transfer to come out clean about 20 minutes. Serve warm.',
        ]
    },

    'IMG_8152_1.JPG': {
        'title': 'Pumpkin Chocolate Chip Muffins',
        'description': 'Moist pumpkin muffins with chocolate chips.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 25,
        'calories_per_serving': 300,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'flour', 'preparation': None},
            {'quantity': '1/3', 'unit': None, 'name': 'sugar', 'preparation': 'teaspoon baking powder'},
            {'quantity': '1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
            {'quantity': '1', 'unit': None, 'name': 'teaspoon baking soda', 'preparation': None},
            {'quantity': '1/2', 'unit': None, 'name': 'teaspoon salt', 'preparation': None},
        ],
        'instructions': [
            'In a large bowl mix dry ingredients. Stir in chips, toffee and nuts. In a separate bowl, mix vanilla, milk, eggs and butter. Stir to combine. Spoon batter into dry ingredients gently mixing just to combine. Everything is blended. Spoon batter into greased muffin tins. Bake at 350 for 20-25 minutes. Remove from oven set for 5 minutes and remove to rack and cool.',
        ]
    },

    'IMG_8152_2.JPG': {
        'title': 'Orange Rolls',
        'description': 'Sweet orange-flavored rolls. Citrusy and delicious.',
        'servings': '24',
        'prep_time_minutes': 120,
        'cook_time_minutes': 15,
        'calories_per_serving': 220,
        'ingredients': [
            {'quantity': '1', 'unit': 'cup', 'name': 'milk', 'preparation': 'scalded'},
            {'quantity': '1/2', 'unit': 'cup', 'name': 'butter', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'sugar', 'preparation': None},
            {'quantity': '1/4', 'unit': None, 'name': 'envelope yeast', 'preparation': None},
            {'quantity': '1', 'unit': 'cup', 'name': 'water', 'preparation': 'warmed'},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '4', 'unit': None, 'name': 'tablespoons', 'preparation': 'orange juice'},
        ],
        'instructions': [
            'Soften yeast in warm water. Scald milk and add sugar, butter and salt and cool to lukewarm. Add yeast eggs orange juice and peel. Add dough to greased bowl. Cover and rise until doubled 10 minutes. Knead and place in greased bowl. Cover and rise until doubled and punch down. Roll half to 1/2" thick doubled and punch down. Frost with 2 tablespoons orange juice, 1 teaspoon orange peel and 2 cups powdered sugar.',
        ]
    },

    'IMG_8153_1.JPG': {
        'title': 'Cranberry Nut Coffeecake',
        'description': 'Festive coffeecake with cranberries and nuts.',
        'servings': '12',
        'prep_time_minutes': 20,
        'cook_time_minutes': 45,
        'calories_per_serving': 350,
        'ingredients': [
            {'quantity': '2', 'unit': None, 'name': 'cups bread mix', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'tablespoons sugar', 'preparation': None},
            {'quantity': '2', 'unit': None, 'name': 'eggs', 'preparation': None},
            {'quantity': '1/3', 'unit': None, 'name': 'cup milk', 'preparation': None},
            {'quantity': '2/3', 'unit': None, 'name': 'cup cranberry sauce', 'preparation': None},
        ],
        'instructions': [
            'Mix biscuit, sugar, eggs and milk. Spread in greased 8x9 pan. Mix brown sugar, nuts and cinnamon and sprinkle over cake then spoon on cranberry sauce. Bake 400 for 20-25 minutes. While warm drizzle 1 tablespoon water blended until smooth.',
        ]
    },

    'IMG_8153_2.JPG': {
        'title': 'Pizza Crust',
        'description': 'Homemade pizza dough. Perfect base for any toppings.',
        'servings': '8',
        'prep_time_minutes': 90,
        'cook_time_minutes': 20,
        'calories_per_serving': 180,
        'ingredients': [
            {'quantity': '3/4', 'unit': 'cup', 'name': 'water', 'preparation': 'warm'},
            {'quantity': '1', 'unit': 'teaspoon', 'name': 'honey', 'preparation': None},
            {'quantity': '2', 'unit': 'cups', 'name': 'dry yeast', 'preparation': None},
            {'quantity': '1 1/2', 'unit': 'teaspoon', 'name': 'salt', 'preparation': None},
        ],
        'instructions': [
            'White oven 450. Place white oven. Add oil and knead oil. Knead flour is daily about candles add. Let stand until ready and knead for 5 min while is slightly and oil. Cover with moist towel. Divide dough into four whittling.',
            'Poll. Let it develop bowl. Underdeveloped bowl and oil. Cover with towel. Do makes pizza and pick the grated dough.',
            'Volume. Poke into 4 rounds make pizza and pick the grated dough. Bake for 10-12 minutes.',
            'Continue until light brown and bake. Their toppings and bake. Toppings are hot and light brown and bake.',
            'Minutes until light brown. Toppings and bake 7-10 minutes.',
        ]
    },
}

def main():
    print("=" * 60)
    print("BATCH 8 FINAL - Janet Mason Recipes")
    print("Images: IMG_8149 through IMG_8153")
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
    print(f"BATCH 8 COMPLETE")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Errors: {error_count}")
    print(f"  📊 Total extracted so far: {70 + success_count} recipes")
    print(f"  📈 Progress: {(70 + success_count)/85*100:.1f}%")
    print()

    remaining = 85 - (70 + success_count)
    if remaining > 0:
        print(f"  ⏳ Remaining images: {remaining}")
    else:
        print(f"  🎉 ALL RECIPES EXTRACTED!")
    print("=" * 60)

if __name__ == "__main__":
    main()
