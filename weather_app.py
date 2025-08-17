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
        position: relative;
        overflow: hidden;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .city-image-container {
        position: relative;
        border-radius: 15px;
        overflow: hidden;
        margin-bottom: 1rem;
        height: 200px;
        background: rgba(255, 255, 255, 0.1);
    }
    
    .city-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 15px;
        opacity: 0.8;
    }
    
    .city-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, rgba(0,0,0,0.3), rgba(0,0,0,0.1));
        display: flex;
        align-items: flex-end;
        padding: 1rem;
        border-radius: 15px;
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
        position: relative;
        overflow: hidden;
    }
    
    .current-temp {
        font-size: 4rem;
        font-weight: 300;
        color: white;
        margin: 0;
        line-height: 1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .city-name {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 0.5rem;
        text-shadow: 0 1px 5px rgba(0,0,0,0.5);
    }
    
    .weather-desc {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 1rem;
        text-shadow: 0 1px 3px rgba(0,0,0,0.3);
    }
    
    .forecast-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .forecast-item:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        color: white;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .metric-container:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.2);
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    
    /* Weather particles */
    .weather-particles {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        overflow: hidden;
    }
    
    /* Floating weather icons */
    .floating-icon {
        position: absolute;
        font-size: 2rem;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(180deg); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .weather-icon-large {
        animation: pulse 3s ease-in-out infinite;
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
    
    /* Temperature gradient based on value */
    .temp-hot { color: #ff6b6b; }
    .temp-warm { color: #feca57; }
    .temp-cool { color: #48dbfb; }
    .temp-cold { color: #0abde3; }
    .temp-freezing { color: #006ba6; }
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

def get_weather_background(weather_condition, is_day=True):
    """Get dynamic background based on weather condition"""
    if 'clear' in weather_condition.lower():
        if is_day:
            return "linear-gradient(135deg, #74b9ff 0%, #0984e3 50%, #fdcb6e 100%)"  # Sunny
        else:
            return "linear-gradient(135deg, #2d3436 0%, #636e72 50%, #74b9ff 100%)"  # Clear night
    elif 'cloud' in weather_condition.lower():
        return "linear-gradient(135deg, #636e72 0%, #74b9ff 50%, #ddd 100%)"  # Cloudy
    elif 'rain' in weather_condition.lower() or 'drizzle' in weather_condition.lower():
        return "linear-gradient(135deg, #2d3436 0%, #636e72 50%, #74b9ff 100%)"  # Rainy
    elif 'thunder' in weather_condition.lower() or 'storm' in weather_condition.lower():
        return "linear-gradient(135deg, #2d3436 0%, #636e72 30%, #e17055 100%)"  # Stormy
    elif 'snow' in weather_condition.lower():
        return "linear-gradient(135deg, #ddd 0%, #74b9ff 50%, #fff 100%)"  # Snow
    elif 'mist' in weather_condition.lower() or 'fog' in weather_condition.lower():
        return "linear-gradient(135deg, #636e72 0%, #ddd 50%, #b2bec3 100%)"  # Misty
    else:
        return "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"  # Default

def get_weather_animation(weather_condition):
    """Get CSS animation based on weather condition"""
    animations = {
        'clear': """
        @keyframes sunshine {
            0%, 100% { transform: rotate(0deg); }
            50% { transform: rotate(180deg); }
        }
        .weather-animation { animation: sunshine 20s linear infinite; }
        """,
        'rain': """
        @keyframes raindrops {
            0% { transform: translateY(-100vh) rotate(10deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(10deg); opacity: 0; }
        }
        .weather-animation::before {
            content: '💧';
            position: absolute;
            animation: raindrops 1s linear infinite;
            font-size: 1rem;
            left: 10%;
        }
        .weather-animation::after {
            content: '💧';
            position: absolute;
            animation: raindrops 1.5s linear infinite;
            font-size: 1rem;
            left: 80%;
            animation-delay: 0.5s;
        }
        """,
        'snow': """
        @keyframes snowfall {
            0% { transform: translateY(-100vh) rotate(0deg); opacity: 1; }
            100% { transform: translateY(100vh) rotate(360deg); opacity: 0; }
        }
        .weather-animation::before {
            content: '❄️';
            position: absolute;
            animation: snowfall 3s linear infinite;
            font-size: 1rem;
            left: 20%;
        }
        .weather-animation::after {
            content: '❄️';
            position: absolute;
            animation: snowfall 4s linear infinite;
            font-size: 1rem;
            left: 70%;
            animation-delay: 1s;
        }
        """,
        'cloud': """
        @keyframes float {
            0%, 100% { transform: translateX(0px) translateY(0px); }
            33% { transform: translateX(30px) translateY(-10px); }
            66% { transform: translateX(-20px) translateY(10px); }
        }
        .weather-animation { animation: float 6s ease-in-out infinite; }
        """,
        'thunder': """
        @keyframes lightning {
            0%, 90%, 100% { opacity: 1; }
            5%, 10% { opacity: 0.2; }
        }
        .weather-animation { animation: lightning 2s infinite; }
        """
    }
    
    for condition, animation in animations.items():
        if condition in weather_condition.lower():
            return animation
    return ""

def get_city_image_url(city_name):
    """Get city image from Unsplash API"""
    try:
        # Using Unsplash Source API for city images
        # This is a free service that doesn't require API key
        city_formatted = city_name.replace(' ', '%20')
        return f"https://source.unsplash.com/800x600/?{city_formatted},city,skyline"
    except:
        return None

# Main app
st.markdown('<h1 class="main-title">🌤️ Weather</h1>', unsafe_allow_html=True)

# Search container
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    city_input = st.text_input("Search for a city", placeholder="Search for a city...", label_visibility="collapsed")

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
                st.success(f"✅ Weather data loaded for {city_name}")
            else:
                st.error("❌ Failed to fetch weather data")
        else:
            st.error("❌ City not found. Try again with a different spelling.")

# Main content area
if 'current_weather' in st.session_state and 'weather_forecast' in st.session_state:
    current_weather = st.session_state['current_weather']
    weather_forecast = st.session_state['weather_forecast']
    city_name = st.session_state['city_name']
    
    # Get weather-based styling
    weather_condition = current_weather['weather'][0]['description']
    icon_code = current_weather['weather'][0]['icon']
    is_day = 'd' in icon_code
    temp = current_weather['main']['temp']
    
    # Dynamic background based on weather
    dynamic_bg = get_weather_background(weather_condition, is_day)
    weather_animation = get_weather_animation(weather_condition)
    
    # Temperature color coding
    if temp >= 30:
        temp_class = "temp-hot"
    elif temp >= 20:
        temp_class = "temp-warm"
    elif temp >= 10:
        temp_class = "temp-cool"
    elif temp >= 0:
        temp_class = "temp-cold"
    else:
        temp_class = "temp-freezing"
    
    # Add dynamic styles
    st.markdown(f"""
    <style>
        .stApp {{
            background: {dynamic_bg} !important;
        }}
        {weather_animation}
    </style>
    """, unsafe_allow_html=True)
    
    # City image
    city_image_url = get_city_image_url(city_name)
    
    # Current weather - Main card with city image
    st.markdown('<div class="main-container weather-animation">', unsafe_allow_html=True)
    
    # City image header
    if city_image_url:
        st.markdown(f"""
        <div class="city-image-container">
            <img src="{city_image_url}" class="city-image" alt="{city_name}">
            <div class="city-overlay">
                <div>
                    <div class="city-name">📍 {city_name}</div>
                    <div style="font-size: 0.9rem; opacity: 0.8;">Live Weather Data</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Weather particles background
    st.markdown(f"""
    <div class="weather-particles">
        <div class="floating-icon" style="left: 10%; animation-delay: 0s;">{get_weather_emoji(icon_code)}</div>
        <div class="floating-icon" style="left: 80%; animation-delay: 2s;">{get_weather_emoji(icon_code)}</div>
        <div class="floating-icon" style="left: 60%; animation-delay: 4s;">{get_weather_emoji(icon_code)}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Temperature and weather info
    col1, col2 = st.columns([2, 1])
    with col1:
        if not city_image_url:
            st.markdown(f'<div class="city-name">📍 {city_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="current-temp {temp_class}">{temp:.0f}°C</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="weather-desc">{weather_condition.title()} {get_weather_emoji(icon_code)}</div>', unsafe_allow_html=True)
        
        # Additional weather info
        sunrise = datetime.fromtimestamp(current_weather['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(current_weather['sys']['sunset']).strftime('%H:%M')
        st.markdown(f"""
        <div style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin-top: 1rem;">
            🌅 Sunrise: {sunrise} | 🌇 Sunset: {sunset}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="weather-card">
            <div class="weather-icon-large" style="font-size: 3rem; margin-bottom: 0.5rem;">{get_weather_emoji(icon_code)}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">Feels like {current_weather['main']['feels_like']:.0f}°C</div>
            <div style="font-size: 0.8rem; opacity: 0.6; margin-top: 0.5rem;">UV Index: {current_weather.get('uvi', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced metrics with weather-specific data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        humidity_icon = "💧" if current_weather['main']['humidity'] > 70 else "🌵" if current_weather['main']['humidity'] < 30 else "💧"
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{humidity_icon}</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{current_weather['main']['humidity']}%</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Humidity</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        wind_speed = current_weather['wind']['speed']
        wind_icon = "🌪️" if wind_speed > 10 else "💨" if wind_speed > 5 else "🍃"
        wind_direction = current_weather['wind'].get('deg', 0)
        directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        wind_dir = directions[int((wind_direction + 22.5) // 45) % 8]
        
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{wind_icon}</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{wind_speed:.1f} m/s</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Wind {wind_dir}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        pressure = current_weather['main']['pressure']
        pressure_icon = "📈" if pressure > 1020 else "📉" if pressure < 1000 else "🌡️"
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{pressure_icon}</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{pressure}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Pressure hPa</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        visibility = current_weather.get('visibility', 0) / 1000 if current_weather.get('visibility') else 0
        vis_icon = "👁️‍🗨️" if visibility > 10 else "🌫️" if visibility < 5 else "👁️"
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{vis_icon}</div>
            <div style="font-size: 1.2rem; font-weight: 500;">{visibility:.1f}</div>
            <div style="font-size: 0.8rem; opacity: 0.7;">Visibility km</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced 5-day forecast with animations
    st.markdown('<div style="margin-top: 2rem; color: white;"><h3 style="color: white; font-weight: 300;">📅 5-Day Forecast</h3></div>', unsafe_allow_html=True)
    
    df = format_weather_data(weather_forecast)
    
    if df is not None and len(df) > 0:
        cols = st.columns(min(5, len(df)))
        for i, col in enumerate(cols):
            if i < len(df):
                row = df.iloc[i]
                with col:
                    day_name = row['Day'][:3]
                    max_temp = row['Max Temp']
                    min_temp = row['Min Temp']
                    
                    # Temperature color for forecast
                    if max_temp >= 30:
                        forecast_temp_class = "temp-hot"
                    elif max_temp >= 20:
                        forecast_temp_class = "temp-warm"
                    elif max_temp >= 10:
                        forecast_temp_class = "temp-cool"
                    else:
                        forecast_temp_class = "temp-cold"
                    
                    st.markdown(f"""
                    <div class="forecast-item">
                        <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem;">{day_name}</div>
                        <div style="font-size: 2rem; margin: 0.5rem 0;">{get_weather_emoji(row['Icon'])}</div>
                        <div style="font-size: 1rem; font-weight: 500;" class="{forecast_temp_class}">{max_temp:.0f}°</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">{min_temp:.0f}°</div>
                        <div style="font-size: 0.7rem; opacity: 0.6; margin-top: 0.3rem;">{row['Description']}</div>
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