#For database path 
import os

#Get path of the current file folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Builds the full path to the attendance_system.db file
DB_PATH = os.path.join(BASE_DIR, '..', 'database', 'attendance_system.db')

#Folder exists?
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
