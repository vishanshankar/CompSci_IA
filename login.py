import webbrowser
import streamlit as st
import sqlite3
import main_app

def app():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    st.session_state['name'] = None
    with st.form("Login"):
        email = st.text_input("E-mail")
        password = st.text_input("Password", type="password")
        c.execute("SELECT * FROM LOGIN WHERE email = ? AND password = ?", (email, password))
        button = st.form_submit_button("Login")
        user = []
        user = c.fetchall()
        if user:
            st.session_state['name'] =user[0][1]
            authenticated = True
            st.success("Login Successful")
            st.write(st.session_state['name'])
            if button:
                main_app.PAGES["home"]
        else:
            st.error("Login Failed")

if __name__ == "__main__":
    app()