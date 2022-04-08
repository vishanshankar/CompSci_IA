import webbrowser
import streamlit as st
import sqlite3
from welcome import app

def login():
    st.session_state.login = True
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    login_form = st.form("Login")
    email = login_form.text_input("E-mail")
    password = login_form.text_input("Password", type="password")
    login_button = login_form.form_submit_button("submit")
    print("potato", email,password,login_button)
    if login_button is not None:
        user = []
        c.execute("SELECT * FROM LOGIN WHERE email = ? AND password = ?", (email, password))
        user = c.fetchall()
        if user:
            st.session_state['name'] =user[0][1]
            st.session_state['email'] = email
            authenticated = True
            st.success("Login Successful")
            print("returning true.....")
            return True
        else:
            st.error("Login Failed")
            return False

if __name__ == "__main__":
    login()
