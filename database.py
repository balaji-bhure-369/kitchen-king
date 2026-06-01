import sqlite3
import pandas as pd

DB_NAME = "kitchen_king.db"

def get_connection():
    """Returns a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Creates the relational tables for pantry and recipes."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table 1: Pantry Inventory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pantry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ingredient_name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Table 2: Recipes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_name TEXT NOT NULL,
            instructions TEXT
        )
    ''')
    
    # Table 3: Recipe Ingredients (Maps ingredients to a specific recipe)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipe_ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recipe_id INTEGER,
            ingredient_name TEXT NOT NULL,
            FOREIGN KEY(recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# --- PANTRY FUNCTIONS ---
def add_to_pantry(ingredient_name):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Convert to lowercase for consistent matching
        ingredient_name = ingredient_name.strip().lower()
        cursor.execute('INSERT INTO pantry (ingredient_name) VALUES (?)', (ingredient_name,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass # Ignore if it already exists in the pantry
    finally:
        conn.close()

def get_pantry():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM pantry ORDER BY ingredient_name", conn)
    conn.close()
    return df

def delete_pantry_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM pantry WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# --- RECIPE FUNCTIONS ---
def add_recipe(name, instructions, ingredients_list):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Insert the recipe
    cursor.execute('INSERT INTO recipes (recipe_name, instructions) VALUES (?, ?)', (name, instructions))
    recipe_id = cursor.lastrowid # Get the ID of the recipe we just created
    
    # 2. Insert all ingredients linked to this recipe_id
    for item in ingredients_list:
        item_clean = item.strip().lower()
        if item_clean:
            cursor.execute('INSERT INTO recipe_ingredients (recipe_id, ingredient_name) VALUES (?, ?)', 
                           (recipe_id, item_clean))
            
    conn.commit()
    conn.close()

def get_all_recipes():
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM recipes", conn)
    conn.close()
    return df

def get_recipe_ingredients(recipe_id):
    conn = get_connection()
    df = pd.read_sql_query("SELECT ingredient_name FROM recipe_ingredients WHERE recipe_id = ?", 
                           conn, params=(recipe_id,))
    conn.close()
    return df['ingredient_name'].tolist()

def delete_recipe(recipe_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
    # Because of ON DELETE CASCADE, the linked ingredients will also be deleted automatically
    conn.commit()
    conn.close()