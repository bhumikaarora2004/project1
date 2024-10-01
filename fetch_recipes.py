import requests
import pandas as pd
import mysql.connector

API_KEY = 'b03f93ddcce7435998272f7c64f3c2b0'
API_URL = 'https://api.spoonacular.com/recipes/random'

def fetch_recipes(number=10):
    params = {
        'apiKey': API_KEY,
        'number': number
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    recipes = data['recipes']
    return recipes

def save_to_database(recipes):
    conn = mysql.connector.connect(
        user="root",
        password="Bhumika@2608",
        database="recipe_db"
    )
    cursor = conn.cursor()

    for recipe in recipes:
        title = recipe['title']
        ingredients = ', '.join([ingredient['name'] for ingredient in recipe['extendedIngredients']])
        instructions = ' '.join([step['step'] for step in recipe['analyzedInstructions'][0]['steps']])
        image_url = recipe['image']

        cursor.execute("""
            INSERT INTO recipes (title, ingredients, instructions, image_url) 
            VALUES (%s, %s, %s, %s)
        """, (title, ingredients, instructions, image_url))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    recipes = fetch_recipes(number=10)
    save_to_database(recipes)
