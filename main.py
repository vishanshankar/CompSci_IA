import streamlit as st
import sqlite3
import webbrowser
from login import login


def signup_page():
    db = sqlite3.connect('data.db')
    conn = db.cursor()
    st.title("Sign Up")
    st.write("Enter the following information")

    with st.form('Sign-Up'):
        first_name = st.text_input("Enter your first name")
        last_name = st.text_input("Enter your last name")
        email = st.text_input("Enter your email")
        password = st.text_input("Enter your password", type="password")
        password_confirmation = st.text_input("Confirm your password", type="password")
        if password != password_confirmation:
            st.error("Passwords do not match")
        st.checkbox("Are you a Teacher/Faculty")

        button = st.form_submit_button("Submit")
    if button is not None:
        if email != "":
            try:
                conn.execute('INSERT INTO LOGIN VALUES (?,?,?,?)', (email, first_name, last_name, password))
                db.commit()
                db.close()
                st.write("Thank you for your submission")
            except sqlite3.IntegrityError:
                st.error("This user already exists")
def app():
    if 'login' not in st.session_state:
        st.session_state['login'] = False

    placeholder = st.empty()
    with placeholder.container():
        signup_page()

    login_button = st.button("Already have an account? Login.")
    if login_button or st.session_state['login']:
        placeholder.empty()
        login()



if __name__ == "__main__":
    app()
