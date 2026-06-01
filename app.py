"""
Kitchen King: Recipe & Pantry Manager
"""

import streamlit as st
import pandas as pd
import database as db

# Initialize database
db.init_db()

st.set_page_config(page_title="Kitchen King", page_icon="🍳", layout="centered")

st.title("🍳 Kitchen King")
st.subheader("Your Smart Recipe & Pantry Manager")

# App Navigation
tab1, tab2, tab3 = st.tabs(["My Pantry", "Recipe Book", "What Can I Cook?"])

# --- TAB 1: MY PANTRY ---
with tab1:
    st.write("### What's in your kitchen?")
    
    # Form to add items
    with st.form("pantry_form", clear_on_submit=True):
        new_item = st.text_input("Add an ingredient (e.g., onion, chicken, rice)")
        submit_pantry = st.form_submit_button("Add to Pantry")
        
        if submit_pantry and new_item:
            db.add_to_pantry(new_item)
            st.success(f"Added {new_item.lower()} to pantry!")
            
    # Display Pantry
    pantry_df = db.get_pantry()
    if not pantry_df.empty:
        st.write("**Current Inventory:**")
        # Display as pills/tags
        pantry_list = pantry_df['ingredient_name'].tolist()
        st.write(" • ".join([item.title() for item in pantry_list]))
        
        # Delete items
        with st.expander("Manage Pantry Items"):
            item_to_delete = st.selectbox("Select item to remove", pantry_df['id'].tolist(), 
                                          format_func=lambda x: pantry_df[pantry_df['id'] == x]['ingredient_name'].values[0])
            if st.button("Remove Item"):
                db.delete_pantry_item(item_to_delete)
                st.rerun()
    else:
        st.info("Your pantry is empty. Add some ingredients above!")


# --- TAB 2: RECIPE BOOK ---
with tab2:
    st.write("### Add a New Recipe")
    with st.form("recipe_form", clear_on_submit=True):
        recipe_name = st.text_input("Recipe Name")
        ingredients_input = st.text_area("Ingredients (Separate with commas)", placeholder="tomatoes, garlic, pasta, olive oil")
        instructions = st.text_area("Instructions")
        
        submit_recipe = st.form_submit_button("Save Recipe")
        
        if submit_recipe and recipe_name and ingredients_input:
            ing_list = ingredients_input.split(',')
            db.add_recipe(recipe_name, instructions, ing_list)
            st.success(f"Recipe '{recipe_name}' saved successfully!")
            
    st.markdown("---")
    st.write("### Your Saved Recipes")
    recipes_df = db.get_all_recipes()
    
    if not recipes_df.empty:
        for _, row in recipes_df.iterrows():
            with st.expander(row['recipe_name']):
                req_ingredients = db.get_recipe_ingredients(row['id'])
                st.write("**Ingredients:**", ", ".join(req_ingredients).title())
                st.write("**Instructions:**")
                st.write(row['instructions'])
                if st.button("Delete Recipe", key=f"del_{row['id']}"):
                    db.delete_recipe(row['id'])
                    st.rerun()
    else:
        st.info("No recipes saved yet.")


# --- TAB 3: WHAT CAN I COOK? ---
with tab3:
    st.write("### Let's see what you can make today!")
    
    recipes_df = db.get_all_recipes()
    pantry_df = db.get_pantry()
    
    if recipes_df.empty:
        st.warning("You need to add some recipes first!")
    elif pantry_df.empty:
        st.warning("Your pantry is empty! Go add some ingredients.")
    else:
        pantry_set = set(pantry_df['ingredient_name'].tolist())
        
        ready_to_cook = []
        missing_items_list = []
        
        # Cross-reference recipes with pantry
        for _, row in recipes_df.iterrows():
            recipe_ings = set(db.get_recipe_ingredients(row['id']))
            
            # Find what we have and what we are missing
            missing = recipe_ings - pantry_set
            
            if len(missing) == 0:
                ready_to_cook.append(row['recipe_name'])
            else:
                missing_items_list.append({
                    'name': row['recipe_name'],
                    'missing': missing,
                    'total_required': len(recipe_ings)
                })
        
        # Display 100% Matches
        if ready_to_cook:
            st.success("**You have all the ingredients for:**")
            for recipe in ready_to_cook:
                st.write(f"✅ **{recipe}**")
        else:
            st.info("You don't have all the ingredients for any single recipe right now.")
            
        st.markdown("---")
        
        # Display Partial Matches (Sorted by least missing ingredients)
        st.write("**Almost there (Missing 1-2 ingredients):**")
        almost_there = [r for r in missing_items_list if len(r['missing']) <= 2]
        
        if almost_there:
            # Sort by fewest missing items first
            almost_there = sorted(almost_there, key=lambda x: len(x['missing']))
            for item in almost_there:
                missing_str = ", ".join(item['missing']).title()
                st.write(f"🔸 **{item['name']}** — Missing: *{missing_str}*")
        else:
            st.write("No close matches.")