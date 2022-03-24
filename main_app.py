import streamlit as st
import login, main, home

PAGES = {
    "login": login,
    "signup": main,
    "home": home
}
st.sidebar.title('Navigation')
selection = st.sidebar.selectbox("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
