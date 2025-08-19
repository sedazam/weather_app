import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

# Load API key from environment
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Set page configuration
st.set_page_config(
    page_title="Weather App - Live Weather Forecast",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for minimalist weather app design
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #4A90E2 0%, #764ba2 50%, #f093fb 70%, #f5576c 100%);
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
        padding: 0;
        margin: 0;
    }
    
    .main-weather-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(30px);
        border-radius: 30px;
        padding: 3rem 2rem;
        margin: 2rem auto;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
        text-align: center;
        max-width: 500px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    }
    
    .city-name {
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 2rem;
        color: white;
        opacity: 0.9;
    }
    
    .weather-icon-main {
        font-size: 6rem;
        margin: 1rem 0;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }
    
    .main-temperature {
        font-size: 4rem;
        font-weight: 200;
        margin: 1rem 0;
        color: white;
    }
    
    .temp-range {
        font-size: 1.2rem;
        margin: 1rem 0;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .weather-description {
        font-size: 1.3rem;
        margin: 1.5rem 0;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
    }
    
    .forecast-row {
        display: flex;
        justify-content: space-between;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .forecast-day {
        text-align: center;
        color: white;
        flex: 1;
        padding: 0 0.5rem;
    }
    
    .day-name {
        font-size: 1rem;
        margin-bottom: 1rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 400;
    }
    
    .forecast-icon {
        font-size: 2.5rem;
        margin: 0.5rem 0;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
    }
    
    .forecast-temps {
        font-size: 1rem;
        margin-top: 0.5rem;
        color: rgba(255, 255, 255, 0.9);
    }
    
    .search-container {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 25px;
        padding: 1rem;
        margin: 2rem auto;
        backdrop-filter: blur(20px);
        max-width: 500px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9);
        border: none;
        border-radius: 20px;
        padding: 0.75rem 1rem;
        color: #333;
        font-size: 1rem;
        box-shadow: none;
    }
    
    .stButton > button {
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 20px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Center everything */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
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

def get_location_by_ip():
    """Get approximate location using IP geolocation"""
    try:
        response = requests.get('http://ip-api.com/json/')
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return data['lat'], data['lon'], data['city']
    except:
        pass
    return None, None, None

def get_weather_by_coords(lat, lon):
    """Get weather data using coordinates"""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Search container
st.markdown('<div class="search-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([3, 1, 1])
with col1:
    city = st.text_input("Search for a city", placeholder="Enter city name", label_visibility="collapsed")
with col2:
    search_btn = st.button("🔍 Search")
with col3:
    location_btn = st.button("📍 My Location")
st.markdown('</div>', unsafe_allow_html=True)

# Auto-detect location if button clicked
if location_btn:
    with st.spinner("🌍 Detecting your location..."):
        lat, lon, detected_city = get_location_by_ip()
        if lat and lon:
            st.session_state['auto_location'] = True
            st.session_state['auto_lat'] = lat
            st.session_state['auto_lon'] = lon
            st.session_state['auto_city'] = detected_city
            st.success(f"📍 Location detected: {detected_city}")
        else:
            st.error("❌ Could not detect your location. Please enter a city manually.")

# Check if we should use auto-detected location
use_auto_location = st.session_state.get('auto_location', False)

if (city and search_btn) or use_auto_location:
    if not API_KEY:
        st.error("⚠️ API key not found! Please add OPENWEATHER_API_KEY to your .env file")
    else:
        try:
            # Get weather data
            if use_auto_location:
                current_lat = st.session_state.get('auto_lat')
                current_lon = st.session_state.get('auto_lon')
                current_data = get_weather_by_coords(current_lat, current_lon)
                if current_data:
                    lat = current_lat
                    lon = current_lon
                    st.session_state['auto_location'] = False
                else:
                    st.error("❌ Could not get weather data for your location")
                    st.stop()
            else:
                current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                current_response = requests.get(current_url)
                current_response.raise_for_status()
                current_data = current_response.json()
                lat = current_data['coord']['lat']
                lon = current_data['coord']['lon']
            
            forecast_data = get_forecast_data(lat, lon)
            
            # Main weather card matching Chandigarh design
            st.markdown(f"""
            <div class="main-weather-card">
                <div class="city-name">{current_data['name']}</div>
                <div class="weather-icon-main">{get_weather_icon(current_data['weather'][0]['main'])}</div>
                <div class="main-temperature">{current_data['main']['temp']:.0f}°</div>
                <div class="temp-range">{current_data['main']['temp_min']:.0f}° - {current_data['main']['temp_max']:.0f}°</div>
                <div class="weather-description">{current_data['weather'][0]['description'].title()}</div>
                
                <div class="forecast-row">
            """, unsafe_allow_html=True)
            
            # 5-day forecast
            if forecast_data:
                # Group forecast by day
                daily_forecasts = {}
                for item in forecast_data['list']:
                    date = datetime.fromtimestamp(item['dt']).date()
                    if date not in daily_forecasts:
                        daily_forecasts[date] = {
                            'temps': [],
                            'condition': item['weather'][0]['main'],
                            'icon': get_weather_icon(item['weather'][0]['main'])
                        }
                    daily_forecasts[date]['temps'].append(item['main']['temp'])
                
                days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
                forecast_html = ""
                
                for i, (date, data) in enumerate(list(daily_forecasts.items())[:5]):
                    day_name = days[i] if i < len(days) else date.strftime("%a")
                    min_temp = min(data['temps'])
                    max_temp = max(data['temps'])
                    
                    forecast_html += f"""
                    <div class="forecast-day">
                        <div class="day-name">{day_name}</div>
                        <div class="forecast-icon">{data['icon']}</div>
                        <div class="forecast-temps">{max_temp:.0f}/{min_temp:.0f}</div>
                    </div>
                    """
                
                st.markdown(forecast_html, unsafe_allow_html=True)
            
            st.markdown("""
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        except requests.exceptions.RequestException:
            st.error("❌ City not found or API error. Please check the city name and try again.")
        except KeyError as e:
            st.error(f"❌ Unexpected response format from weather API: {e}")

else:
    # Welcome screen
    st.markdown("""
    <div class="main-weather-card">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌤️</div>
        <div class="city-name">Weather App</div>
        <div class="weather-description">Search for any city to get beautiful weather information</div>
        <div style="color: rgba(255,255,255,0.6); font-size: 1rem; margin-top: 1rem;">Click "📍 My Location" for automatic detection</div>
    </div>
    """, unsafe_allow_html=True)
