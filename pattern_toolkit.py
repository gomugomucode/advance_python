def right_triangle(height):
    for i in range(1, height + 1):
        for j in range(i):
            print("*", end="")
        print()


def inverted_triangle(height):
    for i in range(height, 0, -1):
        for j in range(i):
            print("*", end="")
        print()


def pyramid(height):
    for i in range(1, height + 1):
        for j in range(height - i):
            print(" ", end="")
        for k in range(2 * i - 1):
            print("*", end="")
        print()


while True:
    print("\nChoose pattern:")
    print("1. Right Triangle")
    print("2. Inverted Triangle")
    print("3. Pyramid")
    print("4. Exit")

    user_choice = int(input("Enter your choice: "))

    if user_choice == 4:
        print("See you soon")
        break

    height = int(input("Enter height: "))

    match user_choice:
        case 1:
            right_triangle(height)
        case 2:
            inverted_triangle(height)
        case 3:
            pyramid(height)
        case _:
            print("Invalid choice")
