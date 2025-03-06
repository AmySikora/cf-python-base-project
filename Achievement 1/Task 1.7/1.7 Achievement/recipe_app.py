# Import required packages
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Create SQLAlchemy engine using MySQL Connector/Python
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# Create session class to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Defines declarative base for the ORM
Base = declarative_base()
logging.info("Database connection successful!")

# Defines Recipe model table structure
class Recipe(Base):
    __tablename__ = "final_recipes"

    # Define table columns
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

    # Calculates the difficulty level of the recipe based on cooking time and number of ingredients
    def calculate_difficulty(self):
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

# Function to create a new recipe
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

    ingredients_str = ", ".join(ingredients)
    recipe = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
    recipe.calculate_difficulty()

    session.add(recipe)
    session.commit()
    logging.info("Recipe added successfully!")
    print("\nRecipe added successfully!")

# Start the app
def main_menu():
    while True:
        print("\nMain Menu")
        print("1. Create a new recipe")
        print("Type 'quit' to exit.")

        choice = input("Your choice: ").strip().lower()

        if choice == "1":
            create_recipe()
        elif choice == "quit":
            session.close()
            engine.dispose()
            break
        else:
            logging.warning("User entered an invalid choice.")
            print("Invalid choice.")

main_menu()
