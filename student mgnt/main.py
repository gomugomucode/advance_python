from load_save_data import load_data
from add_student import add_student
from view_student import view_all
from delete_student import delete_student 

def main():
    students = load_data()

    while True:
        print("\n==== STUDENT MANAGEMENT SYSTEM ====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Delete Student")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_all(students)
        elif choice == "3":
            delete_student(students)
        elif choice == "4":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
