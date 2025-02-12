import pickle

# Function to display a recipe
def display_recipe(recipe):
    print("\n----------------------------")
    print("Recipe:", recipe["name"])
    print("Cooking Time:", recipe["cooking_time"], "mins")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print("-", ingredient)
    print("Difficulty:", recipe["difficulty"])
    print("----------------------------")

# Function to search recipes by ingredient
def search_ingredient(data):
    all_ingredients = data["all_ingredients"]

    # Show available ingredients with numbers
    print("\nIngredients List:")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")

    # Ask user to select an ingredient by number
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

    # Find recipes with the selected ingredient
    print(f"\nSearching for recipes with: {ingredient_searched}...")
    recipes_with_ingredient = [recipe for recipe in data["recipes_list"] if ingredient_searched in recipe["ingredients"]]

    # Display results
    if recipes_with_ingredient:
        print(f"\n{len(recipes_with_ingredient)} Recipe(s) found:")
        for recipe in recipes_with_ingredient:
            display_recipe(recipe)
    else:
        print("No recipes found with this ingredient.")

# Load recipe data from file
filename = input("Enter the recipe file name: ").strip()

try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
        print("\nFile loaded successfully!")
except FileNotFoundError:
    print("Error: File not found. Please check the filename.")
    data = {"recipes_list": [], "all_ingredients": []}
except (EOFError, pickle.UnpicklingError):
    print("Error reading file. Creating a new recipe list.")
    data = {"recipes_list": [], "all_ingredients": []}

# Start search if recipes exist
if data["recipes_list"]:
    search_ingredient(data)
else:
    print("No recipes available to search.")
