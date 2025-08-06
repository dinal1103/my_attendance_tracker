#For viewing database
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT * FROM Student")
#cursor.execute("SELECT * FROM Attendance")
#cursor.execute("SELECT * FROM Error_Report")
#cursor.execute("SELECT * FROM Faculty")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
