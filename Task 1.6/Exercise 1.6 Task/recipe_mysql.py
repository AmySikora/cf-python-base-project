import mysql.connector

# Defines cooking difficulty    
def calc_difficulty(cooking_time, num_ingredients): 
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"
    
# Define create recipe
def create_recipe(conn, cursor):
    name = input("\nEnter recipe name: ").strip()
    
    # Verify cooking time input is a number
    while True: 
        try:
            cooking_time = int(input("Enter cooking time in minutes: "))
            break
        except ValueError:
            print("Only numerical values can be entered. Please enter a number.")

    # Get ingredients
    ingredients = []
    while True:
        try:
            n = int(input("Enter the number of ingredients: "))
            if n > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")   

    for _ in range(n):
        ingredient = input("Enter an ingredient: ").strip().lower()
        if ingredient not in ingredients:
            ingredients.append(ingredient)
        else:
            print(ingredient + " is already in the list. Skipping duplicate.")

    # Convert ingredients list to a comma-separated string
    ingredients_str = ", ".join(ingredients)

    # Calculate cooking difficulty 
    difficulty = calc_difficulty(cooking_time, len(ingredients))

    # SQL Query to Insert Data into the Recipes Table
    query = '''INSERT INTO recipes (name, ingredients, cooking_time, difficulty) 
               VALUES (%s, %s, %s, %s)'''
    
    values = (name, ingredients_str, cooking_time, difficulty)

    # Execute query
    cursor.execute(query, values)
    conn.commit()  # Save changes to the database

    print("\nRecipe added successfully!")

# Defines search for recipe ingredient
def search_recipe(conn, cursor):
    # Search database for ingredients
    cursor.execute("SELECT ingredients FROM recipes")
    results = cursor.fetchall() # Fetch data in rows
    
    # Creating a list for ingredients
    all_ingredients = set()

    # Process results
    for row in results:
        ingredients_list = row[0].split(", ") # Convert string back to list
        all_ingredients.update(ingredients_list) # Add ingredients

    # Sort list of ingredients
    all_ingredients = sorted(list(all_ingredients))

    # Showsingredients
    print("\nAvailable Ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(str(index) + ". " + ingredient)

    # Ask user to select an ingredient
    while True:
        try:
            num = int(input("\nEnter the number of the ingredient to search for: "))
            if 0 <= num < len(all_ingredients):
                ingredient_searched = all_ingredients[num]  # Correct variable name
                break
            else:
                print("Invalid choice. Please enter a valid number from the list.")
        except ValueError:
            print("Only numbers are allowed. Please try again.")

    # Search database for recipes with the ingredient
    query = "SELECT name, ingredients, cooking_time, difficulty FROM recipes WHERE ingredients LIKE %s"
    cursor.execute(query, ('%' + ingredient_searched + '%',))
    recipes_found = cursor.fetchall()  # Get all recipe matches

    # Show results
    if recipes_found:
        print("\n" + str(len(recipes_found)) + " Recipe(s) found with " + ingredient_searched + ":")
        for recipe in recipes_found:
            print("\n--------------------------------")
            print("Name: " + recipe[0])
            print("Ingredients: " + recipe[1])
            print("Cooking Time: " + str(recipe[2]) + " minutes")
            print("Difficulty: " + recipe[3])
            print("--------------------------------")
    else:
        print("No recipes found with this ingredient.")

# Define update recipe function
def update_recipe(conn, cursor):
    # Fetch all recipes
    cursor.execute("SELECT id, name FROM recipes")
    all_recipes = cursor.fetchall()  # Fetch data as tuples
    
    if not all_recipes:
        print("\nNo recipes found in the database.")
        return  # No recipes found, exit function

    # Display the available recipes with their IDs
    print("\nAvailable Recipes:")
    for recipe in all_recipes:
        print("ID:", recipe[0], "- Name:", recipe[1])

    # Ask user to select a recipe by ID
    while True:
        try:
            recipe_id = int(input("\nEnter the ID number of the recipe you would like to update: "))
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
            selected_recipe = cursor.fetchone()
            if selected_recipe:
                break
            else:
                print("Recipe ID", recipe_id, "does not exist. Please try again.")
        except ValueError:
            print("Only numbers are allowed. Please try again.")

    # Ask what to update
    while True:
        print("\nWhat would you like to update?")
        print("1 - Name")
        print("2 - Cooking Time")
        print("3 - Ingredients")
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    # Update based on choice 
    if choice == '1':  # Updates name
        new_name = input("Enter the new name of the recipe: ").strip()
        cursor.execute("UPDATE recipes SET name = %s WHERE id = %s", (new_name, recipe_id))

    elif choice == '2':  # Updates cooking time
        while True:
            try:
                new_cooking_time = int(input("Enter new cooking time (in minutes): "))  
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Recalculate difficulty
        cursor.execute("SELECT ingredients FROM recipes WHERE id = %s", (recipe_id,))
        ingredients_str = cursor.fetchone()[0]
        num_ingredients = len(ingredients_str.split(", "))
        new_difficulty = calc_difficulty(new_cooking_time, num_ingredients)

        cursor.execute("UPDATE recipes SET cooking_time = %s, difficulty = %s WHERE id = %s",
                       (new_cooking_time, new_difficulty, recipe_id))
    
    elif choice == '3':  # Updates ingredients
        new_ingredients = input("Enter new ingredients (separated by commas): ").strip().lower()

        # Recalculate difficulty
        num_ingredients = len(new_ingredients.split(", "))
        cursor.execute("SELECT cooking_time FROM recipes WHERE id = %s", (recipe_id,))
        cooking_time = cursor.fetchone()[0]
        new_difficulty = calc_difficulty(cooking_time, num_ingredients)

        cursor.execute("UPDATE recipes SET ingredients = %s, difficulty = %s WHERE id = %s",
                       (new_ingredients, new_difficulty, recipe_id))
    
    # Commit the changes
    conn.commit()
    print("\nRecipe ID", recipe_id, "was successfully updated!")



# Define delete recipe function
def delete_recipe(conn, cursor):
    # Fetch all recipes
    cursor.execute("SELECT id, name FROM recipes")
    all_recipes = cursor.fetchall()  # Fetch data as tuples

    if not all_recipes:
        print("\nNo recipes found in the database.")
        return  # No recipes found, exit function

    # Display the available recipes with their IDs
    print("\nAvailable Recipes:")
    for recipe in all_recipes:
        print("ID:", recipe[0], "- Name:", recipe[1])

    # Ask user to select a recipe by ID
    while True:
        try:
            recipe_id = int(input("\nEnter the ID number of the recipe you would like to delete: "))
            cursor.execute("SELECT * FROM recipes WHERE id = %s", (recipe_id,))
            selected_recipe = cursor.fetchone()
            if selected_recipe:
                break
        except ValueError:
            pass  # Invalid input, continue loop

     # Confirm deletion
    print("\nAre you sure you want to delete this recipe? (yes/no)")
    confirm = input().strip().lower()
    if confirm != 'yes':
        print("\nRecipe deletion canceled.")
        return  # Cancel deletion

    # Delete recipe
    cursor.execute("DELETE FROM recipes WHERE id = %s", (recipe_id,))
    conn.commit()  # Save changes

    # Print confirmation message after successful deletion
    print("\nRecipe ID", recipe_id, "was successfully deleted!")

# This is the loop running in the main menu
# Loop continues as long as user doesn't quit
def main_menu(conn, cursor):
    choice = ""  # Define choice before loop starts

    while choice != 'quit':  # Keep running until user quits
        print("\nMain Menu")
        print("=====================================")
        print("What would you like to do? Pick a choice!")
        print("1. Create a new recipe")
        print("2. Search for a recipe by ingredient")
        print("3. Update an existing recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit the program.")  

        choice = input("Your choice: ").strip().lower()  # Remove spaces & make lowercase

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == 'quit':
            print("Closing recipes and saving changes...")   
            conn.commit()  # Save changes to database
            cursor.close()
            conn.close()
            return  # Ensures function exits properly
        else:
            print("Invalid choice. Please enter one of the following numbers: 1, 2, 3, 4, or 'quit'.")    

import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database credentials securely
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Establish database connection
conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    passwd=DB_PASSWORD,
    database=DB_NAME
)

cursor = conn.cursor()

# Start the menu
main_menu(conn, cursor)
