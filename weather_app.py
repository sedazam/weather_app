import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load API key from environment
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Set page configuration
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered"
)

# App title
st.title("🌤️ Weather App")
st.write("Get current weather information for any city")

# Input for city name
city = st.text_input("Enter city name:")

if city:
    if not API_KEY:
        st.error("⚠️ API key not found! Please add OPENWEATHER_API_KEY to your .env file")
    else:
        # Make API request
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            # Display weather information
            st.success(f"✅ Weather data for {data['name']}, {data['sys']['country']}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Temperature", f"{data['main']['temp']:.1f}°C", f"Feels like {data['main']['feels_like']:.1f}°C")
                st.metric("Humidity", f"{data['main']['humidity']}%")
            
            with col2:
                st.metric("Weather", data['weather'][0]['description'].title())
                st.metric("Wind Speed", f"{data['wind']['speed']} m/s")
            
            # Additional info
            st.subheader("Additional Information")
            st.write(f"**Pressure:** {data['main']['pressure']} hPa")
            st.write(f"**Visibility:** {data.get('visibility', 'N/A')} meters")
            st.write(f"**Cloudiness:** {data['clouds']['all']}%")
            
        except requests.exceptions.RequestException:
            st.error("❌ City not found or API error. Please check the city name and try again.")
        except KeyError:
            st.error("❌ Unexpected response format from weather API.")

else:
    st.info("👆 Please enter a city name above to get weather information")

# Footer
st.markdown("---")
st.caption("Powered by OpenWeatherMap API")