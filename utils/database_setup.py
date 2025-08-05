import sqlite3
import sys
import os

# Add project root to sys.path BEFORE any local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

#Student table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Student (
    enrollment_number TEXT PRIMARY KEY,
    name TEXT,
    semester INTEGER,
    year INTEGER,
    sex TEXT,
    face_encoding BLOB
)
''')

#Attendance table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_number TEXT,
    date TEXT,
    time TEXT,
    subject TEXT,
    faculty TEXT,
    lecture_no INTEGER,
    status TEXT DEFAULT "Present",
    FOREIGN KEY (enrollment_number) REFERENCES Student(enrollment_number)
)
''')

#Error report table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Error_Report (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    enrollment_number TEXT,
    date TEXT,
    time TEXT,
    subject TEXT,
    issue TEXT,
    FOREIGN KEY (enrollment_number) REFERENCES Student(enrollment_number)
)
''')

# Faculty table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT UNIQUE,
    subject TEXT
)
''')

#password column
try:
    cursor.execute("ALTER TABLE Faculty ADD COLUMN password TEXT")
except sqlite3.OperationalError as e:
    print(f"Password column already exist: {e}")

conn.commit()
conn.close()

print(f"Database and all tables created at: {DB_PATH}")
