import streamlit as st
import webbrowser
import sqlite3

def app():
    db = sqlite3.connect('data.db')
    conn = db.cursor()
    st.title("Welcome")
    st.write("We Would Like to get to know you more")
    email = st.session_state['email']
    with st.form('welcome-questionnaire'):
        st.write("What subjects would you be interested in taking (Choose up to 3 in each)")
        hl_options = st.multiselect('Higher Level Subjects',["Math", "English", "Psychology", "Economics", "Business Management", "History", "Spanish", "French", "Hindi", "Tamil", "Physics", "Biology", "Chemistry", "Computer Science", "Environmental Science", "Theatre", "Visual Arts"])
        sl_options = st.multiselect('Standard Level Subjects',["Math", "English", "Psychology", "Economics", "Business Management", "History", "Spanish", "French", "Hindi", "Tamil", "Physics", "Biology", "Chemistry", "Computer Science", "Environmental Science", "Theatre", "Visual Arts"])
        subject_conf = st.checkbox("I am sure that I want to take these courses")
        career_path_options = st.selectbox('Career Paths',["Accounting", "Business", "Engineering", "Law", "Medicine", "Nursing", "Science", "Social Sciences", "Education", "Other"])
        career_conf = st.checkbox("I am sure about my Career Choice")
        st.write("Our System will give you suggestions as well as send your information to a counsellor to help you get a better idea about how to go about your IB journey")
        submit = st.form_submit_button("Submit")
        if submit:

            res = conn.execute("SELECT * FROM USER_INFO WHERE email = ?", (email,)).fetchall()
            st.write
            if len(res) == 0:
                conn.execute('INSERT INTO USER_INFO VALUES (?,?,?,?,?,?)', (email, ",".join(hl_options), ",".join(sl_options), subject_conf, career_path_options, career_conf))
            else:
                conn.execute('DELETE FROM USER_INFO WHERE email = ?', (email,))
                conn.execute('INSERT INTO USER_INFO VALUES (?,?,?,?,?,?)', (email, ",".join(hl_options), ",".join(sl_options), subject_conf, career_path_options, career_conf))
            db.commit()
            db.close()
            st.session_state['welcome_app'] =  True
            return True







if __name__ == "__main__":
    app()
