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
            st.success("✅ Logged out successfully.")
            with st.spinner("⏳ Redirecting to Login Page"):
                time.sleep(1)
            st.switch_page("pages/2_Login.py")

st.title("Faculty Registration")

admin_code = st.text_input("Enter Admin Code")

if admin_code == "FACULTY2025": #ADMIN CODE TO BE CHANGED
    with st.form("faculty_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO Faculty (name, email, subject, password) VALUES (?, ?, ?, ?)",
                               (name, email, subject, password))
                conn.commit()
                st.success("Faculty Registered Successfully")
            except sqlite3.IntegrityError:
                st.error("Email already exists.")
else:
    st.warning("Please enter a valid Admin Code.")
