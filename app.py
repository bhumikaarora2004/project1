import mysql.connector
import pandas as pd
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# Function to establish database connection
def get_db_connection():
    return mysql.connector.connect(
        user="root",
        password="Bhumika@2608",
        database="recipe_db"
    )

# Route for the main landing page
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch all recipes from the database
@app.route('/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM recipes')
    recipes = cursor.fetchall()
    conn.close()
    return render_template('recipes.html', recipes=recipes)

# Route to handle form submission and fetch recommendations based on ingredient
@app.route('/recommendations', methods=['GET', 'POST'])
def get_recommendations():
    if request.method == 'POST':
        preference = request.form.get('ingredient')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        query = f"SELECT * FROM recipes WHERE ingredients LIKE '%{preference}%'"
        cursor.execute(query)
        recipes = cursor.fetchall()
        conn.close()
        
        if not recipes:
            return render_template('recipes.html', recipes=[], preference=preference, message='No recipes found for your preference')
        
        return render_template('recipes.html', recipes=recipes, preference=preference)

    # Handle GET request if needed (optional)
    return render_template('index.html')
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
