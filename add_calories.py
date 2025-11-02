#!/usr/bin/env python3
"""Add calorie information to all recipes"""

import sqlite3

CALORIES = {
    "Bananas Foster": 380,
    "Beef Bourguignon": 520,
    "Beef Bourguignon Joe's": 540,
    "Beef Stroganoff": 450,
    "Brisket Joe's Spiced Brisket": 450,
    "Buttery Breakfast Casserole": 420,
    "Caramelized Onion Tart with Figs Blue Cheese by Lauren Prescott": 380,
    "Chicken Florentine": 340,
    "Chicken Piccata: Pan Fried Breaded Chicken Cutlets with Lemon & Caper Sauce – Homemade Italian Cooki": 380,
    "Chris Wants Italian Baked Eggs Damn Delicious": 280,
    "Corned Beef and Cabbage": 420,
    "Curried Cauliflower And Chicken": 320,
    "CurryChickenWithLambAndVegetables": 480,
    "Eggplant Parm": 425,
    "Five Sauces for the Modern Cook The New York Times": 150,
    "Gjelina's Roasted Yams": 280,
    "Kerala Style Vegetable Korma": 260,
    "Laura Archibald Meatloaf": 380,
    "Mary Likes Fettuccine With Asparagus": 420,
    "Mary Likes Springtime Spaghetti Carbonara": 580,
    "Mary wants Fettuccine With Asparagus": 420,
    "Mary's Favorite Fettuccine Alfredo": 650,
    "MikeMaceysMashed Potatoes": 320,
    "Mueller's Classic Lasagna": 480,
    "Our Favorite French Onion Soup": 320,
    "Pasta Primavera with Asparagus and Peas": 380,
    "Pasta with Spicy Sun Dried Tomato Cream Sauce": 520,
    "Scrambled Eggs Masala": 220,
    "South Indian Vegetable Curry": 240,
    "Stilton Chicken with Apples": 420,
    "Vegetable Korma with Optional Chicken": 280,
}

def update_calories():
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM recipes")
    recipes = cursor.fetchall()

    updated = 0
    for recipe_id, title in recipes:
        for key, calories in CALORIES.items():
            if key.lower() in title.lower() or title.lower() in key.lower():
                cursor.execute(
                    "UPDATE recipes SET calories_per_serving = ? WHERE id = ?",
                    (calories, recipe_id)
                )
                print(f"✓ {title}: {calories} cal/serving")
                updated += 1
                break

    conn.commit()
    conn.close()
    print(f"\nUpdated {updated} recipes with calorie information")

if __name__ == '__main__':
    update_calories()
