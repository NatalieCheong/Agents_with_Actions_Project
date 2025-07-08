import requests
import os
from dotenv import load_dotenv
from nexus.nexus_base.action_manager import agent_action

load_dotenv()

@agent_action
def get_weather(city: str) -> str:
    """Get current weather information for a specified city."""
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    if not api_key:
        return "❌ Error: OPEN_WEATHER_MAP_API_KEY not found in environment variables"
    
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    try:
        params = {
            'q': city,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        city_name = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        description = data['weather'][0]['description'].title()
        
        weather_info = f"""🌤️ Weather in {city_name}, {country}:
Temperature: {temperature}°C (feels like {feels_like}°C)
Conditions: {description}
Humidity: {humidity}%"""
        
        return weather_info
        
    except Exception as e:
        return f"❌ Error fetching weather data: {str(e)}"

