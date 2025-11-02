#!/usr/bin/env python3
"""
Enhance recipe instructions by adding ingredient quantities inline
Example: "Add the onions" -> "Add the onions (2 large, diced)"
"""

import sqlite3
import re
from difflib import SequenceMatcher

def get_all_recipes():
    """Get all recipes with ingredients and instructions"""
    conn = sqlite3.connect('recipes.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT id, title FROM recipes WHERE source_attribution != 'Janet' OR source_attribution IS NULL")
    recipes = [dict(row) for row in cursor.fetchall()]

    for recipe in recipes:
        # Get ingredients
        cursor.execute("""
            SELECT id, quantity, unit, ingredient_name, preparation
            FROM ingredients
            WHERE recipe_id = ?
            ORDER BY id
        """, (recipe['id'],))
        recipe['ingredients'] = [dict(row) for row in cursor.fetchall()]

        # Get instructions
        cursor.execute("""
            SELECT id, step_number, instruction_text
            FROM instructions
            WHERE recipe_id = ?
            ORDER BY step_number
        """, (recipe['id'],))
        recipe['instructions'] = [dict(row) for row in cursor.fetchall()]

    conn.close()
    return recipes

def similarity(a, b):
    """Calculate similarity between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_ingredient_in_text(text, ingredient_name):
    """Check if ingredient is mentioned in instruction text"""
    text_lower = text.lower()
    ing_lower = ingredient_name.lower()

    # Direct match
    if ing_lower in text_lower:
        return True

    # Try key words from ingredient name
    key_words = ing_lower.split()
    for word in key_words:
        if len(word) > 3 and word in text_lower:
            return True

    return False

def format_ingredient_quantity(ingredient):
    """Format ingredient quantity for inline display"""
    parts = []

    if ingredient['quantity']:
        parts.append(str(ingredient['quantity']))

    if ingredient['unit']:
        parts.append(ingredient['unit'])

    result = ' '.join(parts)

    # Add ingredient name if we only have quantity/unit
    if result and ingredient['ingredient_name']:
        result = f"{result} {ingredient['ingredient_name']}"
    elif ingredient['ingredient_name']:
        result = ingredient['ingredient_name']

    if ingredient['preparation']:
        result = f"{result}, {ingredient['preparation']}"

    return result

def enhance_instruction(instruction_text, ingredients):
    """Enhance a single instruction with ingredient quantities"""
    enhanced = instruction_text
    flags = []

    # Find ingredients mentioned in this step
    mentioned_ingredients = []
    for ing in ingredients:
        if ing['ingredient_name'] and find_ingredient_in_text(instruction_text, ing['ingredient_name']):
            mentioned_ingredients.append(ing)

    # For each mentioned ingredient, try to add quantity inline
    for ing in mentioned_ingredients:
        ing_name = ing['ingredient_name'].lower()
        key_words = ing_name.split()

        # Find the best match in the text
        text_lower = enhanced.lower()

        # Try to find the ingredient reference
        for word in key_words:
            if len(word) > 3:  # Skip short words like "the", "and"
                # Look for patterns like "the onions", "add garlic", etc.
                patterns = [
                    f"the {word}",
                    f"add {word}",
                    f"with {word}",
                    f"{word} to",
                    word
                ]

                for pattern in patterns:
                    if pattern in text_lower:
                        # Found it! Now add the quantity
                        quantity_str = format_ingredient_quantity(ing)

                        # Create the enhanced version
                        # Find the exact position in the original text
                        idx = text_lower.find(pattern)
                        if idx != -1:
                            # Check if we haven't already enhanced this spot
                            if '(' not in enhanced[max(0, idx-10):idx+len(pattern)+10]:
                                # Insert quantity after the ingredient mention
                                before = enhanced[:idx+len(pattern)]
                                after = enhanced[idx+len(pattern):]
                                enhanced = f"{before} ({quantity_str}){after}"
                                text_lower = enhanced.lower()
                                break

                break  # Only enhance once per ingredient

    # Flag if the instruction seems incomplete
    if len(enhanced) < 20 or 'needs review' in enhanced.lower():
        flags.append('SHORT_INSTRUCTION')

    return enhanced, flags

def update_instruction(instruction_id, new_text):
    """Update instruction in database"""
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE instructions
        SET instruction_text = ?
        WHERE id = ?
    """, (new_text, instruction_id))

    conn.commit()
    conn.close()

def enhance_all_instructions():
    """Process all recipes and enhance instructions"""
    recipes = get_all_recipes()

    total_instructions = 0
    enhanced_instructions = 0
    flagged_recipes = []

    print("Enhancing instructions with inline ingredient quantities...\n")

    for recipe in recipes:
        if not recipe['ingredients'] or not recipe['instructions']:
            continue

        print(f"Processing: {recipe['title']}")
        recipe_flags = []

        for inst in recipe['instructions']:
            total_instructions += 1
            original = inst['instruction_text']
            enhanced, flags = enhance_instruction(original, recipe['ingredients'])

            if enhanced != original:
                enhanced_instructions += 1
                print(f"  ✓ Step {inst['step_number']}: Enhanced")
                # Update in database
                update_instruction(inst['id'], enhanced)

            if flags:
                recipe_flags.extend(flags)

        if recipe_flags:
            flagged_recipes.append((recipe['title'], recipe_flags))

        print()

    print(f"{'='*70}")
    print(f"Total instructions processed: {total_instructions}")
    print(f"Instructions enhanced: {enhanced_instructions}")
    print(f"Recipes flagged for review: {len(flagged_recipes)}")

    if flagged_recipes:
        print(f"\n{'='*70}")
        print("Recipes flagged for manual review:")
        for title, flags in flagged_recipes:
            print(f"  - {title}: {', '.join(set(flags))}")

    return total_instructions, enhanced_instructions

if __name__ == '__main__':
    total, enhanced = enhance_all_instructions()
    print(f"\n{'='*70}")
    print("Instruction enhancement complete!")
    print(f"Enhanced {enhanced} out of {total} instructions")
