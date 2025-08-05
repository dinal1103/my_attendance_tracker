import streamlit as st
from datetime import datetime

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


st.title("Upload Classroom Photo - Attendance")

if st.session_state.get("role") != "faculty":
    st.warning("Access Denied. This page is for faculty only.")
    st.stop()

# Upload photo
uploaded_photo = st.file_uploader("Upload classroom photo", type=["jpg", "jpeg", "png"])

with st.form("upload_form"):
    subject = st.text_input("Subject")
    lecture_no = st.text_input("Lecture Number")
    submit = st.form_submit_button("Submit")

if uploaded_photo and submit:
    st.success("Photo uploaded successfully.")

    #for processing face recognition
    
