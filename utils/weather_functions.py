import logging
import requests

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
        logging.info("Weather data collected successfully.")
        return weather_data
    except requests.exceptions.HTTPError as e:
        logging.error(f"HTTP Error: {e}")
        raise e
    except requests.exceptions.ConnectionError as e:
        logging.error(f"Connection Error: {e}")
        raise e
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        raise e
