import streamlit as st
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.db_config import DB_PATH
from datetime import date

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


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You must log in to access this page.")
    st.stop()


st.title("Report Attendance Error")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with st.form("error_form"):
    enroll = st.text_input("Enrollment Number")
    subject = st.text_input("Subject")
    lec_date = st.date_input("Date")
    lecture_no = st.text_input("Lecture Number")
    issue = st.text_area("Describe your issue")
    submit = st.form_submit_button("Submit")

if submit:
    cursor.execute("""
        INSERT INTO Error_Report (enrollment_number, date, time, subject, issue)
        VALUES (?, ?, time('now'), ?, ?)
    """, (enroll, str(lec_date), subject, issue))
    conn.commit()
    st.success("Issue submitted successfully.")

