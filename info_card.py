name = input("Enter your name : ")
age = input("Enter your age : ")
hobby1 = input("Enter your first hobby : ")
hobby2 = input("Enter your second hobby : ")
hobby3 = input("Enter your third hobby : ")

age = int(age)

# Store hobbies in a list
hobbies = [hobby1, hobby2, hobby3]

print("\n--- Bio Data ---\n")

print(f"Name   : {name}")
print(f"Age    : {age}")

print("Hobbies:")
for h in hobbies:
    print(f" - {h}")

# Checking types
print("\nData Types:")
print(type(name))
print(type(age))
print(type(hobbies))


with open("info_card.txt", "w") as f:
    f.write("--- Bio Data ---\n\n")
    f.write(f"Name   : {name}\n")
    f.write(f"Age    : {age}\n")
    f.write("Hobbies:\n")
    for h in hobbies:
        f.write(f" - {h}\n")
