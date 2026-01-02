from load_save_data import save_data

def delete_student(students):
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("ID must be a number.")
        return

    if student_id in students:
        name = students[student_id]["name"]
        del students[student_id]
        save_data(students)
        print(f"Student {name} deleted.")
    else:
        print("ID not found.")
