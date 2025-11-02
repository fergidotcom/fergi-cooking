"""
Recipe extraction module - extracts recipe data from various file formats
"""

import os
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import subprocess

# PDF extraction
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("PDF libraries not installed. Run: pip install PyPDF2 pdfplumber")

# Image/OCR
try:
    from PIL import Image
    import pytesseract
except ImportError:
    print("Image/OCR libraries not installed. Run: pip install Pillow pytesseract")


class RecipeExtractor:
    """Extract recipe information from various file formats"""

    def __init__(self):
        self.supported_formats = ['.pdf', '.pages', '.jpg', '.jpeg', '.png', '.gif']

    def extract_from_file(self, file_path: str) -> Dict:
        """
        Main extraction method - routes to appropriate extractor based on file type
        """
        file_ext = Path(file_path).suffix.lower()
        filename = Path(file_path).name

        recipe_data = {
            'title': self._clean_filename(filename),
            'original_filename': filename,
            'file_path': file_path,
            'source_attribution': self._detect_source_from_filename(filename),
            'ingredients': [],
            'instructions': [],
            'tags': [],
            'images': []
        }

        try:
            if file_ext == '.pdf':
                text = self._extract_from_pdf(file_path)
            elif file_ext == '.pages':
                text = self._extract_from_pages(file_path)
            elif file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
                text = self._extract_from_image(file_path)
                recipe_data['images'].append(file_path)
            else:
                print(f"Unsupported file format: {file_ext}")
                return recipe_data

            # Parse the extracted text
            parsed = self._parse_recipe_text(text)
            recipe_data.update(parsed)

            # Enhance with filename-based metadata
            metadata = self._extract_metadata_from_filename(filename)
            recipe_data.update(metadata)

        except Exception as e:
            print(f"Error extracting from {file_path}: {str(e)}")
            recipe_data['notes'] = f"Extraction error: {str(e)}"

        return recipe_data

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""

        try:
            # Try pdfplumber first (better for structured PDFs)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            print(f"pdfplumber failed for {file_path}, trying PyPDF2: {str(e)}")

            # Fallback to PyPDF2
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n\n"
            except Exception as e2:
                print(f"PyPDF2 also failed: {str(e2)}")
                text = f"[Error extracting PDF: {str(e2)}]"

        return text

    def _extract_from_pages(self, file_path: str) -> str:
        """
        Extract text from Apple Pages document
        Strategy: Convert to PDF first, then extract
        """
        try:
            # Pages files are actually zip packages
            # Try to convert using macOS command-line tools if available
            pdf_path = file_path.replace('.pages', '_converted.pdf')

            # Use macOS textutil if available
            result = subprocess.run(
                ['textutil', '-convert', 'txt', '-stdout', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return result.stdout
            else:
                # Try alternative: use sips/convert to PDF then extract
                # This is a placeholder - Pages extraction is complex
                return f"[Pages document: {Path(file_path).name}]\n[Manual review recommended]"

        except Exception as e:
            print(f"Error extracting Pages document: {str(e)}")
            return f"[Pages extraction error: {str(e)}]"

    def _extract_from_image(self, file_path: str) -> str:
        """Extract text from image using OCR"""
        try:
            image = Image.open(file_path)

            # Perform OCR
            text = pytesseract.image_to_string(image)

            return text
        except Exception as e:
            print(f"Error performing OCR on {file_path}: {str(e)}")
            return f"[OCR error: {str(e)}]"

    def _parse_recipe_text(self, text: str) -> Dict:
        """
        Parse recipe text to extract structured data
        This is a heuristic parser - not perfect but handles common formats
        """
        result = {
            'description': '',
            'ingredients': [],
            'instructions': [],
            'prep_time_minutes': None,
            'cook_time_minutes': None,
            'total_time_minutes': None,
            'servings': None,
            'tags': []
        }

        if not text or len(text.strip()) < 20:
            return result

        lines = text.split('\n')

        # Extract times
        time_pattern = r'(\d+)\s*(hour|hr|minute|min)'
        prep_match = re.search(r'prep\s*time[:\s]*' + time_pattern, text, re.IGNORECASE)
        cook_match = re.search(r'cook\s*time[:\s]*' + time_pattern, text, re.IGNORECASE)
        total_match = re.search(r'total\s*time[:\s]*' + time_pattern, text, re.IGNORECASE)

        if prep_match:
            result['prep_time_minutes'] = self._parse_time_to_minutes(prep_match.group(1), prep_match.group(2))
        if cook_match:
            result['cook_time_minutes'] = self._parse_time_to_minutes(cook_match.group(1), cook_match.group(2))
        if total_match:
            result['total_time_minutes'] = self._parse_time_to_minutes(total_match.group(1), total_match.group(2))

        # Extract servings
        servings_match = re.search(r'(?:serves|servings|yield)[:\s]*(\d+(?:-\d+)?(?:\s*to\s*\d+)?)', text, re.IGNORECASE)
        if servings_match:
            result['servings'] = servings_match.group(1)

        # Find ingredient section
        ingredient_start = -1
        instruction_start = -1

        for idx, line in enumerate(lines):
            line_lower = line.lower().strip()
            if re.match(r'^ingredients?:?$', line_lower) or 'ingredients' in line_lower[:30]:
                ingredient_start = idx
            elif any(keyword in line_lower for keyword in ['instructions', 'directions', 'preparation', 'method', 'steps']):
                instruction_start = idx
                break

        # Extract ingredients
        if ingredient_start >= 0:
            section_end = instruction_start if instruction_start > ingredient_start else len(lines)
            for line in lines[ingredient_start + 1:section_end]:
                ingredient = self._parse_ingredient_line(line.strip())
                if ingredient:
                    result['ingredients'].append(ingredient)

        # Extract instructions
        if instruction_start >= 0:
            instruction_lines = []
            for line in lines[instruction_start + 1:]:
                line = line.strip()
                if line and len(line) > 10:  # Ignore very short lines
                    instruction_lines.append(line)

            # Group into steps
            result['instructions'] = self._parse_instructions(instruction_lines)

        # Extract description (first substantial paragraph)
        description_lines = []
        for line in lines[:min(20, len(lines))]:
            line = line.strip()
            if len(line) > 30 and not any(keyword in line.lower() for keyword in ['ingredient', 'instruction', 'prep time', 'cook time']):
                description_lines.append(line)
                if len(' '.join(description_lines)) > 200:
                    break

        result['description'] = ' '.join(description_lines)[:500]

        return result

    def _parse_ingredient_line(self, line: str) -> Optional[Dict]:
        """Parse a single ingredient line"""
        if not line or len(line) < 3:
            return None

        # Skip section headers
        if line.lower() in ['ingredients', 'for the sauce', 'for the filling']:
            return None

        # Common ingredient patterns
        # Examples: "2 cups flour", "1/2 tsp salt", "3-4 large eggs, beaten"

        ingredient = {
            'quantity': None,
            'unit': None,
            'name': line,
            'preparation': None,
            'group': None
        }

        # Try to parse quantity and unit
        quantity_pattern = r'^([\d\/\-]+(?:\s*to\s*[\d\/\-]+)?)\s+([a-zA-Z]+)?'
        match = re.match(quantity_pattern, line)

        if match:
            ingredient['quantity'] = match.group(1)
            rest = line[match.end():].strip()

            # Common units
            units = ['cup', 'cups', 'tbsp', 'tablespoon', 'tablespoons', 'tsp', 'teaspoon', 'teaspoons',
                    'oz', 'ounce', 'ounces', 'lb', 'lbs', 'pound', 'pounds', 'g', 'gram', 'grams',
                    'kg', 'kilogram', 'kilograms', 'ml', 'milliliter', 'l', 'liter', 'pinch', 'dash']

            words = rest.split()
            if words and words[0].lower().rstrip('s') in [u.rstrip('s') for u in units]:
                ingredient['unit'] = words[0]
                rest = ' '.join(words[1:])

            # Separate preparation (comma-separated or parenthetical)
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

        return ingredient

    def _parse_instructions(self, lines: List[str]) -> List[str]:
        """Parse instruction lines into steps"""
        instructions = []
        current_step = ""

        for line in lines:
            # Check if line starts with a number (step number)
            if re.match(r'^\d+[\.\)]\s', line):
                if current_step:
                    instructions.append(current_step.strip())
                current_step = re.sub(r'^\d+[\.\)]\s', '', line)
            else:
                if current_step:
                    current_step += " " + line
                else:
                    current_step = line

        if current_step:
            instructions.append(current_step.strip())

        return instructions

    def _parse_time_to_minutes(self, value: str, unit: str) -> int:
        """Convert time string to minutes"""
        try:
            value = int(value)
            unit = unit.lower()
            if 'hour' in unit or unit == 'hr':
                return value * 60
            else:  # minutes
                return value
        except:
            return None

    def _clean_filename(self, filename: str) -> str:
        """Extract clean recipe title from filename"""
        # Remove extension
        title = Path(filename).stem

        # Remove common suffixes
        title = re.sub(r'\s*Recipe.*$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s*\|.*$', '', title)

        # Remove URLs/domains
        title = re.sub(r'https?://[^\s]+', '', title)
        title = re.sub(r'www\.[^\s]+', '', title)

        # Clean up
        title = title.replace('_', ' ').replace('-', ' ')
        title = re.sub(r'\s+', ' ', title).strip()

        return title

    def _detect_source_from_filename(self, filename: str) -> str:
        """Detect recipe source from filename"""
        filename_lower = filename.lower()

        # Check for known sources
        if 'epicurious' in filename_lower:
            return 'Epicurious'
        elif 'nyt' in filename_lower or 'new york times' in filename_lower:
            return 'NYT Cooking'
        elif "joe's" in filename_lower or 'joes' in filename_lower:
            return 'Fergi'
        elif 'fergi' in filename_lower:
            return 'Fergi'
        elif 'janet' in filename_lower or 'mason' in filename_lower:
            return 'Janet'
        elif 'adrienne' in filename_lower:
            return 'Adrienne'
        elif 'nancy' in filename_lower:
            return 'Nancy Bern'
        elif 'laura' in filename_lower:
            return 'Laura Archibald'
        elif 'irene' in filename_lower:
            return 'Irene'
        elif 'mike' in filename_lower or 'macey' in filename_lower:
            return 'Mike Macey'
        elif 'diane' in filename_lower:
            return 'Diane Locandro'
        elif 'marty' in filename_lower:
            return 'Marty'
        else:
            return 'Unknown'

    def _extract_metadata_from_filename(self, filename: str) -> Dict:
        """Extract additional metadata from filename"""
        metadata = {}

        filename_lower = filename.lower()

        # Detect cuisine types
        cuisines = {
            'italian': ['italian', 'pasta', 'lasagna', 'parmesan', 'alfredo', 'carbonara'],
            'indian': ['curry', 'korma', 'masala', 'indian'],
            'french': ['bourguignon', 'french'],
            'caribbean': ['jerk'],
            'american': ['meatloaf', 'casserole', 'barbecue']
        }

        for cuisine, keywords in cuisines.items():
            if any(keyword in filename_lower for keyword in keywords):
                metadata['cuisine_type'] = cuisine.capitalize()
                break

        # Detect meal types
        if any(word in filename_lower for word in ['breakfast', 'eggs', 'casserole']):
            metadata['meal_type'] = 'Breakfast'
        elif any(word in filename_lower for word in ['dessert', 'bananas foster', 'eggnog']):
            metadata['meal_type'] = 'Dessert'

        # Detect dietary preferences
        if any(word in filename_lower for word in ['vegetable', 'veggie', 'vegetarian']):
            metadata['vegetarian'] = 1

        return metadata


if __name__ == "__main__":
    # Test the extractor
    extractor = RecipeExtractor()
    test_file = "Beef Bourguignon Joe's Recipe.pdf"
    if os.path.exists(test_file):
        result = extractor.extract_from_file(test_file)
        print("Extracted recipe data:")
        print(f"Title: {result['title']}")
        print(f"Source: {result['source_attribution']}")
        print(f"Ingredients: {len(result['ingredients'])}")
        print(f"Instructions: {len(result['instructions'])}")
