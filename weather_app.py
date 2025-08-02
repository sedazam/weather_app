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
st.title("🌤️ 5-Day Weather Forecast")
st.markdown("Get detailed weather forecasts for any city around the world")

# Sidebar for input
with st.sidebar:
    st.header("🏙️ City Selection")
    city_input = st.text_input("Enter city name:", placeholder="e.g., London, New York, Tokyo")
    
    if st.button("Get Forecast", type="primary"):
        if city_input:
            with st.spinner("Fetching weather data..."):
                lat, lon, city_name = get_coordinates(city_input)
                
                if lat and lon:
                    current_weather = get_current_weather(lat, lon)
                    weather_forecast = get_weather_forecast(lat, lon)
                    
                    if current_weather and weather_forecast:
                        st.session_state['current_weather'] = current_weather
                        st.session_state['weather_forecast'] = weather_forecast
                        st.session_state['city_name'] = city_name
                        st.success(f"Weather data loaded for {city_name}")
                    else:
                        st.error("Failed to fetch weather data")
                else:
                    st.error("City not found. Please check the spelling and try again.")
    
    st.markdown("---")
    st.markdown("**Note:** You need an OpenWeatherMap API key to use this app. Get one free at [openweathermap.org](https://openweathermap.org/api) and add it to your .env file")

# Main content area
if 'current_weather' in st.session_state and 'weather_forecast' in st.session_state:
    current_weather = st.session_state['current_weather']
    weather_forecast = st.session_state['weather_forecast']
    city_name = st.session_state['city_name']
    
    # Current weather
    st.subheader(f"Current Weather in {city_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Temperature",
            f"{current_weather['main']['temp']:.1f}°C",
            f"Feels like {current_weather['main']['feels_like']:.1f}°C"
        )
    
    with col2:
        st.metric("Humidity", f"{current_weather['main']['humidity']}%")
    
    with col3:
        st.metric("Wind Speed", f"{current_weather['wind']['speed']} m/s")
    
    with col4:
        st.metric("Pressure", f"{current_weather['main']['pressure']} hPa")
    
    st.markdown(f"**Conditions:** {current_weather['weather'][0]['description'].title()} {get_weather_emoji(current_weather['weather'][0]['icon'])}")
    
    # 5-day forecast
    st.subheader("📅 5-Day Forecast")
    
    df = format_weather_data(weather_forecast)
    
    if df is not None:
        # Display forecast cards
        for i in range(0, len(df), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with col:
                        emoji = get_weather_emoji(row['Icon'])
                        st.markdown(f"""
                        <div style="
                            border: 1px solid #ddd;
                            border-radius: 10px;
                            padding: 15px;
                            margin: 5px;
                            text-align: center;
                            background-color: #f9f9f9;
                        ">
                            <h4>{row['Day']}</h4>
                            <p style="font-size: 14px; color: #666;">{row['Date']}</p>
                            <div style="font-size: 30px;">{emoji}</div>
                            <p><strong>{row['Temperature (°C)']}°C</strong></p>
                            <p>{row['Description']}</p>
                            <p>💧 {row['Humidity (%)']}% | 💨 {row['Wind Speed (m/s)']} m/s</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Temperature chart
        st.subheader("📊 Temperature Trend")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Max Temp'],
            mode='lines+markers',
            name='Max Temperature',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Min Temp'],
            mode='lines+markers',
            name='Min Temperature',
            line=dict(color='blue', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="5-Day Temperature Forecast",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            hovermode='x unified',
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Data table
        with st.expander("📋 Detailed Forecast Data"):
            display_df = df[['Date', 'Day', 'Temperature (°C)', 'Description', 'Humidity (%)', 'Wind Speed (m/s)']]
            st.dataframe(display_df, use_container_width=True)

else:
    # Welcome message
    st.info("👆 Enter a city name in the sidebar to get started!")
    
    st.markdown("""
    ### Features:
    - 🌍 **Global Coverage**: Get weather forecasts for cities worldwide
    - 📊 **Visual Charts**: Temperature trends with interactive graphs
    - 📱 **Responsive Design**: Works on desktop and mobile devices
    - 🎯 **Accurate Data**: Powered by OpenWeatherMap API
    
    ### How to use:
    1. Enter a city name in the sidebar
    2. Click "Get Forecast" 
    3. View current conditions and 5-day forecast
    4. Explore temperature trends in the chart
    
    ### Setup Instructions:
    1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
    2. Create a `.env` file in the project folder and add: `OPENWEATHER_API_KEY=your_api_key_here`
    3. Install required packages: `pip install -r requirements.txt`
    4. Run the app: `streamlit run weather_app.py`
    """)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit | Weather data provided by OpenWeatherMap",
    help="This app uses the OpenWeatherMap API to fetch real-time weather data"
)