import requests
try:
    from log_setup import *
except ImportError:
    from .log_setup import *

def get_weather(latitude, longitude, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat":   latitude,
        "lon":   longitude,
        "appid": api_key
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        weather_data = response.json()
        logger_tw.info("Weather data collected successfully.")
        return weather_data
    except requests.exceptions.HTTPError as e:
        logger_tw.error(f"HTTP Error: {e}")
        raise e
    except requests.exceptions.ConnectionError as e:
        logger_tw.error(f"Connection Error: {e}")
        raise e
    except requests.exceptions.RequestException as e:
        logger_tw.error(f"Error: {e}")
        raise e
