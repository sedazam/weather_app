"""
Template Engine for Weather App
Handles loading and rendering HTML templates
"""

import os

def load_template(template_name):
    """Load HTML template from templates directory"""
    template_path = os.path.join(os.path.dirname(__file__), 'templates', template_name)
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"<!-- Template {template_name} not found -->"

def load_css():
    """Load CSS styles from styles.css file"""
    css_path = os.path.join(os.path.dirname(__file__), 'styles.css')
    try:
        with open(css_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "/* CSS file not found */"

def render_weather_card(city_name, weather_icon, temperature, min_temp, max_temp, description, forecast_days_html):
    """Render the main weather card with data"""
    template = load_template('weather_card.html')
    return template.format(
        city_name=city_name,
        weather_icon=weather_icon,
        temperature=int(temperature),
        min_temp=int(min_temp),
        max_temp=int(max_temp),
        description=description,
        forecast_days=forecast_days_html
    )

def render_forecast_day(day_name, icon, max_temp, min_temp):
    """Render a single forecast day"""
    template = load_template('forecast_day.html')
    return template.format(
        day_name=day_name,
        icon=icon,
        max_temp=int(max_temp),
        min_temp=int(min_temp)
    )

def render_forecast_days(forecast_list):
    """Render all forecast days"""
    forecast_html = ""
    for day_data in forecast_list:
        forecast_html += render_forecast_day(
            day_data['day'],
            day_data['icon'],
            day_data['max_temp'],
            day_data['min_temp']
        )
    return forecast_html

def render_welcome_screen():
    """Render the welcome/landing screen"""
    return load_template('welcome.html')
