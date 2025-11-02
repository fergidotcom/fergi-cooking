-- Recipe Database Schema
-- Normalized database for recipe management system

-- Main recipes table
CREATE TABLE IF NOT EXISTS recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    prep_time_minutes INTEGER,
    cook_time_minutes INTEGER,
    total_time_minutes INTEGER,
    servings TEXT,
    difficulty TEXT CHECK(difficulty IN ('Easy', 'Medium', 'Hard', 'Unknown')),
    cuisine_type TEXT,
    meal_type TEXT, -- breakfast, lunch, dinner, dessert, snack, etc.
    source_attribution TEXT, -- e.g., "Janet", "Fergi", "NYT Cooking", "Epicurious"
    source_url TEXT,
    original_filename TEXT NOT NULL,
    file_path TEXT NOT NULL,
    date_added DATETIME DEFAULT CURRENT_TIMESTAMP,
    date_modified DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    rating INTEGER CHECK(rating >= 0 AND rating <= 5),
    favorite BOOLEAN DEFAULT 0,
    vegetarian BOOLEAN DEFAULT 0,
    vegan BOOLEAN DEFAULT 0,
    gluten_free BOOLEAN DEFAULT 0,
    dairy_free BOOLEAN DEFAULT 0
);

-- Ingredients table
CREATE TABLE IF NOT EXISTS ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    ingredient_order INTEGER NOT NULL, -- to maintain order
    quantity TEXT, -- e.g., "2", "1/2", "1-2"
    unit TEXT, -- e.g., "cup", "tbsp", "oz"
    ingredient_name TEXT NOT NULL,
    preparation TEXT, -- e.g., "chopped", "diced", "minced"
    ingredient_group TEXT, -- e.g., "For the sauce", "For the topping"
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Instructions table
CREATE TABLE IF NOT EXISTS instructions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    step_number INTEGER NOT NULL,
    instruction_text TEXT NOT NULL,
    instruction_group TEXT, -- e.g., "Prepare the vegetables", "Make the sauce"
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Tags table for flexible categorization
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT UNIQUE NOT NULL
);

-- Recipe-Tags junction table (many-to-many)
CREATE TABLE IF NOT EXISTS recipe_tags (
    recipe_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (recipe_id, tag_id),
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Cooking history/notes
CREATE TABLE IF NOT EXISTS cooking_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    date_cooked DATETIME DEFAULT CURRENT_TIMESTAMP,
    rating INTEGER CHECK(rating >= 0 AND rating <= 5),
    notes TEXT,
    modifications TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Images table for recipe photos
CREATE TABLE IF NOT EXISTS recipe_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    image_path TEXT NOT NULL,
    image_type TEXT CHECK(image_type IN ('original', 'thumbnail', 'step')),
    caption TEXT,
    display_order INTEGER DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Full-text search virtual table for recipes
CREATE VIRTUAL TABLE IF NOT EXISTS recipes_fts USING fts5(
    title,
    description,
    ingredients_text,
    instructions_text,
    tags_text,
    content=recipes
);

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_recipes_title ON recipes(title);
CREATE INDEX IF NOT EXISTS idx_recipes_source ON recipes(source_attribution);
CREATE INDEX IF NOT EXISTS idx_recipes_cuisine ON recipes(cuisine_type);
CREATE INDEX IF NOT EXISTS idx_recipes_meal_type ON recipes(meal_type);
CREATE INDEX IF NOT EXISTS idx_recipes_favorite ON recipes(favorite);
CREATE INDEX IF NOT EXISTS idx_recipes_rating ON recipes(rating);
CREATE INDEX IF NOT EXISTS idx_ingredients_recipe ON ingredients(recipe_id);
CREATE INDEX IF NOT EXISTS idx_instructions_recipe ON instructions(recipe_id);
CREATE INDEX IF NOT EXISTS idx_cooking_log_recipe ON cooking_log(recipe_id);
CREATE INDEX IF NOT EXISTS idx_recipe_images_recipe ON recipe_images(recipe_id);

-- Triggers to update modified timestamp
CREATE TRIGGER IF NOT EXISTS update_recipe_timestamp
AFTER UPDATE ON recipes
BEGIN
    UPDATE recipes SET date_modified = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
