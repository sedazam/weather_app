"""
Weather App - Main Application
A beautiful, minimalist weather application built with Streamlit
"""

import streamlit as st
import requests
from utils import (
    get_weather_icon, get_forecast_data, get_location_by_ip,
    get_weather_by_coords, get_weather_by_city, process_forecast_data
)
from templates import (
    load_css, render_weather_card, render_forecast_days, render_welcome_screen
)

# Set page configuration
st.set_page_config(
    page_title="Weather App - Live Weather Forecast",
    page_icon="🌤️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Load and apply CSS styles
css_styles = load_css()
st.markdown(f"<style>{css_styles}</style>", unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Search inputs
    city = st.text_input("Search for a city", placeholder="Enter city name", label_visibility="collapsed")

    # Buttons below search bar
    col1, col2 = st.columns([1, 1])
    with col1:
        search_btn = st.button("🔍 Search")
    with col2:
        location_btn = st.button("📍")

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
        display_weather_data(city, use_auto_location)
    else:
        # Display welcome screen
        welcome_html = render_welcome_screen()
        st.markdown(welcome_html, unsafe_allow_html=True)

def display_weather_data(city, use_auto_location):
    """Display weather data for the given city or auto-detected location"""
    
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
                return
        else:
            current_data = get_weather_by_city(city)
            if not current_data:
                st.error("❌ City not found or API error. Please check the city name and try again.")
                return
            lat = current_data['coord']['lat']
            lon = current_data['coord']['lon']
        
        # Get forecast data
        forecast_data = get_forecast_data(lat, lon)
        forecast_list = process_forecast_data(forecast_data)
        
        # Render forecast days HTML
        forecast_days_html = render_forecast_days(forecast_list)
        
        # Render complete weather card
        weather_html = render_weather_card(
            city_name=current_data['name'],
            weather_icon=get_weather_icon(current_data['weather'][0]['main']),
            temperature=current_data['main']['temp'],
            min_temp=current_data['main']['temp_min'],
            max_temp=current_data['main']['temp_max'],
            description=current_data['weather'][0]['description'].title(),
            forecast_days_html=forecast_days_html
        )
        
        # Display the weather card
        st.markdown(weather_html, unsafe_allow_html=True)
        
    except requests.exceptions.RequestException:
        st.error("❌ Network error. Please check your internet connection and try again.")
    except KeyError as e:
        st.error(f"❌ Unexpected response format from weather API: {e}")
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
