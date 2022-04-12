import streamlit as st
import sqlite3
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
            placeholder.empty()
            login_button = True
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
            else:
                    welcome_success = True
                    st.session_state['welcome_success'] =  True

            if welcome_success:
                placeholder3.empty()
                conn = sqlite3.connect('data.db')
                c = conn.cursor()

                c.execute("SELECT * FROM USER_INFO WHERE email = ?", (email,))
                res = c.fetchall()
                data = res[-1]
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
                change_courses  = st.checkbox("Want to change your profile?")
                if change_courses:
                    welcome_app()
                job_confidence = False
                subject_confidence = False
                if subject_conf == 1:
                    subject_confidence == True
                if job_conf == 1:
                    job_confidence == True
                st.title("Home")
                st.header("What is this?")
                st.write("Welcome to your Future Planner, here you will find everything you need to succeed throughout your journey through the IB.")
                st.write("This app is still under development, so please be patient with us.")
                st.header("Where do I go from here?")
                st.write("The information you have provided us with has been sent for review to a counselor. The counselor will choose the best course of action for your IB journey and report back to you as soon as possible. Please be patient!")
                st.header("Your Responses")
                st.write(f"Your HL Subjects are: {hl_subjects}")
                st.write(f"Your SL Subjects are: {sl_subjects}")
                st.write(f"You are confident that you will choose these subjects: {subject_confidence}")
                st.write(f"Your Career Choice is : {job_fam}")
                st.write(f"You are confident about your Career Choice: {job_confidence}")
                st.header("Our Suggestions based on your Responses")
                if "Physics" in hl_subjects and "Math" in hl_subjects:
                    st.write("Your HL Subjects suggest that you would thrive in an Engineering career")
                if "Business Management" in hl_subjects and "Economics" in hl_subjects:
                    st.write("Your HL Subjects suggest that you would thrive in an Accounting or Business Related Career")






def admin():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM user_info")
    st.title("Admin Panel")
    st.header("Student Choices")
    df = pd.DataFrame(c.fetchall(), columns=["email","hl_options", "sl_options", "subject_conf", "career_path", "career_conf"])
    st.write(df)
    hl_subjects = df["hl_options"]
    from collections import defaultdict
    subject_counter = defaultdict(int)
    for x in hl_subjects:
        for y in x.split(","):
            subject_counter[y] += 1
    dframe = pd.DataFrame({'count': subject_counter})
    st.header("HL Subject Counts")
    st.bar_chart(data=dframe, width=0, height=0, use_container_width=True)

    sl_subjects = df["sl_options"]
    subject_counter1 = defaultdict(int)
    for x in sl_subjects:
        for y in x.split(","):
            subject_counter1[y] += 1
    dframe1 = pd.DataFrame({'count': subject_counter1})
    st.header("SL Subject Count")
    st.bar_chart(data=dframe1, width=0, height=0, use_container_width=True)





if __name__ == "__main__":
    app()
