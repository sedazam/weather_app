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
    
    .location-info {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }
</style>

<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    
    // Store coordinates in session storage
    sessionStorage.setItem('user_lat', lat);
    sessionStorage.setItem('user_lon', lon);
    
    // Trigger Streamlit rerun with coordinates
    window.parent.postMessage({
        type: 'streamlit:setComponentValue',
        value: {lat: lat, lon: lon}
    }, '*');
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}
</script>
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
        # Using a free IP geolocation service
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

# Show location detection info
if 'location_method' not in st.session_state:
    st.session_state['location_method'] = None

st.markdown("""
<div class="location-info">
    💡 <strong>Location Detection:</strong> Click "📍 My Location" to automatically get weather for your current location using IP-based detection.
</div>
""", unsafe_allow_html=True)

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
if use_auto_location:
    current_lat = st.session_state.get('auto_lat')
    current_lon = st.session_state.get('auto_lon')
    current_city = st.session_state.get('auto_city')
else:
    current_lat = None
    current_lon = None
    current_city = city

if (city and search_btn) or use_auto_location:
    if not API_KEY:
        st.error("⚠️ API key not found! Please add OPENWEATHER_API_KEY to your .env file")
    else:
        try:
            # Get weather data based on input type
            if use_auto_location:
                current_data = get_weather_by_coords(current_lat, current_lon)
                if current_data:
                    lat = current_lat
                    lon = current_lon
                    # Reset auto location after use
                    st.session_state['auto_location'] = False
                else:
                    st.error("❌ Could not get weather data for your location")
                    st.stop()
            else:
                # Get current weather by city name
                current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
                current_response = requests.get(current_url)
                current_response.raise_for_status()
                current_data = current_response.json()
                
                # Get coordinates for forecast
                lat = current_data['coord']['lat']
                lon = current_data['coord']['lon']
            
            forecast_data = get_forecast_data(lat, lon)
            
            # Main weather display
            st.markdown('<div class="main-weather-container">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f'<div class="city-title">{current_data["name"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="weather-condition">{current_data["weather"][0]["description"].title()}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="temp-range">H:{current_data["main"]["temp_max"]:.0f}° L:{current_data["main"]["temp_min"]:.0f}°</div>', unsafe_allow_html=True)
                st.markdown(f'<div style="color: rgba(255,255,255,0.7); margin-bottom: 1rem;">{datetime.now().strftime("%A")} Today</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'<div class="current-temp">{current_data["main"]["temp"]:.0f}°</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Hourly forecast (using forecast data)
            if forecast_data:
                st.markdown('<div class="hourly-container">', unsafe_allow_html=True)
                st.markdown('<h4 style="color: white; margin-bottom: 1rem;">Hourly Forecast</h4>', unsafe_allow_html=True)
                
                hourly_cols = st.columns(8)
                for i, col in enumerate(hourly_cols):
                    if i < len(forecast_data['list']):
                        item = forecast_data['list'][i]
                        time = datetime.fromtimestamp(item['dt'])
                        
                        with col:
                            if i == 0:
                                time_str = "Now"
                            else:
                                time_str = time.strftime("%I%p").lstrip('0').lower()
                            
                            st.markdown(f"""
                            <div class="hourly-item">
                                <div style="font-size: 0.8rem; margin-bottom: 0.3rem;">{time_str}</div>
                                <div style="font-size: 1.5rem; margin: 0.3rem 0;">{get_weather_icon(item['weather'][0]['main'])}</div>
                                <div style="font-size: 0.9rem;">{item['main']['temp']:.0f}°</div>
                            </div>
                            """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # 5-day forecast and weather details
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if forecast_data:
                    st.markdown('<div class="forecast-container">', unsafe_allow_html=True)
                    st.markdown('<h4 style="color: white; margin-bottom: 1rem;">5-Day Forecast</h4>', unsafe_allow_html=True)
                    
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
                    
                    for i, (date, data) in enumerate(list(daily_forecasts.items())[:5]):
                        day_name = "Today" if i == 0 else date.strftime("%A")
                        min_temp = min(data['temps'])
                        max_temp = max(data['temps'])
                        
                        st.markdown(f"""
                        <div class="forecast-day">
                            <div>{day_name}</div>
                            <div style="display: flex; align-items: center; gap: 1rem;">
                                <span>{data['icon']}</span>
                                <span>{max_temp:.0f}° {min_temp:.0f}°</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="weather-details">', unsafe_allow_html=True)
                st.markdown('<h4 style="color: white; margin-bottom: 1rem;">Weather Details</h4>', unsafe_allow_html=True)
                
                # Sunrise and sunset
                sunrise = datetime.fromtimestamp(current_data['sys']['sunrise']).strftime("%-I:%M %p")
                sunset = datetime.fromtimestamp(current_data['sys']['sunset']).strftime("%-I:%M %p")
                
                details = [
                    ("Sunrise", sunrise),
                    ("Sunset", sunset),
                    ("Chance of Rain", "0%"),  # Not available in free API
                    ("Humidity", f"{current_data['main']['humidity']}%"),
                    ("Wind", f"{current_data['wind'].get('deg', 'N/A')} {current_data['wind']['speed']} mph"),
                    ("Feels Like", f"{current_data['main']['feels_like']:.0f}°"),
                    ("Pressure", f"{current_data['main']['pressure']} hPa"),
                    ("Visibility", f"{current_data.get('visibility', 10000)/1000:.1f} km")
                ]
                
                for label, value in details:
                    st.markdown(f"""
                    <div class="detail-item">
                        <span>{label}</span>
                        <span>{value}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            
        except requests.exceptions.RequestException:
            st.error("❌ City not found or API error. Please check the city name and try again.")
        except KeyError as e:
            st.error(f"❌ Unexpected response format from weather API: {e}")

else:
    # Welcome screen
    st.markdown("""
    <div class="main-weather-container" style="text-align: center;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🌤️</div>
        <h2 style="color: white; font-weight: 300; margin-bottom: 1rem;">Weather</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem;">Search for any city to get detailed weather information</p>
    </div>
    """, unsafe_allow_html=True)