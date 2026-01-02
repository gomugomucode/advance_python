def view_all(students):
    if not students:
        print("No students found.")
        return

    print("\n--- STUDENT RECORDS ---")
    print("ID | Name | Age")
    print("-----------------")
    for sid, info in students.items():
        print(f"{sid} | {info['name']} | {info['age']}")
