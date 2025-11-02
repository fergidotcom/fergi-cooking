"""
Vision-based recipe extractor for Janet Mason's cookbook images
Uses Claude's vision capabilities to accurately extract recipe information
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional
import re


class VisionRecipeExtractor:
    """
    Extract recipe information from images using vision analysis
    This is a placeholder that will be called with actual vision results
    """

    def __init__(self):
        self.processed_recipes = {}
        self.recipe_mapping_file = "janet_recipe_mapping.json"

    def extract_from_image_analysis(self, image_path: str, vision_analysis: str) -> Dict:
        """
        Extract recipe data from vision analysis text

        Args:
            image_path: Path to the image file
            vision_analysis: Text description of what's in the image

        Returns:
            Dictionary with recipe information
        """
        filename = Path(image_path).name

        recipe_data = {
            'title': self._extract_title(vision_analysis, filename),
            'original_filename': filename,
            'file_path': image_path,
            'source_attribution': 'Janet',
            'ingredients': self._extract_ingredients(vision_analysis),
            'instructions': self._extract_instructions(vision_analysis),
            'description': self._extract_description(vision_analysis),
            'notes': f'Extracted from cookbook image: {filename}',
            'tags': ['Janet Mason', 'Cookbook'],
            'images': [image_path]
        }

        # Extract metadata
        metadata = self._extract_metadata(vision_analysis)
        recipe_data.update(metadata)

        return recipe_data

    def _extract_title(self, text: str, filename: str) -> str:
        """Extract recipe title from vision analysis"""
        # Look for common title patterns
        lines = text.split('\n')

        # Check first few lines for title-like content
        for line in lines[:10]:
            line = line.strip()
            # Skip very short lines and common headers
            if len(line) < 3 or line.lower() in ['recipe', 'ingredients', 'directions']:
                continue
            # Look for title patterns (often all caps or capitalized)
            if line.isupper() or (line[0].isupper() and len(line.split()) <= 8):
                # Clean up the title
                title = re.sub(r'^(recipe|for):\s*', '', line, flags=re.IGNORECASE)
                title = title.strip()
                if title and len(title) > 3:
                    return title

        # Fallback: use filename without extension
        return Path(filename).stem.replace('_', ' ')

    def _extract_ingredients(self, text: str) -> List[Dict]:
        """Extract ingredients from vision analysis"""
        ingredients = []

        # Find ingredient section
        in_ingredients = False
        lines = text.split('\n')

        for line in lines:
            line = line.strip()

            # Start of ingredients section
            if re.match(r'^ingredients?:?$', line, re.IGNORECASE):
                in_ingredients = True
                continue

            # End of ingredients section
            if in_ingredients and re.match(r'^(directions?|instructions?|method|preparation):?$', line, re.IGNORECASE):
                break

            # Extract ingredient
            if in_ingredients and line:
                ingredient = self._parse_ingredient_line(line)
                if ingredient:
                    ingredients.append(ingredient)

        return ingredients

    def _parse_ingredient_line(self, line: str) -> Optional[Dict]:
        """Parse a single ingredient line"""
        if not line or len(line) < 2:
            return None

        # Skip section headers
        if line.lower() in ['ingredients', 'for the sauce', 'for the filling']:
            return None

        ingredient = {
            'quantity': None,
            'unit': None,
            'name': line,
            'preparation': None
        }

        # Try to parse quantity and unit
        quantity_pattern = r'^([\d\/\-\.]+(?:\s+[\d\/]+)?(?:\s+to\s+[\d\/]+)?)\s*'
        match = re.match(quantity_pattern, line)

        if match:
            ingredient['quantity'] = match.group(1)
            rest = line[match.end():].strip()

            # Common units
            units = ['cup', 'cups', 'tablespoon', 'tablespoons', 'tbsp', 'tsp', 'teaspoon', 'teaspoons',
                    'ounce', 'ounces', 'oz', 'pound', 'pounds', 'lb', 'lbs', 'gram', 'grams', 'g',
                    'kilogram', 'kg', 'ml', 'liter', 'l', 'pinch', 'dash', 'clove', 'cloves', 'can', 'cans']

            words = rest.split()
            if words and words[0].lower().rstrip('s.') in [u.rstrip('s.') for u in units]:
                ingredient['unit'] = words[0]
                rest = ' '.join(words[1:])

            # Separate name and preparation
            if ',' in rest:
                parts = rest.split(',', 1)
                ingredient['name'] = parts[0].strip()
                ingredient['preparation'] = parts[1].strip()
            elif '(' in rest:
                parts = rest.split('(', 1)
                ingredient['name'] = parts[0].strip()
                ingredient['preparation'] = parts[1].replace(')', '').strip()
            else:
                ingredient['name'] = rest

        return ingredient if ingredient['name'] else None

    def _extract_instructions(self, text: str) -> List[str]:
        """Extract cooking instructions from vision analysis"""
        instructions = []

        # Find instructions section
        in_instructions = False
        lines = text.split('\n')
        current_step = ""

        for line in lines:
            line = line.strip()

            # Start of instructions
            if re.match(r'^(directions?|instructions?|method|preparation|steps):?$', line, re.IGNORECASE):
                in_instructions = True
                continue

            # Process instruction lines
            if in_instructions and line:
                # Check if line starts with step number
                if re.match(r'^\d+[\.\)]\s', line):
                    if current_step:
                        instructions.append(current_step.strip())
                    current_step = re.sub(r'^\d+[\.\)]\s', '', line)
                elif current_step:
                    current_step += " " + line
                else:
                    current_step = line

        # Add final step
        if current_step:
            instructions.append(current_step.strip())

        return instructions

    def _extract_description(self, text: str) -> str:
        """Extract recipe description"""
        # Look for descriptive text before ingredients
        lines = text.split('\n')
        description_lines = []

        for line in lines:
            line = line.strip()
            # Stop at ingredients section
            if re.match(r'^ingredients?:?$', line, re.IGNORECASE):
                break
            # Collect substantial lines
            if len(line) > 30 and not line.isupper():
                description_lines.append(line)
                if len(' '.join(description_lines)) > 200:
                    break

        return ' '.join(description_lines)[:500] if description_lines else ''

    def _extract_metadata(self, text: str) -> Dict:
        """Extract metadata like servings, times, etc."""
        metadata = {}

        # Extract servings
        servings_match = re.search(r'(?:serves|servings|yield)[:\s]*(\d+(?:-\d+)?)', text, re.IGNORECASE)
        if servings_match:
            metadata['servings'] = servings_match.group(1)

        # Extract prep time
        prep_match = re.search(r'prep(?:aration)?\s*time[:\s]*(\d+)\s*(hour|hr|minute|min)', text, re.IGNORECASE)
        if prep_match:
            value = int(prep_match.group(1))
            unit = prep_match.group(2).lower()
            metadata['prep_time_minutes'] = value * 60 if 'hour' in unit or unit == 'hr' else value

        # Extract cook time
        cook_match = re.search(r'cook(?:ing)?\s*time[:\s]*(\d+)\s*(hour|hr|minute|min)', text, re.IGNORECASE)
        if cook_match:
            value = int(cook_match.group(1))
            unit = cook_match.group(2).lower()
            metadata['cook_time_minutes'] = value * 60 if 'hour' in unit or unit == 'hr' else value

        return metadata

    def save_mapping(self, image_file: str, recipe_data: Dict):
        """Save the image-to-recipe mapping"""
        if os.path.exists(self.recipe_mapping_file):
            with open(self.recipe_mapping_file, 'r') as f:
                mapping = json.load(f)
        else:
            mapping = {}

        mapping[image_file] = {
            'title': recipe_data['title'],
            'extracted': True
        }

        with open(self.recipe_mapping_file, 'w') as f:
            json.dump(mapping, f, indent=2)

    def load_mapping(self) -> Dict:
        """Load existing mapping"""
        if os.path.exists(self.recipe_mapping_file):
            with open(self.recipe_mapping_file, 'r') as f:
                return json.load(f)
        return {}


# Manual mapping for Janet Mason recipes (to be filled in by vision analysis)
JANET_RECIPE_TITLES = {
    'IMG_8111.JPG': 'Baking Powder Biscuits',
    'IMG_8112.JPG': 'Mango and Roasted Corn Salsa',
    'IMG_8113.JPG': 'Spinach Artichoke Dip',
    'IMG_8114.JPG': 'Fresh Tomato Bruschetta',
    'IMG_8115.JPG': 'Chinese Spring Rolls',
    'IMG_8120.JPG': 'Party Mix',
    # More to be added as analyzed
}


def get_recipe_title_from_filename(filename: str) -> str:
    """Get recipe title from manual mapping or generate from filename"""
    if filename in JANET_RECIPE_TITLES:
        return JANET_RECIPE_TITLES[filename]
    else:
        # Generate from filename
        return Path(filename).stem.replace('_', ' ')


if __name__ == "__main__":
    extractor = VisionRecipeExtractor()
    print("Vision-based recipe extractor ready")
    print(f"Known recipe mappings: {len(JANET_RECIPE_TITLES)}")
