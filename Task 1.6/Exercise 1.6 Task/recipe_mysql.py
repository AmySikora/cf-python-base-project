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
            print(f"{ingredient} is already in the list. Skipping duplicate.")

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

    return {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

# This is the loop running in the main menu
# Loop continues as long as user doesn't quit
def main_menu(conn, cursor):
    choice = ""  # Define choice before loop starts

    while choice != 'quit':  # Correct indentation
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

# Database connection setup
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='P@ssword123!',
    database='my_database'
)

cursor = conn.cursor()

# Start the menu
main_menu(conn, cursor)
