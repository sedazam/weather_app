import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import pandas as pd

# Load API key from environment
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Set page configuration
st.set_page_config(
    page_title="Weather",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for modern weather app design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #4A90E2 0%, #5BA3F5 50%, #87CEEB 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    }
    
    .main-weather-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }
    
    .city-title {
        font-size: 2.5rem;
        font-weight: 300;
        color: white;
        margin-bottom: 0.2rem;
    }
    
    .weather-condition {
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 0.5rem;
    }
    
    .temp-range {
        font-size: 1rem;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 1rem;
    }
    
    .current-temp {
        font-size: 5rem;
        font-weight: 200;
        color: white;
        margin: 0;
        line-height: 1;
    }
    
    .hourly-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .hourly-item {
        text-align: center;
        color: white;
        padding: 0.5rem;
        margin: 0 0.2rem;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.1);
        min-width: 80px;
    }
    
    .forecast-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    }
    
    .forecast-day {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        color: white;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .weather-details {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        color: white;
    }
    
    .detail-item {
        display: flex;
        justify-content: space-between;
        padding: 0.3rem 0;
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 1rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
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
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

def get_weather_icon(condition):
    """Get weather icon based on condition"""
    icons = {
        'clear': '☀️',
        'clouds': '☁️',
        'rain': '🌧️',
        'drizzle': '🌦️',
        'thunderstorm': '⛈️',
        'snow': '❄️',
        'mist': '🌫️',
        'fog': '🌫️',
        'haze': '🌫️'
    }
    for key, icon in icons.items():
        if key in condition.lower():
            return icon
    return '🌤️'

def get_forecast_data(lat, lon):
    """Get 5-day forecast data"""
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Search container
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    city = st.text_input("Search for a city", placeholder="Enter city name", label_visibility="collapsed")
with col2:
    search_btn = st.button("Search")
st.markdown('</div>', unsafe_allow_html=True)

if city:
    if not API_KEY:
        st.error("⚠️ API key not found! Please add OPENWEATHER_API_KEY to your .env file")
    else:
        # Make API request
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Display weather information
            st.success(f"✅ Weather data for {data['name']}, {data['sys']['country']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Temperature", f"{data['main']['temp']:.1f}°C", f"Feels like {data['main']['feels_like']:.1f}°C")
                st.metric("Humidity", f"{data['main']['humidity']}%")
            
            with col2:
                st.metric("Weather", data['weather'][0]['description'].title())
                st.metric("Wind Speed", f"{data['wind']['speed']} m/s")
            
            # Additional info
            st.subheader("Additional Information")
            st.write(f"**Pressure:** {data['main']['pressure']} hPa")
            st.write(f"**Visibility:** {data.get('visibility', 'N/A')} meters")
            st.write(f"**Cloudiness:** {data['clouds']['all']}%")
            
        except requests.exceptions.RequestException:
            st.error("❌ City not found or API error. Please check the city name and try again.")
        except KeyError:
            st.error("❌ Unexpected response format from weather API.")

else:
    st.info("👆 Please enter a city name above to get weather information")

# Footer
st.markdown("---")
st.caption("Powered by OpenWeatherMap API")