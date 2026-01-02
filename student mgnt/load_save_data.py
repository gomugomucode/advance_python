import json
import os

FILE_NAME = "student_data.json"

def load_data():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return {}  # Empty dict if file corrupted
    return {}  # File doesn't exist

def save_data(students):
    with open(FILE_NAME, "w") as file:  # overwrite old data
        json.dump(students, file, indent=4)
