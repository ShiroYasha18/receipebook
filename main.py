import streamlit as st
import sqlite3
import numpy as np
import pandas as pd

conn = sqlite3.connect('recipe.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS recipe ( id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,
             cooking_time INTEGER,  
             ingredients TEXT NOT NULL,
             steps TEXT NOT NULL

             )''')
conn.commit()


def fetch_all_items_as_dataframe():
    c.execute("SELECT * FROM recipe")
    rows = c.fetchall()
    df = pd.DataFrame(rows, columns=['id', 'name', 'cooking_time', 'ingredients', 'steps'])
    return df


def fetch_all_items():
    c.execute("SELECT * FROM recipe")
    rows = c.fetchall()
    return rows


def item_name_exists(name):
    c.execute("SELECT COUNT(*) FROM recipe WHERE name = ?", (name,))
    count = c.fetchone()[0]
    return count > 0


def add_item(name, cooking_time, ingredients, steps):  # Updated arguments
    if not item_name_exists(name):
        c.execute("INSERT INTO recipe (name, cooking_time, ingredients,steps) VALUES (?, ?, ?,?)",
                  (name, cooking_time, ingredients, steps))
        conn.commit()
        st.success("Recipe added successfully!")
    else:
        st.error("Recipe with that name already exists. Please choose a unique name.")


def update_item(id, name, cooking_time, ingredients, steps):  # Updated arguments
    c.execute("UPDATE recipe SET name = ?, cooking_time = ?, ingredients = ?, steps = ? WHERE id = ?",
              (name, cooking_time, ingredients, steps, id))
    conn.commit()
    st.success("Recipe updated successfully!")


def delete_item_by_name(name):
    if item_name_exists(name):
        c.execute("DELETE FROM recipe WHERE name = ?", (name,))
        conn.commit()
        st.success("Recipe deleted successfully!")
    else:
        st.error("Recipe with that name does not exist.")


st.title("Recipe Book👨🏻‍🍳")

selected_operation = st.sidebar.selectbox("Options", ["Create", "Read", "Update", "Delete"])

if selected_operation == "Create":
    st.subheader("Add New Recipe")
    new_recipe_name = st.text_input("Recipe Name")
    new_cooking_time = st.number_input("Cooking Time (Minutes)", min_value=0)  # Updated label
    new_ingredients = st.text_area("Ingredients")
    new_steps = st.text_area("Steps")
    if st.button("Add Recipe"):
        add_item(new_recipe_name, new_cooking_time, new_ingredients, new_steps)
if selected_operation == "Read":
    st.subheader("Current Recipes")
    items_df = fetch_all_items_as_dataframe()
    if not items_df.empty:
        st.dataframe(items_df, width=800, height=400)
    else:
        st.info("No recipes found.")

if selected_operation == "Update":
    items = fetch_all_items()
    if items:
        selected_item_id = st.sidebar.selectbox("Select Recipe to Update", [item[0] for item in items])
        if selected_item_id:
            c.execute("SELECT * FROM recipe WHERE id = ?", (selected_item_id,))
            item_to_update = c.fetchone()
            st.subheader("Update Recipe")
            updated_name = st.text_input("Recipe Name", item_to_update[1])
            updated_cooking_time = st.number_input("Cooking Time (Minutes)", min_value=0, value=item_to_update[2])
            updated_ingredients = st.text_area("Ingredients", item_to_update[3])
            updated_steps = st.text_area("Steps", item_to_update[4])
            if st.button("Update Recipe"):
                update_item(selected_item_id, updated_name, updated_cooking_time, updated_ingredients, updated_steps)

if selected_operation == "Delete":
    st.subheader("Delete Recipe by Name")
    item_to_delete_name = st.text_input("Enter Recipe Name")
    if st.button("Delete Recipe", key="delete"):
         delete_item_by_name(item_to_delete_name)


    conn.close()