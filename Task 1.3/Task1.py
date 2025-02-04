a = int(input("Enter a number: "))
b = int(input("Enter another number: "))
operator = input("Enter a (+ or -) sign to add or subtact the numbers: ")

if operator == "+": 
    result = a + b
    print("The sum if these numbers is " + str(a + b))

if operator == "-": 
    result = a - b
    print("The difference between these numbers is " - str(a - b))