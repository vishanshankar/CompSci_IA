import streamlit as st
import webbrowser
import sqlite3

def app():
    db = sqlite3.connect('data.db')
    conn = db.cursor()
    st.title("Welcome")
    st.write("We Would Like to get to know you more")
    with st.form('welcome-questionnaire'):
        st.write("What subjects would you be interested in taking (Choose up to 3 in each)")
        hl_options = st.multiselect('Higher Level Subjects',["Math", "English", "Psychology", "Economics", "Business Management", "History", "Spanish", "French", "Hindi", "Tamil", "Physics", "Biology", "Chemistry", "Computer Science", "Environmental Science", "Theatre", "Visual Arts"])
        sl_options = st.multiselect('Standard Level Subjects',["Math", "English", "Psychology", "Economics", "Business Management", "History", "Spanish", "French", "Hindi", "Tamil", "Physics", "Biology", "Chemistry", "Computer Science", "Environmental Science", "Theatre", "Visual Arts"])
        subject_conf = st.checkbox("I don't know what subjects I want to take in IB")
        career_path_options = st.multiselect('Career Paths',["Accounting", "Business", "Engineering", "Law", "Medicine", "Nursing", "Science", "Social Sciences", "Education", "Other"])
        career_conf = st.checkbox("I don't know what career path I want to pursue")
        st.write("Our System will give you suggestions as well as send your information to a counsellor to help you get a better idea about how to go about your IB journey")
        submit = st.form_submit_button("Submit")





if __name__ == "__main__":
    app()
