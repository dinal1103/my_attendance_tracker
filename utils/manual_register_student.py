#For reference data to check working of UI
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

students = [
    ('230280152043', 'Dinal Patel', 5, 2025, 'Female'),
    ('230280152051', 'Vrutti Patel', 5, 2025, 'Female'),
    ('230280152057', 'Drashti Rathod', 5, 2025, 'Female'),
    ('230280152046', 'Priya Singh', 5, 2023, 'Female'),
]

for student in students:
    try:
        cursor.execute('''
            INSERT INTO Student (enrollment_number, name, semester, year, sex, face_encoding)
            VALUES (?, ?, ?, ?, ?, NULL)
        ''', student)
    except sqlite3.IntegrityError:
        print(f"Student {student[0]} already exist skipping...")
    else:
        print(f"Added student: {student[1]} ({student[0]})")

faculties = [
    ("Dr. Sharma", "sharma@college.edu", "AI", "admin123"),
    ("Prof. Mehta", "mehta@college.edu", "ML", "mehta456"),
    ("Dr. Iyer", "iyer@college.edu", "DS", "iyer789"),
]

for faculty in faculties:
    try:
        cursor.execute('''
            INSERT INTO Faculty (name, email, subject, password)
            VALUES (?, ?, ?, ?)
        ''', faculty)
    except sqlite3.IntegrityError:
        print(f"Faculty {faculty[1]} already exist skipping...")
    else:
        print(f"Added faculty: {faculty[0]} ({faculty[1]})")

conn.commit()
conn.close()

print("Students and Faculty inserted into database")
