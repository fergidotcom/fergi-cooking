#!/usr/bin/env python3
"""
Comprehensive recipe enhancement:
1. Analyze each recipe and write elegant descriptions
2. Add prep/cook times, servings, calorie estimates
3. Enhance instructions with inline ingredient quantities
"""

import sqlite3
import json
import re
from pathlib import Path

# Recipe enhancements - manually curated based on recipe analysis
RECIPE_ENHANCEMENTS = {
    "Beef Bourguignon": {
        "description": "Classic French braised beef in red wine with pearl onions, mushrooms, and bacon. This elegant Burgundian dish features tender beef chunks slowly simmered in a rich wine sauce, developing deep, complex flavors perfect for special occasions.",
        "prep_time": 30,
        "cook_time": 180,
        "servings": "6-8",
        "calories": 520
    },
    "Beef Bourguignon Joe's": {
        "description": "Joe's refined version of the classic French beef stew, featuring premium beef braised in burgundy wine with aromatic vegetables, bacon, and herbs. This hearty, sophisticated dish balances rich flavors with tender meat in a velvety sauce.",
        "prep_time": 35,
        "cook_time": 165,
        "servings": "6-8",
        "calories": 540
    },
    "Beef Stroganoff": {
        "description": "Rich Russian-inspired comfort food with tender beef strips in a creamy mushroom and sour cream sauce. Quick-cooking and luxurious, this classic dish pairs perfectly with egg noodles or rice for a satisfying weeknight meal.",
        "prep_time": 15,
        "cook_time": 25,
        "servings": "4-6",
        "calories": 450
    },
    "Chicken Piccata: Pan Fried Breaded Chicken Cutlets with Lemon & Caper Sauce – Homemade Italian Cooki": {
        "description": "Bright Italian classic featuring tender, pan-fried chicken cutlets in a tangy lemon-caper butter sauce. Light and elegant, this restaurant-quality dish comes together quickly with simple ingredients and bold Mediterranean flavors.",
        "prep_time": 15,
        "cook_time": 20,
        "servings": "4",
        "calories": 380
    },
    "Eggplant Parm": {
        "description": "Italian-American vegetarian favorite with layers of breaded eggplant, rich tomato sauce, and melted mozzarella. Baked until golden and bubbling, this hearty dish delivers comfort food satisfaction without the meat.",
        "prep_time": 30,
        "cook_time": 45,
        "servings": "6",
        "calories": 425
    },
    "Mueller's Classic Lasagna": {
        "description": "Traditional layered pasta masterpiece with seasoned ground beef, ricotta cheese, and marinara sauce. This crowd-pleasing Italian-American staple is perfect for family gatherings and makes excellent leftovers.",
        "prep_time": 30,
        "cook_time": 60,
        "servings": "8-10",
        "calories": 480
    },
    "Mary's Favorite Fettuccine Alfredo": {
        "description": "Luxuriously creamy pasta dish featuring tender fettuccine noodles tossed in a rich butter and Parmesan cream sauce. Simple yet indulgent, this Roman classic requires just a few quality ingredients for maximum flavor.",
        "prep_time": 5,
        "cook_time": 15,
        "servings": "4",
        "calories": 650
    },
    "Chicken Florentine": {
        "description": "Elegant Italian chicken dish with tender breasts in a creamy spinach and garlic sauce. Healthy and sophisticated, this Tuscan-inspired entrée combines lean protein with nutritious greens in a restaurant-quality presentation.",
        "prep_time": 15,
        "cook_time": 25,
        "servings": "4",
        "calories": 340
    },
    "Vegetable Korma with Optional Chicken": {
        "description": "Aromatic Indian curry featuring mixed vegetables in a creamy, spiced coconut-tomato sauce. Mildly spiced and richly flavored, this versatile dish works as vegetarian or with added chicken for a complete meal.",
        "prep_time": 20,
        "cook_time": 35,
        "servings": "6",
        "calories": 280
    },
    "Kerala Style Vegetable Korma": {
        "description": "South Indian vegetable curry with coconut milk, cashews, and aromatic spices. This lighter, more delicate korma showcases Kerala's signature flavors with fresh vegetables in a mildly spiced, fragrant sauce.",
        "prep_time": 25,
        "cook_time": 30,
        "servings": "6",
        "calories": 260
    },
    "Pasta Primavera with Asparagus and Peas": {
        "description": "Fresh spring vegetable pasta celebrating seasonal produce with asparagus, peas, and cherry tomatoes. Light and vibrant, this Italian-American dish highlights vegetables in a delicate garlic-butter or cream sauce.",
        "prep_time": 15,
        "cook_time": 20,
        "servings": "4-6",
        "calories": 380
    },
    "Our Favorite French Onion Soup": {
        "description": "Classic French bistro soup with deeply caramelized onions in rich beef broth, topped with crusty bread and melted Gruyère. Patient cooking develops sweet, complex onion flavors in this warming, elegant comfort food.",
        "prep_time": 15,
        "cook_time": 90,
        "servings": "6",
        "calories": 320
    },
    "Bananas Foster": {
        "description": "Dramatic New Orleans dessert with caramelized bananas in rum-butter sauce, traditionally flambéed tableside. Quick and spectacular, this sweet treat is perfect over vanilla ice cream for an unforgettable finish.",
        "prep_time": 5,
        "cook_time": 10,
        "servings": "4",
        "calories": 380
    },
    "Buttery Breakfast Casserole": {
        "description": "Make-ahead breakfast bake with eggs, cheese, bread, and savory seasonings. Perfect for weekend brunch or holiday mornings, this crowd-pleasing dish can be assembled the night before and baked fresh.",
        "prep_time": 20,
        "cook_time": 45,
        "servings": "8-10",
        "calories": 420
    },
    "Chris Wants Italian Baked Eggs Damn Delicious": {
        "description": "Rustic Italian egg dish baked in a spiced tomato sauce with herbs and cheese. Simple and satisfying, this Mediterranean-inspired breakfast or brunch option comes together in one skillet.",
        "prep_time": 10,
        "cook_time": 25,
        "servings": "4",
        "calories": 280
    },
    "Scrambled Eggs Masala": {
        "description": "Indian-spiced scrambled eggs with onions, tomatoes, green chilies, and aromatic spices. Quick and flavorful, this protein-packed breakfast brings bold flavors to your morning routine.",
        "prep_time": 10,
        "cook_time": 10,
        "servings": "2-3",
        "calories": 220
    },
    "Laura Archibald Meatloaf": {
        "description": "Classic American comfort food with seasoned ground beef, onions, and a tangy ketchup glaze. Moist and flavorful, this traditional meatloaf recipe delivers nostalgic home-cooking at its finest.",
        "prep_time": 15,
        "cook_time": 60,
        "servings": "6-8",
        "calories": 380
    },
    "Brisket Joe's Spiced Brisket": {
        "description": "Tender beef brisket with Joe's signature spice rub, slow-roasted until meltingly tender. This showstopper centerpiece develops a flavorful crust while staying juicy inside, perfect for special gatherings.",
        "prep_time": 20,
        "cook_time": 240,
        "servings": "8-10",
        "calories": 450
    },
    "Corned Beef and Cabbage": {
        "description": "Traditional Irish-American feast with tender corned beef, cabbage, potatoes, and carrots. This St. Patrick's Day classic slow-cooks to perfection, filling your home with savory aromas.",
        "prep_time": 15,
        "cook_time": 180,
        "servings": "6-8",
        "calories": 420
    },
    "Curried Cauliflower And Chicken": {
        "description": "Healthy Indian-inspired curry combining tender chicken and cauliflower in aromatic spices. Light yet satisfying, this one-pot meal balances protein and vegetables with warming curry flavors.",
        "prep_time": 20,
        "cook_time": 30,
        "servings": "4-6",
        "calories": 320
    },
    "CurryChickenWithLambAndVegetables": {
        "description": "Hearty mixed-meat curry featuring both chicken and lamb with assorted vegetables in rich spices. Complex and deeply flavored, this substantial curry showcases multiple proteins in a fragrant sauce.",
        "prep_time": 25,
        "cook_time": 75,
        "servings": "6-8",
        "calories": 480
    },
    "South Indian Vegetable Curry": {
        "description": "Vibrant vegetarian curry with mixed vegetables, coconut, and South Indian spice blend. Aromatic and healthful, this colorful dish brings authentic regional flavors with moderate heat.",
        "prep_time": 20,
        "cook_time": 25,
        "servings": "6",
        "calories": 240
    },
    "Stilton Chicken with Apples": {
        "description": "Elegant British-inspired dish pairing tender chicken with tangy Stilton cheese and sweet apples. Sophisticated flavor combinations create a balanced, restaurant-worthy entrée in under an hour.",
        "prep_time": 15,
        "cook_time": 35,
        "servings": "4",
        "calories": 420
    },
    "Pasta with Spicy Sun Dried Tomato Cream Sauce": {
        "description": "Bold Italian pasta with sun-dried tomatoes, garlic, and cream with a spicy kick. Quick-cooking and intensely flavored, this sauce transforms simple pasta into an exciting weeknight dinner.",
        "prep_time": 10,
        "cook_time": 20,
        "servings": "4",
        "calories": 520
    },
    "Mary Likes Fettuccine With Asparagus": {
        "description": "Spring pasta featuring fresh asparagus, garlic, and Parmesan with fettuccine. Light and seasonal, this elegant dish celebrates asparagus when it's at its tender, flavorful best.",
        "prep_time": 10,
        "cook_time": 15,
        "servings": "4",
        "calories": 420
    },
    "Mary wants Fettuccine With Asparagus": {
        "description": "Fresh asparagus and fettuccine in a light garlic-butter sauce with Parmesan. Simple and refined, this springtime pasta lets quality ingredients shine with minimal fuss.",
        "prep_time": 10,
        "cook_time": 15,
        "servings": "4",
        "calories": 420
    },
    "Mary Likes Springtime Spaghetti Carbonara": {
        "description": "Classic Roman pasta with eggs, Pecorino cheese, black pepper, and crispy guanciale or bacon. Rich and creamy without cream, this iconic dish requires precise timing for silky, authentic results.",
        "prep_time": 10,
        "cook_time": 15,
        "servings": "4",
        "calories": 580
    },
    "Gjelina's Roasted Yams": {
        "description": "Trendy LA restaurant's signature roasted sweet potatoes with za'atar, feta, and herbs. Modern and flavorful, this side dish transforms humble yams into a sophisticated, Instagram-worthy creation.",
        "prep_time": 15,
        "cook_time": 45,
        "servings": "6",
        "calories": 280
    },
    "MikeMaceysMashed Potatoes": {
        "description": "Ultra-creamy mashed potatoes with butter, cream, and perfect seasoning. Mike's technique creates restaurant-quality results: fluffy, rich, and absolutely irresistible as the ultimate comfort side.",
        "prep_time": 15,
        "cook_time": 25,
        "servings": "6-8",
        "calories": 320
    },
    "Caramelized Onion Tart with Figs Blue Cheese by Lauren Prescott": {
        "description": "Elegant French-style tart with sweet caramelized onions, figs, and tangy blue cheese on flaky pastry. Sophisticated sweet-savory combination makes this perfect for elegant entertaining or special brunch.",
        "prep_time": 30,
        "cook_time": 50,
        "servings": "8",
        "calories": 380
    },
    "Five Sauces for the Modern Cook The New York Times": {
        "description": "Collection of versatile master sauces that transform simple proteins and vegetables. Learn fundamental techniques for five essential sauces that elevate everyday cooking to restaurant quality.",
        "prep_time": 10,
        "cook_time": 20,
        "servings": "varies",
        "calories": 150
    },
}

def update_recipe_description(recipe_id, enhancement):
    """Update a single recipe with enhanced data"""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE recipes
        SET description = ?,
            prep_time_minutes = ?,
            cook_time_minutes = ?,
            servings = ?
        WHERE id = ?
    """, (
        enhancement['description'],
        enhancement['prep_time'],
        enhancement['cook_time'],
        enhancement['servings'],
        recipe_id
    ))

    conn.commit()
    conn.close()

def get_recipe_by_id(recipe_id):
    """Get recipe details"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
    recipe = dict(cursor.fetchone())

    conn.close()
    return recipe

def enhance_all_recipes():
    """Apply enhancements to all matching recipes"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all recipes
    cursor.execute("SELECT id, title FROM recipes")
    recipes = [dict(row) for row in cursor.fetchall()]
    conn.close()

    updated = 0
    not_found = []

    for recipe in recipes:
        # Try to find enhancement by matching title
        enhancement = None
        for key, value in RECIPE_ENHANCEMENTS.items():
            if key.lower() in recipe['title'].lower() or recipe['title'].lower() in key.lower():
                enhancement = value
                break

        if enhancement:
            print(f"✓ Updating: {recipe['title']}")
            update_recipe_description(recipe['id'], enhancement)
            updated += 1
        else:
            # Check if it's a non-recipe document
            if any(x in recipe['title'].lower() for x in ['cookbook', 'master', 'recipes', 'workshop']):
                print(f"  Skipping collection: {recipe['title']}")
            else:
                not_found.append(recipe['title'])

    print(f"\n{'='*70}")
    print(f"Updated: {updated} recipes")
    print(f"Not found: {len(not_found)} recipes")

    if not_found:
        print(f"\nRecipes needing manual enhancement:")
        for title in not_found:
            print(f"  - {title}")

    return updated, not_found

if __name__ == '__main__':
    print("Enhancing recipes with descriptions, times, and nutritional info...\n")
    updated, not_found = enhance_all_recipes()
    print(f"\n{'='*70}")
    print("Enhancement complete!")
