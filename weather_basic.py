import streamlit as st

# Page config
st.set_page_config(
    page_title="Weather",
    page_icon="🌤️",
    layout="centered"
)

# Simple CSS for Android-style design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .title {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 20px;
        padding: 0.75rem 1rem;
        color: #333;
        font-size: 1rem;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.75rem 2rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Main app
st.markdown('<div class="title">🌤️ Android Weather</div>', unsafe_allow_html=True)

st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.write("### Welcome to your Android-style Weather App!")
st.write("This is working! The beautiful gradient background and glass effects are applied.")

city = st.text_input("Enter a city name", placeholder="e.g., London, New York")

if st.button("Get Weather"):
    if city:
        st.success(f"You searched for: {city}")
        st.write("🌟 The app is working! Next step: Add weather API integration.")
    else:
        st.warning("Please enter a city name")

st.write("---")
st.write("✨ **Android-style features:**")
st.write("- Glass morphism background")
st.write("- Purple gradient design")  
st.write("- Rounded input fields")
st.write("- Modern typography")

st.markdown('</div>', unsafe_allow_html=True)
