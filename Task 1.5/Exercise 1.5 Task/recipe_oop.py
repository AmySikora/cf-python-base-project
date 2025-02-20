# Defines Recipe Class
class Recipe:
    # Class variable to store recipe ingredients
    all_ingredients = set()

    # Initializing the Recipe object with name and cooking time
    def __init__(self, name, cooking_time):
        self.name = name  # Stores recipe's name
        self.ingredients = []  # Creates an empty list of ingredients
        self.cooking_time = cooking_time  # Stores cooking time in minutes
        self.difficulty = None  # Stores recipe's calcutlated difficulty 

    # Adds ingredients to recipe and updates ingredient list
    def add_ingredients(self, *ingredients): 
        self.ingredients.extend(ingredient) # Adds each ingredient to list
        self.update_all_ingredients()  # Updates the global ingredient set
        self.calculate_difficulty() # Updates difficulty if number of ingredients change

    # Determines the difficulty of recipe based on cooking_time and ingredient number
    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
    
    # Search for recipe ingredient
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
            
    # Updates all_ingresients class variable to include recipe ingredients
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)
    
    # String that represens the printed recipe 
    def __str__(self):
        output = "Name: " + self.name + \
            "\nCooking Time (in minutes): " + str(self.cooking_time) + \
            "\nIngredients: " + ', '.join(self.ingredients) + \
            "\nDifficulty: " + str(self.difficulty) + \
            "\n_________________________\n"

        for ingredient in self.ingredients:
            output += "- " + ingredient + "\n"

        return output

    # Define search for a recipe ingredient
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

# Adding Recipe classesa and ingredients
tea = Recipe("Tea", 5)
tea.add_ingredients("Water", "Tea Leaves", "Sugar")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients("Flour", "Sugar", "Eggs", "Milk", "Butter", " Vanilla Essence")
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients("Banana", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
print(banana_smoothie)

# Adds recipes to list
recipes_list = [tea, coffee, cake, banana_smoothie]

# Print string of recipes
print("\nAll Recipes:")
for recipe in recipes_list:
    print(recipe)

# Search for ingredient(s) in recipes
for ingredient in ["Water", "Sugar", "Bananas"]:
    Recipe.recipe_search(recipes_list, ingredient)
                   

