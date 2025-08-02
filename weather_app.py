import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="7-Day Weather Forecast",
    page_icon="🌤️",
    layout="wide"
)

# API configuration
# Using OpenWeatherMap API (free tier allows 1000 calls/day)
API_KEY = "http://api.openweathermap.org/data/2.5/forecast?id=524901&appid={API key}"  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5"

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
    """Get 7-day weather forecast using coordinates"""
    forecast_url = f"{BASE_URL}/onecall"
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric',
        'exclude': 'minutely,alerts'
    }
    
    try:
        response = requests.get(forecast_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def format_weather_data(weather_data):
    """Format weather data for display"""
    if not weather_data:
        return None
    
    daily_data = []
    
    for day in weather_data['daily'][:7]:  # Get 7 days
        date = datetime.fromtimestamp(day['dt'])
        daily_data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Day': date.strftime('%A'),
            'Temperature (°C)': f"{day['temp']['min']:.1f} - {day['temp']['max']:.1f}",
            'Min Temp': day['temp']['min'],
            'Max Temp': day['temp']['max'],
            'Description': day['weather'][0]['description'].title(),
            'Humidity (%)': day['humidity'],
            'Wind Speed (m/s)': day['wind_speed'],
            'Icon': day['weather'][0]['icon']
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
st.title("🌤️ 7-Day Weather Forecast")
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
                    weather_data = get_weather_forecast(lat, lon)
                    if weather_data:
                        st.session_state['weather_data'] = weather_data
                        st.session_state['city_name'] = city_name
                        st.success(f"Weather data loaded for {city_name}")
                    else:
                        st.error("Failed to fetch weather data")
                else:
                    st.error("City not found. Please check the spelling and try again.")
    
    st.markdown("---")
    st.markdown("**Note:** You need an OpenWeatherMap API key to use this app. Get one free at [openweathermap.org](https://openweathermap.org/api)")

# Main content area
if 'weather_data' in st.session_state:
    weather_data = st.session_state['weather_data']
    city_name = st.session_state['city_name']
    
    # Current weather
    current = weather_data['current']
    st.subheader(f"Current Weather in {city_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Temperature",
            f"{current['temp']:.1f}°C",
            f"Feels like {current['feels_like']:.1f}°C"
        )
    
    with col2:
        st.metric("Humidity", f"{current['humidity']}%")
    
    with col3:
        st.metric("Wind Speed", f"{current['wind_speed']} m/s")
    
    with col4:
        st.metric("Pressure", f"{current['pressure']} hPa")
    
    st.markdown(f"**Conditions:** {current['weather'][0]['description'].title()} {get_weather_emoji(current['weather'][0]['icon'])}")
    
    # 7-day forecast
    st.subheader("📅 7-Day Forecast")
    
    df = format_weather_data(weather_data)
    
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
            title="7-Day Temperature Forecast",
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
    3. View current conditions and 7-day forecast
    4. Explore temperature trends in the chart
    
    ### Setup Instructions:
    1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
    2. Replace `your_openweather_api_key_here` in the code with your actual API key
    3. Install required packages: `pip install streamlit requests pandas plotly`
    4. Run the app: `streamlit run weather_app.py`
    """)

# Footer
st.markdown("---")
st.markdown(
    "Built with ❤️ using Streamlit | Weather data provided by OpenWeatherMap",
    help="This app uses the OpenWeatherMap API to fetch real-time weather data"
)