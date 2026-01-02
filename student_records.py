import json
import os

# File where data is stored permanently
FILE_NAME = "students_database.json"

def load_data():
    """Reads the database file and returns a dictionary."""
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {} # Return empty if file is corrupted
    return {}

def save_data(data):
    """Writes the current dictionary into the database file."""
    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=4)

def add_student(students):
    s_id = input("Enter Student ID: ")
    if s_id in students:
        print("Error: ID already exists!")
        return
    
    name = input("Enter Name: ")
    age = input("Enter Age: ")
    
    # Add to dictionary
    students[s_id] = {"name": name, "age": age}
    save_data(students) # Update file
    print(f"Student {name} added successfully.")

def view_all(students):
    if not students:
        print("\nDatabase is empty.")
        return
    
    print("\n--- Student Records ---")
    for s_id, details in students.items():
        print(f"ID: {s_id} | Name: {details['name']} | Age: {details['age']}")

def delete_student(students):
    print("\n1. Delete by ID")
    print("2. Delete by Name")
    sub_choice = input("Select delete method: ")

    match sub_choice:
        case "1":
            s_id = input("Enter ID to delete: ")
            if students.pop(s_id, None):
                save_data(students)
                print(f"ID {s_id} deleted from file.")
            else:
                print("ID not found.")
        
        case "2":
            target_name = input("Enter Name to delete: ").lower()
            id_to_delete = None
            for s_id, details in students.items():
                if details['name'].lower() == target_name:
                    id_to_delete = s_id
                    break
            
            if id_to_delete:
                del students[id_to_delete]
                save_data(students)
                print(f"Student '{target_name}' removed from file.")
            else:
                print("Name not found.")

def main():
    # Load data from file once at the start
    students = load_data()

    while True:
        print("\n==== STUDENT SYSTEM ====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Delete Student")
        print("4. Exit")
        
        choice = input("Enter choice (1-4): ")

        match choice:
            case "1":
                add_student(students)
            case "2":
                view_all(students)
            case "3":
                delete_student(students)
            case "4":
                print("Exiting program. Goodbye!")
                break
            case _:
                print("Invalid selection. Try again.")

if __name__ == "__main__":
    main()
