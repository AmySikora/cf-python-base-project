class Animal(object):
    # Every animal has an age, but a name may not be necessary
    def __init__(self, age):
        self.age = age
        self.name = None

    # We'll throw in getter methods for age and name       
    def get_age(self):
        return self.age

    def get_name(self):
        return self.name

    # And setter methods as well
    def set_age(self, age):
        self.age = age

    def set_name(self, name):
        self.name = name

    # We'll also have a well-formatted string representation, too!
    def __str__(self):
        output = "\nClass: Animal\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output

a = Animal(5)
print(a)

class Cat(Animal):  
    # Introducing a new method where it speaks
    def speak(self):
        print("Meow")

    def __str__(self):
        output = "\nClass: Cat\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output

 
class Dog(Animal):
    def speak(self):
        print("Woof!")

    def __str__(self):
        output = "\nClass: Dog\nName: " + str(self.name) + \
            "\nAge: " + str(self.age)
        return output

cat = Cat(3)
dog = Dog(6)

cat.set_name("Stripes")
dog.set_name("Bubbles")

class Human(Animal):
    # Making its own initialization method
    def __init__(self, name, age):
        # Calling the parent class' init method to initialize
        # other attributes like 'name' and 'age'
        Animal.__init__(self, age)
         # Setting a name, since humans must have names
        self.set_name(name) 
        self.set_age(age)
        # Our new attribute for humans, 'friends'!
        self.friends = []

        # Adding another method to add friends
    def add_friend(self, friend_name):
        self.friends.append(friend_name)
        
        # A method to display friends
    def speak(self):
        print("Hello, my name's " + self.name + "!")

    # A method to display friends
    def __str__(self):
        output = "\nClass: Human\nName: " + str(self.name) + \
            "\nAge: " + str(self.age) + "\nFriends list: \n"
        for friend in self.friends:
            output += friend + "\n"
        return output
    
human = Human("Tobias", 35)