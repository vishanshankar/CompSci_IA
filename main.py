import streamlit as st
import sqlite3
import webbrowser
from login import login
from welcome import app as welcome_app
import pandas as pd


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
        admin = st.checkbox("Are you a Teacher/Faculty")

        button = st.form_submit_button("Submit")
    if button is not None:
        if email != "":
            try:
                conn.execute('INSERT INTO LOGIN VALUES (?,?,?,?,?)', (email, first_name, last_name, password, admin))
                db.commit()
                db.close()
                st.write("Thank you for your submission")
                return True
            except sqlite3.IntegrityError:
                st.error("This user already exists")
def app():
    if 'login' not in st.session_state:
        st.session_state['login'] = False

    if 'login_success' not in st.session_state:
        st.session_state['login_success'] = False

    if 'email' not in st.session_state:
        st.session_state['email'] =  None

    if 'welcome_success' not in st.session_state:
        st.session_state['welcome_success'] =  False



    login_success = st.session_state["login_success"]
    email = st.session_state["email"]
    welcome_success = st.session_state["welcome_success"]
    placeholder = st.empty()
    placeholder2 = st.empty()
    placeholder3 = st.empty()
    if not login_success:
        with placeholder.container():
            signup_success = signup_page()
            login_button = st.button("Already have an account? Login.")
        if signup_success:
            placeholder.empty() login_button = True
        placeholder2 = st.empty()
        with placeholder2.container():
            if login_button or st.session_state['login']:
                placeholder.empty()
                login_success = login()
                st.session_state['login_success'] = login_success
                email = st.session_state["email"]

    if login_success:
        if placeholder2 is not None:
            placeholder2.empty()
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("SELECT admin  FROM LOGIN WHERE email = ?", (email,))
        res0 = c.fetchall()[0][0]
        if res0:
            admin()
        else:
            c.execute("SELECT * FROM USER_INFO WHERE email = ?", (email,))
            res = c.fetchall()
            if len(res) == 0:
                with placeholder3.container():
                    welcome_success = welcome_app()
                    st.session_state['welcome_success'] =  welcome_success
            if welcome_success:
                placeholder3.empty()
                conn = sqlite3.connect('data.db')
                c = conn.cursor()
                c.execute("SELECT * FROM USER_INFO WHERE email = ?", (email,))
                res = c.fetchall()
                data = res[0]
                hl_subjects = data[1].split(",")
                sl_subjects = data[2].split(",")
                subject_conf = data[3]
                job_fam = data[4]
                job_conf = data[5]
                st.write(f"Your HL Subjects are: {hl_subjects}")
                st.write(f"Your SL Subjects are: {sl_subjects}")
                st.write(f"Your SUBJECT_CONF is: {subject_conf}")
                st.write(f"Your job_fam is : {job_fam}")
                st.write(f"Your job_conf is: {job_conf}")



def admin():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_info")
    st.markdown("# Admin Panel")
    df = pd.DataFrame(c.fetchall(), columns=["email","hl_options", "sl_options", "subject_conf", "career_path", "career_conf"])
    st.write(df)




if __name__ == "__main__":
    app()
