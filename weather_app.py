import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Weather",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Android-style sleek design
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
    
    .weather-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        text-align: center;
        color: white;
    }
    
    .current-temp {
        font-size: 4rem;
        font-weight: 300;
        color: white;
        margin: 0;
        line-height: 1;
    }
    
    .city-name {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0.5rem;
    }
    
    .weather-desc {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
    }
    
    .forecast-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        color: white;
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        padding: 1rem;
        margin-bottom: 2rem;
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
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Custom title styling */
    .main-title {
        text-align: center;
        color: white;
        font-size: 2rem;
        font-weight: 300;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# API configuration
# Using OpenWeatherMap API (free tier allows 1000 calls/day)
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

def get_weather_forecast(lat, lon):
    """Get 5-day weather forecast using coordinates"""
    forecast_url = f"{BASE_URL}/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(forecast_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

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

def format_weather_data(weather_data):
    """Format weather data for display"""
    if not weather_data:
        return None
    
    daily_data = []
    current_date = None
    daily_temps = []
    
    # Group hourly data by day
    for item in weather_data['list']:
        date = datetime.fromtimestamp(item['dt'])
        date_str = date.strftime('%Y-%m-%d')
        
        if current_date != date_str:
            # Save previous day's data
            if daily_temps:
                daily_data.append({
                    'Date': current_date,
                    'Day': datetime.strptime(current_date, '%Y-%m-%d').strftime('%A'),
                    'Temperature (°C)': f"{min(daily_temps):.1f} - {max(daily_temps):.1f}",
                    'Min Temp': min(daily_temps),
                    'Max Temp': max(daily_temps),
                    'Description': daily_desc,
                    'Humidity (%)': daily_humidity,
                    'Wind Speed (m/s)': daily_wind,
                    'Icon': daily_icon
                })
            
            # Start new day
            current_date = date_str
            daily_temps = [item['main']['temp']]
            daily_desc = item['weather'][0]['description'].title()
            daily_humidity = item['main']['humidity']
            daily_wind = item['wind']['speed']
            daily_icon = item['weather'][0]['icon']
        else:
            daily_temps.append(item['main']['temp'])
    
    # Add the last day
    if daily_temps:
        daily_data.append({
            'Date': current_date,
            'Day': datetime.strptime(current_date, '%Y-%m-%d').strftime('%A'),
            'Temperature (°C)': f"{min(daily_temps):.1f} - {max(daily_temps):.1f}",
            'Min Temp': min(daily_temps),
            'Max Temp': max(daily_temps),
            'Description': daily_desc,
            'Humidity (%)': daily_humidity,
            'Wind Speed (m/s)': daily_wind,
            'Icon': daily_icon
        })
    
    return pd.DataFrame(daily_data)

def get_weather_emoji(icon_code):
    """Get emoji based on weather icon code"""
    icon_map = {
        '01d': '☀️', '01n': '🌙',
        '02d': '⛅', '02n': '☁️',
        '03d': '☁️', '03n': '☁️',
        '04d': '☁️', '04n': '☁️',
        '09d': '🌧️', '09n': '🌧️',
        '10d': '🌦️', '10n': '🌧️',
        '11d': '⛈️', '11n': '⛈️',
        '13d': '❄️', '13n': '❄️',
        '50d': '🌫️', '50n': '🌫️'
    }
    return icon_map.get(icon_code, '🌤️')

# Main app
st.markdown('<h1 class="main-title">🌤️ Weather</h1>', unsafe_allow_html=True)

# Search container
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    city_input = st.text_input("", placeholder="Search for a city...", label_visibility="collapsed")

with col2:
    search_button = st.button("🔍", help="Get weather")

st.markdown('</div>', unsafe_allow_html=True)

# Handle search
if search_button and city_input:
    with st.spinner("🌍 Getting weather data..."):
        lat, lon, city_name = get_coordinates(city_input)
        
        if lat and lon:
            current_weather = get_current_weather(lat, lon)
            weather_forecast = get_weather_forecast(lat, lon)
            
            if current_weather and weather_forecast:
                st.session_state['current_weather'] = current_weather
                st.session_state['weather_forecast'] = weather_forecast
                st.session_state['city_name'] = city_name
                st.rerun()
            else:
                st.error("❌ Failed to fetch weather data")
        else:
            st.error("❌ City not found. Try again with a different spelling.")

# Main content area
if 'current_weather' in st.session_state and 'weather_forecast' in st.session_state:
    current_weather = st.session_state['current_weather']
    weather_forecast = st.session_state['weather_forecast']
    city_name = st.session_state['city_name']
    
    # Current weather - Main card
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # City and current temperature
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<div class="city-name">📍 {city_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="current-temp">{current_weather["main"]["temp"]:.0f}°</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="weather-desc">{current_weather["weather"][0]["description"].title()} {get_weather_emoji(current_weather["weather"][0]["icon"])}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="weather-card">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{get_weather_emoji(current_weather['weather'][0]['icon'])}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Feels like {current_weather['main']['feels_like']:.0f}°</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key metrics in a clean row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">💧</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{current_weather['main']['humidity']}%</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Humidity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">💨</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{current_weather['wind']['speed']:.1f}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Wind m/s</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">🌡️</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{current_weather['main']['pressure']}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Pressure</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        visibility = current_weather.get('visibility', 0) / 1000 if current_weather.get('visibility') else 0
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">👁️</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{visibility:.1f}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Visibility km</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 5-day forecast - Minimal horizontal scroll
    st.markdown('<div style="margin-top: 2rem; color: white;"><h3 style="color: white; font-weight: 300;">5-Day Forecast</h3></div>', unsafe_allow_html=True)
    
    df = format_weather_data(weather_forecast)
    
    if df is not None and len(df) > 0:
        cols = st.columns(min(5, len(df)))
        for i, col in enumerate(cols):
            if i < len(df):
                row = df.iloc[i]
                with col:
                    day_name = row['Day'][:3]  # Abbreviated day name
                    st.markdown(f"""
                    <div class="forecast-item">
                        <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem;">{day_name}</div>
                        <div style="font-size: 2rem; margin: 0.5rem 0;">{get_weather_emoji(row['Icon'])}</div>
                        <div style="font-size: 1rem; font-weight: 500;">{row['Max Temp']:.0f}°</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">{row['Min Temp']:.0f}°</div>
                    </div>
                    """, unsafe_allow_html=True)

else:
    # Welcome message - Minimal and clean
    st.markdown("""
    <div class="main-container" style="text-align: center; color: white;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌤️</div>
        <h2 style="color: white; font-weight: 300; margin-bottom: 1rem;">Weather App</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">Search for any city to get current weather and 5-day forecast</p>
    </div>
    """, unsafe_allow_html=True)