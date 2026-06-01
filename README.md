# Kitchen King: Recipe & Pantry Manager[cite: 5]

Kitchen King is a smart recipe and pantry manager application[cite: 5]. It is built using Python, Streamlit, Pandas[cite: 5], and an SQLite database[cite: 4]. The app helps you track what ingredients you have, save your favorite recipes, and discover what you can cook based on your current inventory[cite: 5].

## Features

* My Pantry: 
  * Add individual ingredients (e.g., onion, chicken, rice) to your inventory[cite: 5].
  * View your current inventory[cite: 5].
  * Manage and remove items you no longer have[cite: 5].
* Recipe Book:
  * Save new recipes by entering the recipe name, a comma-separated list of ingredients, and instructions[cite: 5].
  * View all saved recipes, including their specific ingredient lists and instructions[cite: 5].
  * Delete recipes from your book[cite: 5].
* What Can I Cook?:
  * Cross-references your saved recipes with your current pantry inventory[cite: 5].
  * Shows a list of recipes where you have all of the required ingredients[cite: 5].
  * Displays "Almost there" matches, showing recipes where you are only missing 1 to 2 ingredients[cite: 5].

## Tech Stack

* Frontend & Web Framework: Streamlit[cite: 5]
* Data Manipulation: Pandas[cite: 4, 5]
* Database: SQLite3[cite: 4]

## Project Structure

* app.py: Main Streamlit application file containing the UI and logic[cite: 5].
* database.py: Database helper functions for SQLite operations, including foreign key and cascade delete support[cite: 4].
* kitchen_king.db: SQLite database file generated upon running[cite: 4].

## Installation & Setup

1. Ensure you have Python installed.
2. Install the required dependencies:
   pip install streamlit pandas
3. Run the Streamlit app:
   streamlit run app.py
4. The application will open in your default web browser.

## Usage

1. Start by adding your current kitchen ingredients in the "My Pantry" tab[cite: 5].
2. Add your favorite meals in the "Recipe Book" tab[cite: 5].
3. Check the "What Can I Cook?" tab to see meal suggestions based on what you already have at home[cite: 5].
