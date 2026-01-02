from load_save_data import save_data

def add_student(students):
    try:
        student_id = input("Enter Student ID: ").strip()  # do NOT convert to int
    except ValueError:
        print("ID must be a number.")
        return

    if student_id in students:
        print("ID already exists!")
        return

    name = input("Enter Name: ").strip()
    
    try:
        age = int(input("Enter Age: "))
    except ValueError:
        print("Age must be a number.")
        return

    students[student_id] = {"name": name, "age": age}
    save_data(students)
    print(f"Student {name} added successfully.")
