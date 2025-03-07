# Imports SQLAlchemy packages and modules needed for code to run
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# Loads secrets from .env file
load_dotenv()

# Gets database credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Create SQLAlchemy engine using MySQL Connector/Python
engine = create_engine(f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Create session class to work with the database
Session = sessionmaker(bind=engine)
session = Session()

# Defines declarative base
Base = declarative_base()
print("Database connection successful!")

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Defines Recipe model table structure
class Recipe(Base):
    __tablename__ = "final_recipes"
    
    # Defines the columns 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)

    # Defines how the object is displayed
    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name} ({self.difficulty})>"

    # Defines how the recipe will display when printed
    def __str__(self):
        return (
            f"{'-'*40}\n"
            f"Recipe ID: {self.id} | Name: {self.name} | Cooking Time: {self.cooking_time} minutes | Difficulty: {self.difficulty}\n"
            f"Ingredients: {', '.join(self.return_ingredients_as_list())}\n"
            f"{'-'*40}"
        )

    # Calculates the difficulty level of the recipe based on cooking time and number of ingresdients
    def calc_difficulty(self):
        num_ingredients = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and num_ingredients < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Returns ingredients as a list
    def return_ingredients_as_list(self):
        return self.ingredients.split(", ") if self.ingredients else []

# Create all defined tables in the database
Base.metadata.create_all(engine)

# Function 1: create_recipe
def create_recipe():
    while True:
        name = input("\nEnter recipe name: ").strip()
        if not name:
            logging.warning("User entered an empty recipe name.")
            print("The recipe name cannot be empty. Please add a name to your recipe.")
        elif len(name) > 50:
            logging.warning("User entered a recipe name that is too long.")
            print("Recipe name must be under 50 characters. Please enter a shorter name.")
        else:
            break    

    # Get cooking time and validate it as a number
    while True: 
        try:
            cooking_time = int(input("Enter cooking time in minutes: "))
            if cooking_time > 0:
                break
            else:
                logging.warning("User entered zero or negative cooking time.")
                print("Cooking time must be greater than zero.")
        except ValueError:
            logging.error("Invalid cooking time input.")
            print("Only numbers are allowed. Please try again.")

    # Get ingredients and validate user entries
    ingredients = []
    while True:
        try:
            num_ingredients = int(input("Enter the number of ingredients: "))
            if num_ingredients > 0:
                break
            else:
                logging.warning("User entered zero or negative number of ingredients.")
                print("Please enter a positive number.")
        except ValueError:
            logging.error("Invalid number of ingredients input.")
            print("Please enter a valid number.")   

    for _ in range(num_ingredients):
        ingredient = input("Enter an ingredient: ").strip().lower()
        if ingredient not in ingredients:
            ingredients.append(ingredient)
        else:
            logging.info(f"User entered a duplicate ingredient: {ingredient}")
            print(f"{ingredient} is already on the list.")

    # Converts ingredient list to a string for storage
    ingredients_str = ", ".join(ingredients)
    recipe = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    recipe.calculate_difficulty()

    # Creates and saves new recipe
    recipe = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    recipe.calc_difficulty()

    session.add(recipe)
    session.commit()
    logging.info("Recipe added successfully!")
    print("\nRecipe added successfully!")

# Function 2: view_all_recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("\nNo recipes found in the database.")
        return
    for recipe in recipes:
        print(recipe)

# Function 3: search_by_ingredients
def search_by_ingredients():
    # Checks to see if receipes are in the database
    if session.query(Recipe.id).first() is None:
        print("\nNo recipes found in the database.")
        return

    # Gets all ingredients from database
    results = session.query(Recipe.ingredients).all()
    all_ingredients = set()

    # Loop for all recipe ingredients entered
    for row in results:
        all_ingredients.update(row[0].split(", "))

    # Converts to a sorted list to be displayed
    all_ingredients = sorted(all_ingredients)

    # Displays available ingredients to user
    print("\nAvailable Ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")

    # Asks user to enter a number to select an ingredient
    while True:
        try:
            num = int(input("\nEnter the number of the ingredient to search for: "))
            if 0 <= num < len(all_ingredients):
                ingredient_searched = all_ingredients[num]
                break
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Only numbers are allowed. Please try again.")

    # Searches the database for recipes with the chosen ingredient
    found_recipes = session.query(Recipe).filter(Recipe.ingredients.ilike(f"%{ingredient_searched}%")).all()

    # Displays found recipes or that none match
    if found_recipes:
        print(f"\n{len(found_recipes)} Recipe(s) found with {ingredient_searched}:")
        for recipe in found_recipes:
            print(recipe)
    else:
        print("No recipes found with that ingredient.")

# Function 4: edit_recipe
def edit_recipe():
    # Fetch all recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    if not recipes:
        print("\nNo recipes found.")
        return  # Exit function if no recipes exist

    print("\nAvailable Recipes:")
    for recipe_id, name in recipes:
        print(f"ID: {recipe_id} - Name: {name}")

    # Keep asking until user enters a valid recipe ID
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to update: "))
            recipe = session.query(Recipe).filter_by(id=recipe_id).first()
            if recipe:
                break  # If valid ID entered, exits the loop
            else:
                print("Recipe ID not found. Please enter a valid recipe ID.")
        except ValueError:
            print("Invalid input. Please enter a valid numeric recipe ID.")

    # Keep asking until user enters a valid menu choice
    while True:
        print("\nWhat would you like to update?")
        print("1 - Name")
        print("2 - Cooking Time")
        print("3 - Ingredients")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":  # Updating the name
            while True:
                new_name = input("Enter new name: ").strip()
                if len(new_name) == 0:
                    print("Recipe name cannot be empty. Please enter a valid name.")
                elif len(new_name) > 50:
                    print("Recipe name is too long (max 50 characters). Please try again.")
                else:
                    recipe.name = new_name  # Valid name entered, update it
                    break

        elif choice == "2":  # Updating cooking time
            while True:
                try:
                    new_cooking_time = int(input("Enter new cooking time (in minutes): "))  
                    recipe.cooking_time = new_cooking_time
                    recipe.calc_difficulty()  # Update difficulty level
                    break
                except ValueError:
                    print("Invalid input. Cooking time must be a number. Please try again.")

        elif choice == "3":  # Updating ingredients
            while True:
                new_ingredients = input("Enter new ingredients (comma-separated): ").strip().title()
                if len(new_ingredients) == 0:
                    print("Ingredients list cannot be empty. Please enter at least one ingredient.")
                else:
                    recipe.ingredients = new_ingredients
                    recipe.calc_difficulty()  # Recalculate difficulty
                    break

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue  # Keeps looping if the input is invalid

        break  # Exit choice loop after a valid selection

    session.commit()
    print("\nRecipe updated successfully! Returning to main menu...\n")

          
# Function 5: delete_recipe
def delete_recipe():
    # Fetch all recipes
    recipes = session.query(Recipe.id, Recipe.name).all()

    if not recipes:
        print("\nNo recipes found in the database.")
        return  # Exit function if no recipes exist

    # Display available recipes
    print("\nAvailable Recipes:")
    for recipe_id, name in recipes:
        print(f"ID: {recipe_id} - Name: {name}")

    # Keep asking until a valid recipe ID is entered
    while True:
        try:
            recipe_id = int(input("\nEnter the ID of the recipe to delete: "))
            recipe = session.query(Recipe).filter_by(id=recipe_id).first()
            if recipe:
                break  # Valid recipe found, exit loop
            else:
                print("Recipe ID not found. Please enter a valid recipe ID.")
        except ValueError:
            print("Invalid input. Please enter a numeric recipe ID.")

    # Confirm deletion
    confirm = input(f"\nAre you sure you want to delete '{recipe.name}'? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\nRecipe deletion canceled. Returning to main menu...")
        return  # Exit without deleting

    # Delete recipe
    session.delete(recipe)
    session.commit()

    # Prints a confirmation message after successful deletion
    print(f"\nRecipe '{recipe.name}' was successfully deleted! Returning to main menu...\n")


# Main menu
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Create a new recipe")
        print("2. View all recipes")
        print("3. Search for a recipe by ingredient")
        print("4. Edit a recipe")
        print("5. Delete a recipe")
        print("Type 'quit' to exit.")

        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == "3":
            search_by_ingredients()
        elif choice == "4":
            edit_recipe()
        elif choice == "5":
            delete_recipe()
        elif choice == "quit":
            session.close()
            engine.dispose()
            break
        else:
            print("Invalid choice.")

# Starts the app
main_menu()