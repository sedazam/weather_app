#!/usr/bin/env python3
"""
Simple test script to verify OpenWeatherMap API key works
Run this before using the main weather app
"""

import requests

def test_api_key():
    # Replace with your actual API key
    API_KEY = "your_openweather_api_key_here"
    
    if API_KEY == "your_openweather_api_key_here":
        print("❌ Please replace 'your_openweather_api_key_here' with your actual API key")
        print("   Get one free at: https://openweathermap.org/api")
        return False
    
    # Test geocoding API
    print("🧪 Testing API key with geocoding...")
    geocoding_url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        'q': 'London',
        'limit': 1,
        'appid': API_KEY
    }
    
    try:
        response = requests.get(geocoding_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data:
            print(f"✅ Geocoding API works! Found: {data[0]['name']}, {data[0]['country']}")
            
            # Test weather API
            print("🧪 Testing weather API...")
            weather_url = "http://api.openweathermap.org/data/2.5/weather"
            weather_params = {
                'lat': data[0]['lat'],
                'lon': data[0]['lon'],
                'appid': API_KEY,
                'units': 'metric'
            }
            
            weather_response = requests.get(weather_url, params=weather_params)
            weather_response.raise_for_status()
            weather_data = weather_response.json()
            
            print(f"✅ Weather API works! Current temp in {weather_data['name']}: {weather_data['main']['temp']}°C")
            print("🎉 Your API key is working correctly!")
            return True
            
        else:
            print("❌ API key seems invalid - no data returned")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ API request failed: {e}")
        return False

if __name__ == "__main__":
    print("OpenWeatherMap API Key Tester")
    print("=" * 30)
    test_api_key()
