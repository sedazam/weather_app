# 🌤️ Weather App

A beautiful, minimalist weather application built with Streamlit that provides real-time weather information and 5-day forecasts for any city worldwide.

![Weather App](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.47+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- **🌍 Global Weather Data**: Get weather information for any city worldwide
- **📍 Auto Location Detection**: Automatically detect your current location using IP geolocation
- **🔮 5-Day Forecast**: View detailed weather forecasts for the next 5 days
- **🎨 Beautiful UI**: Minimalist design with glassmorphism effects and gradient backgrounds
- **📱 Responsive Design**: Clean, centered layout that works on all screen sizes
- **🌡️ Detailed Information**: Current temperature, temperature range, and weather conditions
- **🎯 Weather Icons**: Visual weather representation with emoji icons

## 🚀 Live Demo

The app provides:

- Current weather conditions
- Temperature (current, min, max)
- Weather description
- 5-day forecast with daily highs and lows
- Beautiful gradient background with glassmorphic cards

## 🛠️ Installation

### Prerequisites

- Python 3.9 or higher
- OpenWeatherMap API key (free)

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/sedazam/weather_app.git
   cd weather_app
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Get OpenWeatherMap API Key**

   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate your API key

4. **Configure Environment Variables**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your API key:

   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```

5. **Run the Application**

   ```bash
   streamlit run weather_app.py
   ```

6. **Open in Browser**
   - Navigate to `http://localhost:8501`
   - Start searching for cities or use auto-location!

## 🎮 Usage

### Search for Weather

1. Enter any city name in the search bar
2. Click the "🔍 Search" button
3. View current weather and 5-day forecast

### Auto Location Detection

1. Click the "📍" location button
2. Allow location access if prompted
3. View weather for your current location

### Features Overview

- **Search Bar**: Enter city names (e.g., "New York", "London", "Chandigarh")
- **Current Weather**: Large temperature display with weather icon
- **Temperature Range**: Daily high and low temperatures
- **5-Day Forecast**: Week ahead with weather icons and temperature ranges

## 🏗️ Project Structure

```
weather_app/
├── app.py                  # Main application file (modular)
├── weather_app.py          # Original monolithic version
├── utils.py               # Weather API functions and data processing
├── templates.py           # HTML template engine
├── styles.css             # External CSS styles
├── templates/             # HTML template files
│   ├── weather_card.html  # Main weather card template
│   ├── forecast_day.html  # Forecast day template
│   └── welcome.html       # Welcome screen template
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (not in git)
├── .gitignore           # Git ignore rules
├── STRUCTURE.md         # Modular architecture documentation
└── README.md            # Project documentation
```

## 🚀 Running the App

### Option 1: Modular Version (Recommended)
```bash
streamlit run app.py
```

### Option 2: Original Version
```bash
streamlit run weather_app.py
```

## 🔧 Technical Details

### Technologies Used

- **Streamlit**: Web framework for Python apps
- **OpenWeatherMap API**: Weather data source
- **IP Geolocation API**: Automatic location detection
- **Python Requests**: HTTP requests handling
- **Python Datetime**: Date and time operations

### API Endpoints Used

- Current Weather: `api.openweathermap.org/data/2.5/weather`
- 5-Day Forecast: `api.openweathermap.org/data/2.5/forecast`
- IP Location: `ip-api.com/json/`

### Key Features Implementation

- **Glassmorphism UI**: CSS backdrop-filter for modern glass effect
- **Responsive Design**: Flexbox layout with mobile-first approach
- **Error Handling**: Graceful handling of API errors and invalid cities
- **Caching**: Efficient API calls with Streamlit's built-in caching

## 🎨 Design

The app features a modern, minimalist design inspired by popular weather apps:

- **Background**: Beautiful gradient from blue to purple with pink accents
- **Cards**: Glassmorphic design with blur effects and transparency
- **Typography**: Clean, readable fonts with proper hierarchy
- **Icons**: Weather emoji icons for intuitive understanding
- **Layout**: Centered, responsive design that works on all devices

## 📋 Requirements

```
streamlit>=1.47.1
requests>=2.31.0
python-dotenv>=1.0.0
```

## 🌐 Environment Variables

| Variable              | Description                 | Required |
| --------------------- | --------------------------- | -------- |
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | Yes      |

## 🔒 Security

- API keys are stored in environment variables
- `.env` file is excluded from version control
- No sensitive data exposed in the frontend

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [IP-API](https://ip-api.com/) for geolocation services

## 🐛 Issues & Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/sedazam/weather_app/issues) page
2. Create a new issue if your problem isn't listed
3. Provide detailed information about the problem

## 🔄 Version History

- **v1.0.0** - Initial release with basic weather functionality
- **v1.1.0** - Added 5-day forecast feature
- **v1.2.0** - Implemented auto-location detection
- **v1.3.0** - Enhanced UI with glassmorphism design
- **v1.4.0** - Improved layout and responsiveness

---

⭐ **Star this repository if you find it helpful!**

Built with ❤️ by [Seddiq Azam](https://github.com/sedazam)
