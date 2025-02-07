def recipes():
    """
    
    Collects recipes from user, assesses their cooking difficulty,
    and displays a list of the ingredients.
    """

    # Recipe storage
    recipes_list = []
    ingredients_set = set(0)

    def make_recipe():
        """
        Asks user questions about recipe's name, cooking time, and ingredients.
        
        Returns:
            dict: Recipe information
        """
        name = input("Enter recipe name: ")

        # Verify cooking time input is an integer
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
            ingredient = input("Enter an ingredient: ")
            ingredients.append(ingredient)
            ingredients_set.add(ingredient) # Set will stop dupes

        return {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
     
    # Ask how many recipes the user wants to enter
    while True:
        try:
            num = int(input("What number of recipes would you like to enter?: "))
            if num > 0:
                break
            else:
                print("Please enter a positve number.")
        except ValueError:
            print("Please enter a valid number.")

    # Collect recipes
    for _ in range(num):
         recipe = make_recipe()
         recipes_list.append(recipe)

    def print_ingredients():
        """Prints all unique ingredients in alphabbetical order"""
        print("\nAll Unique Ingredients")
        print("_______________")
        for ingredient in sorted(ingredients_set): #sorted
            print(ingredient)

    # Determine recipe difficulty
    for recipe in recipes_list: 
        if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
            recipe['difficulty'] = "Easy"
        elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
            recipe['difficulty'] = "Medium"
        elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
            recipe['difficulty'] = "Intermediate"
        else:
            recipe['difficulty'] = "Hard"

        # Print revipe details
        print("Recipe:", recipe['name'])
        print("Cooking time (min):", recipe['cooking_time'])
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print(" -", ingredient)
        print("Difficulty:", recipe['difficulty'])

    # Print all collected ingredients
    print_ingredients()

# Run the function
recipes()

    
