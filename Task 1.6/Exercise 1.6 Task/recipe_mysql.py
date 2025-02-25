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


