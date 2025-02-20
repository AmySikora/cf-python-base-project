# Defines Recipe Class
class Recipe:
    # Class to store recipe's ingredients
    all_ingredients = set()

    # Recipe object initialzation 
    def __init__(self, name, cooking_time):
        self.name = name  # Recipe name
        self.ingredients = []  # List of ingredients
        self.cooking_time = cooking_time  # Cooking time 
        self.difficulty = None  # Difficulty level

    # Adds ingredients and updates to add new ingredients
    def add_ingredients(self, *ingredients):
        self.ingredients.extend(ingredients)  # Adds ingredients to list
        self.update_all_ingredients()  # Updates all ingredients 
        self.calculate_difficulty()  # Updates difficulty level if ingredients change

    # Determines the cooking difficulty based on cooking time and ingredient count
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10:
            self.difficulty = "Medium"
        elif len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    # Checks if ingredient is in recipe
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    # Updates this recipe's ingredients
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

    # Prints recipe
    def __str__(self):
        output = "Name: " + self.name + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nIngredients: " + ', '.join(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty) + \
            "\n_________________________\n"

        for ingredient in self.ingredients:
            output += "- " + ingredient + "\n"

        return output 
    
    # Searches for recipes with an ingredient
    def recipe_search(data, search_term):
        print(f"\nRecipes containing '{search_term}':")
        found = False
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
                found = True
        if not found:
            print("No recipes found with that ingredient.")

# Main Code

# Adding recipes
tea = Recipe("Tea", 5)
tea.add_ingredients("Water", "Tea Leaves", "Sugar")

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")

cake = Recipe("Cake", 50)
cake.add_ingredients("Flour", "Sugar", "Eggs", "Milk", "Butter", "Vanilla Essence")

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Banana", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")

# List of all recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# Prints all recipes 
print("\nAll Recipes:")
for recipe in recipes_list:
    print(recipe)

# Searches for specific ingredients
for ingredient in ["Water", "Sugar", "Banana"]:
    Recipe.recipe_search(recipes_list, ingredient)
