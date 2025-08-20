"""
Weather App Utilities
Helper functions for weather data processing and UI components
"""

import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

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

def get_weather_by_city(city):
    """Get weather data by city name"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except:
        return None

def process_forecast_data(forecast_data):
    """Process forecast data into daily summaries"""
    if not forecast_data:
        return []
    
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
    
    # Convert to list format with day names
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    forecast_list = []
    
    for i, (date, data) in enumerate(list(daily_forecasts.items())[:5]):
        day_name = days[i] if i < len(days) else date.strftime("%a")
        min_temp = min(data['temps'])
        max_temp = max(data['temps'])
        
        forecast_list.append({
            'day': day_name,
            'icon': data['icon'],
            'max_temp': int(max_temp),
            'min_temp': int(min_temp)
        })
    
    return forecast_list
