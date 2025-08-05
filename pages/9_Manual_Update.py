import streamlit as st
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH

#Logout Button
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


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You must log in to access this page.")
    st.stop()

st.title("Manual Attendance Update")

if st.session_state.get("role") != "faculty":
    st.warning("Access Denied. This page is for faculty only.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

enroll = st.text_input("Enrollment Number")
date = st.date_input("Lecture Date")
lecture = st.text_input("Lecture Number")
new_status = st.selectbox("New Status", ["Present", "Absent"])

if st.button("Update Attendance"):
    cursor.execute("""
        UPDATE Attendance
        SET status=?
        WHERE enrollment_number=? AND date=? AND lecture_no=?
    """, (new_status, enroll, str(date), lecture))
    conn.commit()
    st.success("Attendance updated successfully.")
