import streamlit as st
import sqlite3
import sys
import os
import re
import time
from PIL import Image

# Add root path for db_config import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_config import DB_PATH

# Sidebar Logout (if logged in)
if st.session_state.get("logged_in"):
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state.get('role').capitalize()}`")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.pop("enroll", None)
            st.session_state.pop("faculty_name", None)
            st.success("✅ Logged out successfully.")
            with st.spinner("⏳ Redirecting to Login Page"):
                time.sleep(1)
            st.switch_page("pages/2_Login.py")


# Page Title
st.title("📝 Student Registration")


#Student registration form
with st.form("student_form"):
    name = st.text_input("🧑‍💼 Full Name")
    enroll = st.text_input("🆔 Enrollment Number")
    sex = st.selectbox("⚧️ Select Gender", options=["Male", "Female"])
    year = st.selectbox("🎓 Select Year", options=["1st", "2nd", "3rd", "4th"],index=2)
    semester = st.selectbox("📘 Select Semester (1-8)", options=list(range(1, 9)),index=4)
    st.info("📸 Upload at least 3 clear face images.")
    images = st.file_uploader("🖼️ Upload at least 3 Images", type=["jpg", "jpeg"], accept_multiple_files=True)

    submitted = st.form_submit_button("📩 Register")

if submitted:

    if not name:
        st.error("❗ Full name is required.")
    elif not re.match(r"^[A-Za-z\s]+$", name):
        st.error("❗ Name must contain only alphabets and spaces.")
    elif not enroll.strip().isdigit():
        st.error("❗ Enrollment number must contain digits only.")
    elif len(images) < 3:
        st.warning("❗ Please upload at least 3 face images.")
    else:
        name = ' '.join([part.capitalize() for part in name.strip().split()])
        enroll = enroll.strip()  # Clean spaces
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if enrollment number already exists
        cursor.execute("SELECT 1 FROM Student WHERE enrollment_number = ?", (enroll,))
        if cursor.fetchone():
            st.error("❗ Student already exists with this enrollment number.")
        else:
            # Create folder to save student images
            folder = f"student_images/{enroll}"
            os.makedirs(folder, exist_ok=True)
            
            for i, img in enumerate(images):
                img_path = f"{folder}/{enroll}-{i+1}.jpg"
                with open(img_path, "wb") as f:
                    f.write(img.read())

            # Insert student details into database
            cursor.execute("""
                INSERT INTO Student (enrollment_number, name, semester, year, sex) 
                VALUES (?, ?, ?, ?, ?)
            """, (enroll, name, semester, year, sex))
            conn.commit()
            st.success("✅ Student Registered Successfully.")

            with st.spinner("⏳ Redirecting to Login Page in 2 seconds..."):
                time.sleep(2)
            st.switch_page("pages/2_Login.py")
            

        conn.close()
