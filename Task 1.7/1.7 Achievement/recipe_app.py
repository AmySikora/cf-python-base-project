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

# Create session class
Session = sessionmaker(bind=engine)
session = Session()

# Defines declarative base
Base = declarative_base()
print("Database connection successful!")

# Defines Recipe model
class Recipe(Base):
    __tablename__ = "final_recipes"
    
    # Defines the columns 
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    ingredients = Column(String(255), nullable=False)
    cooking_time = Column(Integer, nullable=False)
    difficulty = Column(String(20), nullable=False)

    # Defines the __repr__ representation method
    def __repr__(self):
        return f"<Recipe ID: {self.id} - {self.name} ({self.difficulty})>"

    # Defines the __str__ string method to print the recipe
    def __str__(self):
        print("-" * 20, end="\n") 
        print(f"Recipe ID: {self.id}", end=" | ")
        print(f"Name: {self.name}", end=" | ")
        print(f"Cooking Time: {self.cooking_time} minutes", end=" | ")
        print(f"Difficulty: {self.difficulty}", end="\n")
        print("-" * 20, end="\n")

    # Calculates the difficulty level of the recipe
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

    # Defines the list of ingredients
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return self.ingredients.split(", ")

# Create all defined tables in the database
Base.metadata.create_all(engine)

# Function 1: create_recipe
def create_recipe():
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
            num_ingredients = int(input("Enter the number of ingredients: "))
            if num_ingredients > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Please enter a valid number.")   

    for _ in range(num_ingredients):
        ingredient = input("Enter an ingredient: ").strip().lower()
        if ingredient not in ingredients:
            ingredients.append(ingredient)
        else:
            print(f"{ingredient} is already on the list.")

    # Convert ingredients list to a comma-separated string
    ingredients_str = ", ".join(ingredients)

    # Creates and savea a recipe
    recipe= Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    recipe.calc_difficulty()

    # Session add and commit recipe
    session.add(recipe)
    session.commit()  # Saves the changes 

    print("\nRecipe added successfully!")

#  Function 2: view_all_recipes
def view_all_recipes():
    # Retrieves as all recipes in the database
    recipes = session.query(Recipe).all()

    # Checks if recipes exist 
    if not recipes:
        print("\nNo recipes found in the database")
        return None
    
    # If recipies found, prints all recipes
    for recipe in recipes:
        print(recipe)

# Function #3 search_by_ingredients()
def search_by_ingredients():
    # Cheks to see if there are recipes in the database
    if session.query(Recipe).count() == 0:
        print("\nNo recipes were found in the database.")
        return None

    # Searches the database for ingredients
    results = session.query(Recipe.ingredients).all()
    all_ingredients = set()

    # Process results
    for row in results:
        all_ingredients.update(row[0].split(", ")) # Converts string back to list

    # Sort list of ingredients
    all_ingredients = sorted(all_ingredients) # Add ingredients

    # Shows the ingredients
    print("\nAvailable Ingredients:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")

    # Asks the user to select an ingredient
    while True:
        try:
            num = int(input("\nEnter the number of the ingredient to search for: "))
            if 0 <= num < len(all_ingredients):
                ingredient_searched = all_ingredients[num]  
                break
            else:
                print("Invalid choice. Please enter a valid number from the list.")
        except ValueError:
            print("Only numbers are allowed. Please try again.")

    # Search database for recipes that match the chosen ingredient
    found_recipes = session.query(Recipe).filter(Recipe.ingredients.like(f"%{ingredient_searched}%")).all()

    # If recipes with the ingredient is found print recipe(s)
    if found_recipes:
        print(f"\n{len(found_recipes)} Recipe(s) found with {ingredient_searched}:")
        for recipe in found_recipes:
            print(recipe)
    # If ingredient was not found notify user        
    else:
        print("No recipes found with that ingredient.")

# Function #4 edit_recipe
def edit_recipe():
    # Fetch all recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    
    # Searched for recipes to edit
    if not recipes:
        print("\nNo recipes found in the database.")
        return  # No recipes found, exit function

    # Displays the available recipes with their IDs and names
    print("\nAvailable Recipes:")
    for recipe_id, name in recipes:
        print(f"ID: {recipe_id} - Name: {name}")

    # Ask user to select a recipe by ID
        try:
            recipe_id = int(input("\nEnter the ID number of the recipe you would like to update: "))
            recipe = session.query(Recipe).filter_by(id=recipe_id).first()
            if not recipe:
                print("The recipe was not found.")
                return
        except ValueError:
            print("Only numbers are allowed. Please try again.")
            return      

    # Ask what the user would like to update
        print("\nWhat would you like to update?")
        print("1 - Name")
        print("2 - Cooking Time")
        print("3 - Ingredients")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            break
        print("Invalid choice. Please enter 1, 2, or 3.")

    # Updates based on users choice 
    if choice == '1':  # Updates name
        recipe.name = input("Enter the new name of the recipe: ").strip()
    elif choice == '2':  # Updates cooking time
            try:
                recipe.cooking_time = int(input("Enter new cooking time (in minutes): ")) 
                # Updates the reciecipe's difficulty level
                recipe.calc_difficulty() 
            except ValueError:
                print("Invalid input. Please enter a number.")
                return
    elif choice == '3':  # Updates ingredients
        new_ingredients = input("Enter new ingredients (separated by commas): ").strip().lower()
        recipe.ingredients = new_ingredients
        # Recalculates recipe difficulty
        recipe.cal_diffuctly()
    else:
        print("Invalid choice") 
        return   
    
    # Commit the changes
    session.commit()
    print("\nRecipe was successfully updated!")

# Function 5: delete_recipe 
def delete_recipe():
    # Fetch all recipes
    recipes = session.query(Recipe.id, Recipe.name).all()  # searches for all recipes by ID and name

    if not recipes:
        print("\nNo recipes found in the database.")
        return  # No recipes found, exit function

    # Display the available recipes with their IDs
    print("\nAvailable Recipes:")
    for recipe_id, name in recipes:
        print(f"ID: {recipe_id} - Name: {name}")

    # Ask user to select a recipe by ID
        try:
            recipe_id = int(input("\nEnter the ID number of the recipe you would like to delete: "))
            recipe = session.query(Recipe).filter_by(id=recipe_id).first()
            if not recipe:
                print("The recipe ID was not found.")
                return
        except ValueError:
            print("Invlaid input.") # Invalid input, continue loop

     # Confirm deletion
    confirm = input("\nAre you sure you want to delete this recipe? (yes/no): ").strip().lower()
    if confirm != 'yes':
        print("\nRecipe deletion canceled.")
        return  # Cancel deletion

    # Delete recipe
    session.delete(recipe)
    session.commit()

    # Print confirmation message after successful deletion
    print("\nRecipe was successfully deleted!")

# This is the loop running in the main menu
# Loop continues as long as user doesn't quit
def main_menu():

    while True:
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
            create_recipe()
        elif choice == "2":
            view_all_recipes()
        elif choice == '3':
            search_by_ingredients()
        elif choice == '4':
            edit_recipe()
        elif choice == '5':
            delete_recipe()
        elif choice == 'quit':
            print("Closing recipes application and saving changes...")   
            session.close()
            engine.dispose() # Closes the engine connection
            break  # Exits loop
        else:
            print("Invalid choice. Please enter a number between 1 and 5 or type 'quit'.")    

# Start the menu
main_menu()
