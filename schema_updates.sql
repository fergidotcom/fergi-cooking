-- Event Management System Schema
-- Created: November 2, 2025

-- Events table
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    event_date DATE,
    event_time TIME,
    location TEXT,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Event-Recipe mapping (many-to-many)
CREATE TABLE IF NOT EXISTS event_recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    course_type TEXT CHECK(course_type IN ('appetizer', 'main', 'side', 'salad', 'dessert', 'beverage', 'other')),
    display_order INTEGER DEFAULT 0,
    notes TEXT,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Recipe variants (for recipes with options like Chicken/Filet)
CREATE TABLE IF NOT EXISTS recipe_variants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    variant_name TEXT NOT NULL,
    variant_description TEXT,
    prep_notes TEXT,
    display_order INTEGER DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Guest selections and responses
CREATE TABLE IF NOT EXISTS guest_selections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    guest_email TEXT NOT NULL,
    guest_name TEXT,
    recipe_id INTEGER,
    variant_id INTEGER,
    selection_type TEXT CHECK(selection_type IN ('prefer', 'will_bring', 'dietary_restriction', 'no_preference')),
    bringing_own_dish_name TEXT,
    bringing_own_dish_description TEXT,
    notes TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE SET NULL,
    FOREIGN KEY (variant_id) REFERENCES recipe_variants(id) ON DELETE SET NULL
);

-- Add has_variants column to recipes table
ALTER TABLE recipes ADD COLUMN has_variants BOOLEAN DEFAULT 0;

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_event_recipes_event ON event_recipes(event_id);
CREATE INDEX IF NOT EXISTS idx_event_recipes_recipe ON event_recipes(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_variants_recipe ON recipe_variants(recipe_id);
CREATE INDEX IF NOT EXISTS idx_guest_selections_event ON guest_selections(event_id);
CREATE INDEX IF NOT EXISTS idx_guest_selections_guest ON guest_selections(guest_email);
CREATE INDEX IF NOT EXISTS idx_guest_selections_recipe ON guest_selections(recipe_id);

-- Sample data: Add Rosemary Stilton Chicken/Filet recipe with variants
-- First, check if the recipe exists, if not create it
INSERT OR IGNORE INTO recipes (
    title,
    description,
    prep_time_minutes,
    cook_time_minutes,
    total_time_minutes,
    servings,
    difficulty,
    cuisine_type,
    meal_type,
    source_attribution,
    original_filename,
    file_path,
    has_variants,
    favorite
) VALUES (
    'Rosemary Stilton Chicken/Filet',
    'Rich and savory dish with fresh rosemary and stilton cheese. Available with either chicken breast or beef filet mignon - your choice! The creamy stilton sauce perfectly complements both proteins.',
    15,
    25,
    40,
    '4 servings',
    'Medium',
    'American',
    'dinner',
    'Fergi',
    'rosemary-stilton-recipe.txt',
    '/Cooking/rosemary-stilton-recipe.txt',
    1,
    1
);

-- Get the recipe ID for the Rosemary Stilton recipe
-- Add variants for this recipe
INSERT OR IGNORE INTO recipe_variants (recipe_id, variant_name, variant_description, prep_notes, display_order)
SELECT id, 'Chicken', 'Tender chicken breast', 'Use 6oz boneless, skinless chicken breasts', 1
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO recipe_variants (recipe_id, variant_name, variant_description, prep_notes, display_order)
SELECT id, 'Filet', 'Premium beef tenderloin', 'Use 8oz beef tenderloin filet mignon', 2
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

-- Add ingredients for Rosemary Stilton recipe
INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 1, '4', '', 'chicken breasts or beef filets', '6-8 oz each'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 2, '2', 'tbsp', 'fresh rosemary', 'chopped'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 3, '4', 'oz', 'stilton cheese', 'crumbled'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 4, '1', 'cup', 'heavy cream', ''
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 5, '2', 'cloves', 'garlic', 'minced'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 6, '', '', 'salt and pepper', 'to taste'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO ingredients (recipe_id, ingredient_order, quantity, unit, ingredient_name, preparation)
SELECT id, 7, '2', 'tbsp', 'olive oil', ''
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

-- Add instructions for Rosemary Stilton recipe
INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 1, 'Season the chicken breasts or beef filets with salt and pepper on both sides.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 2, 'Heat 2 tablespoons of olive oil in a large skillet over medium-high heat.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 3, 'Add the protein to the hot skillet and cook: Chicken for 6-7 minutes per side until golden and cooked through (internal temp 165°F); Filets for 4-5 minutes per side for medium-rare (internal temp 135°F). Remove from pan and set aside.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 4, 'In the same skillet, add minced garlic and cook for 30 seconds until fragrant.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 5, 'Add 1 cup of heavy cream and 2 tablespoons of chopped fresh rosemary. Bring to a gentle simmer.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 6, 'Stir in 4 ounces of crumbled stilton cheese and continue to simmer, stirring occasionally, until the cheese is melted and the sauce has thickened (about 3-4 minutes).'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 7, 'Return the cooked protein to the pan and spoon the sauce over it. Cook for another 2 minutes to heat through.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';

INSERT OR IGNORE INTO instructions (recipe_id, step_number, instruction_text)
SELECT id, 8, 'Serve immediately with the stilton-rosemary sauce spooned over the top. Pairs beautifully with roasted vegetables or mashed potatoes.'
FROM recipes WHERE title = 'Rosemary Stilton Chicken/Filet';
