class ShoppingList(object):
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []
    
     # Adding new items to shoopping list
    def add_item(self, item):
        if item in self.shopping_list:
            print("Item is already on the list.")
        else:
            self.shopping_list.append(item)
            print(item + " was added to the list.")    
    
    # Removing new items from shoopping list
    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print (item + " was removed from the list.")
        else: 
            print("Item is not on your list.")

    # View shopping list 
    def view_list(self):
        print("Shopping List: ", + self.list_name)
        print("---------------")
        for item in self.shopping_list:
            print(item)

# Creating pet store list
pet_store_list = ShoppingList("Pet Store Shopping List")

# Add items
pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collars")
pet_store_list.add_item("flea collars")

# Reamove flea collar
pet_store_list.remove_item("flea collars")

# Add frisbee again
pet_store_list.add_item("frisbee")

# show shopping list
pet_store_list.view_list()


        

    


    



