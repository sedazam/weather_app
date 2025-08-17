import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Weather",
    page_icon="🌤️",
    layout="centered"
)

# API configuration
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5"

# Check if API key is loaded
if not API_KEY:
    st.error("⚠️ OpenWeatherMap API key not found! Please check your .env file.")
    st.stop()

def get_coordinates(city_name):
    """Get coordinates for a city using OpenWeatherMap Geocoding API"""
    geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': city_name,
        'limit': 1,
        'appid': API_KEY
    }
    
    try:
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return data[0]['lat'], data[0]['lon'], data[0]['name']
        else:
            return None, None, None
    except requests.exceptions.RequestException:
        return None, None, None

def get_current_weather(lat, lon):
    """Get current weather using coordinates"""
    current_url = f"{BASE_URL}/weather"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(current_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching current weather: {e}")
        return None

# Main app
st.title("🌤️ Weather App")

# Search input
city_input = st.text_input("Enter city name", placeholder="e.g., London, New York, Tokyo")

if city_input:
    with st.spinner("Getting weather data..."):
        lat, lon, city_name = get_coordinates(city_input)
        
        if lat and lon:
            current_weather = get_current_weather(lat, lon)
            
            if current_weather:
                st.success(f"Weather data loaded for {city_name}")
                
                # Display weather
                temp = current_weather['main']['temp']
                feels_like = current_weather['main']['feels_like']
                humidity = current_weather['main']['humidity']
                description = current_weather['weather'][0]['description']
                
                st.subheader(f"Current Weather in {city_name}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Temperature", f"{temp:.1f}°C", f"Feels like {feels_like:.1f}°C")
                
                with col2:
                    st.metric("Humidity", f"{humidity}%")
                
                with col3:
                    st.metric("Condition", description.title())
                    
            else:
                st.error("Failed to fetch weather data")
        else:
            st.error("City not found. Please try again.")
else:
    st.info("Enter a city name to get weather information")
