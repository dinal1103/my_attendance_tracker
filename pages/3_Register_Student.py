import streamlit as st
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH
from PIL import Image

#Logout button
if st.session_state.get("logged_in"):
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state.get('role').capitalize()}`")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.pop("enroll", None)
            st.session_state.pop("faculty_name", None)
            st.session_state.page = "Home"
            st.success("Logged out successfully.")
            st.stop()

st.title("Student Registration")

#Student registration form
with st.form("student_form"):
    name = st.text_input("Name")
    enroll = st.text_input("Enrollment Number")
    semester = st.selectbox("Semester", list(range(1, 9)))
    year = st.selectbox("Year", ["1st", "2nd", "3rd", "4th"])
    sex = st.selectbox("Sex", ["Male", "Female", "Other"])
    images = st.file_uploader("Upload at least 3 Images", type=["jpg", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("Register")

if submitted:

    if len(images) < 3:
        st.warning("Please upload at least 3 images.")
    else:
        folder = f"student_images/{enroll}"
        os.makedirs(folder, exist_ok=True)

        for i, img in enumerate(images):
            with open(f"{folder}/{enroll}-{i+1}.jpg", "wb") as f:
                f.write(img.read())

        # Add student details to database (face encoding handled separately later)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Student (enrollment_number, name, semester, year, sex) VALUES (?, ?, ?, ?, ?)",
                       (enroll, name, semester, year, sex))
        conn.commit()

        st.success("Student Registered Successfully")
