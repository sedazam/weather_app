import streamlit as st

st.title("🌤️ Weather Test")
st.write("Hello! This is a test to make sure Streamlit is working.")

name = st.text_input("Enter your name")
if name:
    st.write(f"Hello {name}!")

st.write("If you can see this, Streamlit is working correctly!")
