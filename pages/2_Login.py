import streamlit as st
import sqlite3
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

#Logout button
if st.session_state.get("logged_in"):
    with st.sidebar:
        st.markdown(f"**Logged in as:** `{st.session_state.get('role').capitalize()}`")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.session_state.pop("enroll", None)
            st.session_state.pop("faculty_name", None)
            st.session_state.pop("faculty_email", None)
            st.success("✅ Logged out successfully.")
            with st.spinner("⏳ Redirecting"):
                time.sleep(1)
            st.switch_page("pages/2_Login.py")

st.set_page_config(page_title="Login - AI Attendance System", layout="centered")
st.title("🔐 Login")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

role = st.selectbox("Select Role", ["Student", "Faculty"])

if role == "Student":
    enroll = st.text_input("Enrollment Number")
    name = st.text_input("Name")

    if st.button("Login"):
        cursor.execute("""
            SELECT * FROM Student 
            WHERE enrollment_number=? 
            AND REPLACE(LOWER(name), ' ', '') = REPLACE(LOWER(?), ' ', '')
            """, (enroll, name))
        result = cursor.fetchone()

        if result:
            st.success("✅ Student Login Successful")
            st.session_state.logged_in = True
            st.session_state.role = "student"
            st.session_state.enroll = enroll
            st.switch_page("pages/7_View_Attendance.py")
        else:
            st.error("❌ Invalid student credentials.")


elif role == "Faculty":
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        cursor.execute("SELECT * FROM Faculty WHERE email=? AND password=?", (email, password))
        result = cursor.fetchone()

        if result:
            st.success("✅ Faculty Login Successful")
            st.session_state.logged_in = True
            st.session_state.role = "faculty"
            st.session_state.faculty_name = result[1]     
            st.session_state.faculty_email = email        
            st.switch_page("pages/5_Upload_class_Photo.py")
        else:
            st.error("❌ Invalid faculty credentials.")


conn.commit()
conn.close()
