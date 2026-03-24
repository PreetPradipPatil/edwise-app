import streamlit as st

st.title("Main App")

if "redirected" not in st.session_state:
    st.session_state.redirected = True
    st.switch_page("pages/1_Student_Verification.py")