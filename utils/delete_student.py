#To manually delete student and faculty
import sqlite3
import shutil
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

#Either 'student' or 'faculty'
role_to_delete = 'student'
#role_to_delete = 'faculty'

#Identifier:
#For student: use enrollment number
#For faculty: use email
identifier = '230280152051'
#identifier = 'dnlpatel1104@gmail.com'

if role_to_delete.lower() == 'student':
    enrollment_number = identifier

    cursor.execute("DELETE FROM Attendance WHERE enrollment_number = ?", (enrollment_number,))
    cursor.execute("DELETE FROM Error_Report WHERE enrollment_number = ?", (enrollment_number,))
    cursor.execute("DELETE FROM Student WHERE enrollment_number = ?", (enrollment_number,))

    image_folder_path = os.path.join('student_images', enrollment_number)
    if os.path.exists(image_folder_path):
        try:
            shutil.rmtree(image_folder_path)
            print(f"Deleted student image folder: {image_folder_path}")
        except Exception as e:
            print(f"Failed to delete student folder: {image_folder_path}: {e}")
    else:
        print(f"No image folder found for student: {enrollment_number}")

    print(f"Student {enrollment_number} deleted")

elif role_to_delete.lower() == 'faculty':
    faculty_email = identifier
    cursor.execute("DELETE FROM Faculty WHERE email = ?", (faculty_email,))
    print(f"Faculty with email {faculty_email} deleted")

else:
    print("Invalid role specified. Use 'student' or 'faculty'")

conn.commit()
conn.close()
print("Deletion process completed.")



