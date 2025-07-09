import requests
import logging
from typing import Optional
from src.utils.config_manager import ConfigManager

class WeatherService:
    def __init__(self, config: ConfigManager):
        self.config = config

    def get_weather(self, city: str) -> str:
        """Get weather information for a city"""
        api_key = self.config.get('weather_api_key')
        if not api_key:
            return "Weather API key not configured"
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                return f"The temperature in {city} is {temp}°C with {desc}"
            return "Could not fetch weather information"
        except Exception as e:
            logging.error(f"Weather API error: {str(e)}")
            return "Error fetching weather information" 