import streamlit as st
import pandas as pd
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
            st.success("✅ Logged out successfully.")
            with st.spinner("⏳ Redirecting to Login Page"):
                time.sleep(1)
            st.switch_page("pages/2_Login.py")


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You must log in to access this page.")
    st.stop()


st.title("View My Attendance")

if st.session_state.get("role") != "student":
    st.warning("Access Denied. This page is for students only.")
    st.stop()

conn = sqlite3.connect(DB_PATH)
enroll = st.session_state.get("enroll")

query = "SELECT date, time, subject, faculty, lecture_no, status FROM Attendance WHERE enrollment_number = ? ORDER BY date"
df = pd.read_sql_query(query, conn, params=(enroll,))

if not df.empty:
    st.dataframe(df)

    total_lectures = df.shape[0]
    present_lectures = df[df["status"] == "Present"].shape[0]
    percent = round((present_lectures / total_lectures) * 100, 2)

    st.info(f"Total Lectures: {total_lectures}")
    st.info(f"Present: {present_lectures}")
    st.success(f"Attendance Percentage: {percent}%")
else:
    st.warning("No attendance records found.")
