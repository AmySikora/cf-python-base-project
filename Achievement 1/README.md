# **Recipe App (Command Line Version)**
A simple, interactive command-line application for storing and managing recipes in a MySQL database. Users can add, update, delete, and search for recipes using ingredients.  

This project is designed to build **Python scripting and database management skills** while keeping the user experience simple and intuitive.

---

## ** Technologies Used**
- **Python 3.6+** (program logic)
- **SQLAlchemy** (database ORM)
- **MySQL** (storage for recipes)
- **dotenv** (secure credential management)

---

## ** Features**
 **Add, update, delete, and search for recipes**  
**Store recipes in a MySQL database**  
**Find recipes using ingredient-based search**  
**Automatically calculate difficulty** based on ingredients and cooking time  
**Handles errors gracefully** (invalid inputs, missing data, etc.)  
**User-friendly menu navigation**  

---

## **Installation & Setup**
### **Clone the Repository**
```sh
git clone https://github.com/AmySikora/cf-python-base-project
cd cf-python-base-project
```

### ** Install Dependencies**
```sh
pip install -r requirements.txt
```

### **Set Up Environment Variables**
Create a `.env` file in the project directory and add:
```
DB_HOST=your_database_host
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_NAME=your_database_name
```

### **Run the Application**
```sh
python recipe_app.py
```

---

## ** How to Use**
### **Main Menu**
```
1. Add a new recipe
2. Search for a recipe by ingredient
3. Edit an existing recipe
4. Delete a recipe
Type 'quit' to exit.
```

### **Adding a Recipe**
- Enter the **recipe name, cooking time, and ingredients**.
- The app calculates **difficulty level** automatically.

### **Searching for Recipes**
- View a list of **available ingredients**.
- Select an ingredient to find **matching recipes**.

### **Editing & Deleting Recipes**
- Select a recipe by **ID** to modify or remove it.
- Updating a recipe **automatically adjusts difficulty** if needed.

---

## ** Error Handling**
**Prevents duplicate ingredients**  
**Ensures valid numerical inputs**  
✔ **Handles database connection errors** gracefully  
✔ **Guides the user through interactions with clear prompts**  

---

## ** Future Enhancements**
**Convert to a web app with Django**  
**User authentication for personal recipe management**  
**More filtering options (by cooking time, difficulty, etc.)**  

--