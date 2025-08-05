import streamlit as st
import pandas as pd
import sqlite3
import sys
import os

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
            st.session_state.page = "Home"
            st.success("Logged out successfully.")
            st.stop()


if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ You must log in to access this page.")
    st.stop()


st.title("Attendance Report")

conn = sqlite3.connect(DB_PATH)

date = st.date_input("Select Date")
lecture_no = st.text_input("Lecture Number")

if st.button("Get Attendance Report"):
    query = """
        SELECT s.enrollment_number, s.name, a.date, a.time, a.subject, a.faculty, a.lecture_no, a.status
        FROM Attendance a
        JOIN Student s ON a.enrollment_number = s.enrollment_number
        WHERE a.date = ? AND a.lecture_no = ?
        ORDER BY s.enrollment_number
    """
    df = pd.read_sql_query(query, conn, params=(str(date), lecture_no))
    if not df.empty:
        st.dataframe(df)
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, file_name=f"attendance_{date}_{lecture_no}.csv")
    else:
        st.warning("No attendance found for selected date and lecture.")
