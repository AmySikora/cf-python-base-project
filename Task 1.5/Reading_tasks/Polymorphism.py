class ShoppingList:
    # Initialization method
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    # Method to add new items to self.shopping_list
    def add_item(self, item):
        # Simple filter to avoid repeated items
        if item not in self.shopping_list:
            self.shopping_list.append(item)

    # Method to remove an item from self.shopping_list.
    # We'll use a try-except block to avoid errors in case
    # the item isn't found.
    def remove_item(self, item):
        try:
            self.shopping_list.remove(item)
        except ValueError:
            print("Item not found.")

    # Method to view the shopping list
    def view_list(self):
        print("\nItems in " + str(self.list_name) + '\n' + 30 * '-')
        for item in self.shopping_list:
            print(' - ' + str(item))

    # Method to merge two shopping lists
    def merge_lists(self, other_list):
        # Creating a name for our new, merged shopping list
        merged_lists_name = 'Merged List - ' + str(self.list_name) + " + " + str(other_list.list_name)

        # Creating an empty ShoppingList object
        merged_lists_obj = ShoppingList(merged_lists_name)

        # Adding the first shopping list's items to our new list
        merged_lists_obj.shopping_list = self.shopping_list.copy()

        # Adding the second shopping list's items to our new list -
        # we're doing this so that there won't be any repeated items
        for item in other_list.shopping_list:
            if item not in merged_lists_obj.shopping_list:
                merged_lists_obj.shopping_list.append(item)

        # Returning our new, merged object
        return merged_lists_obj


# Creating instances
pet_store_list = ShoppingList('Pet Store List')
grocery_store_list = ShoppingList('Grocery Store List')

# Adding items to pet store list
for item in ['dog food', 'frisbee', 'bowl', 'collars', 'flea collars']:
    pet_store_list.add_item(item)

# Adding items to grocery store list
for item in ['fruits', 'vegetables', 'bowl', 'ice cream']:
    grocery_store_list.add_item(item)

# Merging lists using the instance method
merged_list = pet_store_list.merge_lists(grocery_store_list)

# Viewing merged list
merged_list.view_list()
