#!/usr/bin/env python3
"""
Script to reformat recipe instructions to explicitly list ingredients
instead of using indirect references like "first 5 ingredients".
"""

import sqlite3
import re
from typing import List, Dict, Tuple

def get_recipe_ingredients(cursor, recipe_id: int) -> List[Dict]:
    """Get all ingredients for a recipe in order."""
    cursor.execute("""
        SELECT ingredient_order, quantity, unit, ingredient_name, preparation
        FROM ingredients
        WHERE recipe_id = ?
        ORDER BY ingredient_order
    """, (recipe_id,))

    ingredients = []
    for row in cursor.fetchall():
        order, quantity, unit, name, prep = row
        ingredients.append({
            'order': order,
            'quantity': quantity,
            'unit': unit,
            'name': name,
            'preparation': prep
        })
    return ingredients

def format_ingredient(ing: Dict) -> str:
    """Format a single ingredient as a readable string."""
    parts = []

    if ing['quantity']:
        parts.append(ing['quantity'])
    if ing['unit']:
        parts.append(ing['unit'])

    parts.append(ing['name'])

    if ing['preparation']:
        parts.append(f"({ing['preparation']})")

    return ' '.join(parts)

def format_ingredient_list(ingredients: List[Dict]) -> str:
    """Format a list of ingredients as a comma-separated string."""
    if not ingredients:
        return ""

    formatted = [format_ingredient(ing) for ing in ingredients]

    if len(formatted) == 1:
        return formatted[0]
    elif len(formatted) == 2:
        return f"{formatted[0]} and {formatted[1]}"
    else:
        return ', '.join(formatted[:-1]) + f", and {formatted[-1]}"

def replace_ingredient_references(instruction: str, all_ingredients: List[Dict]) -> str:
    """Replace indirect ingredient references with explicit lists."""

    # Pattern: "first X ingredients" or "first X items"
    pattern1 = r'\b(first|next|last)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(ingredient|item)s?\b'

    # Pattern: "all ingredients"
    pattern2 = r'\ball\s+ingredients\b'

    # Pattern: "remaining ingredients"
    pattern3 = r'\bremaining\s+ingredients?\b'

    # Pattern: "areas X ingredients" (typo in database)
    pattern4 = r'\bareas?\s+(\d+)\s+ingredients?\b'

    # Convert word numbers to integers
    word_to_num = {
        'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
        'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10
    }

    modified = instruction

    # Handle "first/next/last X ingredients"
    matches = list(re.finditer(pattern1, instruction, re.IGNORECASE))
    for match in reversed(matches):  # Process in reverse to maintain positions
        position = match.group(1).lower()
        count_str = match.group(2).lower()

        # Convert to number
        if count_str.isdigit():
            count = int(count_str)
        else:
            count = word_to_num.get(count_str, 0)

        if count > 0 and count <= len(all_ingredients):
            if position == 'first':
                selected = all_ingredients[:count]
            elif position == 'last':
                selected = all_ingredients[-count:]
            else:  # 'next' - this is tricky, we'll assume it means the first X for now
                selected = all_ingredients[:count]

            replacement = format_ingredient_list(selected)
            modified = modified[:match.start()] + replacement + modified[match.end():]

    # Handle "areas X ingredients" (typo)
    matches = list(re.finditer(pattern4, instruction, re.IGNORECASE))
    for match in reversed(matches):
        count = int(match.group(1))
        if count > 0 and count <= len(all_ingredients):
            # This seems to be referring to "next" ingredients
            selected = all_ingredients[:count]
            replacement = format_ingredient_list(selected)
            modified = modified[:match.start()] + replacement + modified[match.end():]

    # Handle "all ingredients"
    if re.search(pattern2, modified, re.IGNORECASE):
        replacement = format_ingredient_list(all_ingredients)
        modified = re.sub(pattern2, replacement, modified, flags=re.IGNORECASE)

    # Handle "remaining ingredients"
    # This is context-dependent, so we'll just replace with all ingredients
    if re.search(pattern3, modified, re.IGNORECASE):
        replacement = format_ingredient_list(all_ingredients)
        modified = re.sub(pattern3, replacement, modified, flags=re.IGNORECASE)

    return modified

def analyze_instructions(db_path: str) -> List[Tuple[int, int, str]]:
    """Analyze instructions and find those with indirect references."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all instructions
    cursor.execute("""
        SELECT i.id, i.recipe_id, i.step_number, i.instruction_text, r.title
        FROM instructions i
        JOIN recipes r ON i.recipe_id = r.id
        ORDER BY i.recipe_id, i.step_number
    """)

    patterns = [
        r'\b(first|next|last)\s+(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s+(ingredient|item)s?\b',
        r'\ball\s+ingredients\b',
        r'\bremaining\s+ingredients?\b',
        r'\bareas?\s+(\d+)\s+ingredients?\b'
    ]

    found = []
    for row in cursor.fetchall():
        inst_id, recipe_id, step_num, text, title = row
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                found.append((inst_id, recipe_id, step_num, text, title))
                break

    conn.close()
    return found

def update_instructions(db_path: str, dry_run: bool = True):
    """Update all instructions to use explicit ingredient lists."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get all instructions with their recipe info
    cursor.execute("""
        SELECT i.id, i.recipe_id, i.step_number, i.instruction_text, r.title
        FROM instructions i
        JOIN recipes r ON i.recipe_id = r.id
        ORDER BY i.recipe_id, i.step_number
    """)

    instructions = cursor.fetchall()
    updates = []

    for inst_id, recipe_id, step_num, text, title in instructions:
        # Get ingredients for this recipe
        ingredients = get_recipe_ingredients(cursor, recipe_id)

        # Replace references
        new_text = replace_ingredient_references(text, ingredients)

        if new_text != text:
            updates.append({
                'id': inst_id,
                'recipe_id': recipe_id,
                'recipe_title': title,
                'step_number': step_num,
                'old_text': text,
                'new_text': new_text
            })

    print(f"\nFound {len(updates)} instructions to update:")
    print("=" * 80)

    for update in updates:
        print(f"\nRecipe: {update['recipe_title']} (ID: {update['recipe_id']})")
        print(f"Step {update['step_number']}:")
        print(f"OLD: {update['old_text']}")
        print(f"NEW: {update['new_text']}")
        print("-" * 80)

    if not dry_run:
        print(f"\nUpdating {len(updates)} instructions...")
        for update in updates:
            cursor.execute("""
                UPDATE instructions
                SET instruction_text = ?
                WHERE id = ?
            """, (update['new_text'], update['id']))

        conn.commit()
        print(f"✓ Updated {len(updates)} instructions successfully!")
    else:
        print("\n[DRY RUN] No changes made. Run with --execute to apply changes.")

    conn.close()
    return len(updates)

if __name__ == "__main__":
    import sys

    db_path = "recipes.db"

    # Check if --execute flag is provided
    execute = "--execute" in sys.argv

    print("=" * 80)
    print("Recipe Instruction Reformatter")
    print("=" * 80)

    if execute:
        print("\n⚠️  EXECUTION MODE - Will modify database!")
    else:
        print("\n📋 DRY RUN MODE - No changes will be made")
        print("Add --execute flag to apply changes")

    count = update_instructions(db_path, dry_run=not execute)

    print("\n" + "=" * 80)
    print(f"Complete! {count} instruction(s) processed.")
    if not execute and count > 0:
        print("\nTo apply these changes, run: python3 reformat_instructions.py --execute")
    print("=" * 80)
