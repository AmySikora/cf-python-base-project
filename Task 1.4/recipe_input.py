import pickle 

# Determine recipe difficulty
def calc_difficulty(cooking_time, num_ingredients): 
    if cooking_time < 10 and num_ingredients < 4:
        return "Easy"
    elif cooking_time < 10 and num_ingredients >= 4:
        return "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        return "Intermediate"
    else:
        return "Hard"

# Define take_recipe function to take recipes from the user
def take_recipe():
    name = input("\nEnter recipe name: ").strip()
    
    # Verify cooking time input is an number
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

    # Calculate cooking difficulty 
    difficulty = calc_difficulty(cooking_time, len(ingredients))

    return {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'difficulty': difficulty
    }

# Get filename from user
filename = input("Enter the filename to store recipes: ").strip()

# Try to open the binary file and load data
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
        print("File loaded successfully.")
except FileNotFoundError:
    print(f"File '{filename}' not found. Creating a new recipe file.")
    data = {"recipes_list": [], "all_ingredients": []}
except: 
    print(f"Error reading '{filename}'. Creating a new recipe file.")
    data = {"recipes_list": [], "all_ingredients": []}

# Gets recipe and ingredients lists from dictionary
recipes_list = data["recipes_list"]
all_ingredients = data["all_ingredients"]

# Asks the user how many recipes they’d like to enter
while True:
    try:
        num_recipes = int(input("\nHow many recipes would you like to enter?: "))
        if num_recipes > 0:
            break
        else:
            print("Please enter a positive number.")
    except ValueError:
        print("Please enter a valid number.")

# Collect user recipes
for _ in range(num_recipes):
    recipe = take_recipe()
    recipes_list.append(recipe)

    # Add new ingredients to the all_ingredients list if not already there
    for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

    print("Your recipe was added!")

# Update the dictionary
data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}

# Save the updated data back to the binary file
with open(filename, "wb") as file:
    pickle.dump(data, file)

print("\nRecipes saved successfully!")
