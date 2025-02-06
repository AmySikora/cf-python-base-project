def recipes():
    recipes_list = []
    ingredients_list = []

    def take_recipe():
        name = input("Enter recipe name: ")
        cooking_time = int(input("Enter cooking time in minutes: "))
        ingredients = []

        n = int(input("Enter the number of ingredients: "))
        for i in range(n):
            ingredient = input("Enter an ingredient: ")
            ingredients.append(ingredient)

        recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
        return recipe 

    num = int(input("What number of recipes would you like to enter?: "))
    
    for i in range(num):
         recipe = take_recipe()
         recipes_list.append(recipe)

         for ingredient in recipe['ingredients']:
             if ingredient not in ingredients_list:
                 ingredients_list.append(ingredient)

    def print_ingredients():
        ingredients_list.sort()
        print("\nAll Ingredients")
        print("_______________")
        for ingredient in ingredients_list:
            print(ingredient)

    for recipe in recipes_list: 
        if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
            recipe['difficulty'] = "Easy"
        elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
            recipe['difficulty'] = "Medium"
        elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
            recipe['difficulty'] = "Intermediate"
        else:
            recipe['difficulty'] = "Hard"

        print("Recipe:", recipe['name'])
        print("Cooking time (min):", recipe['cooking_time'])
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print(" ", ingredient)
        print("Difficulty:", recipe['difficulty'])

    print_ingredients()

recipes()

    
