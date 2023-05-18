import logging
import os
from dotenv import load_dotenv      # pip install python-dotenv
from utils import weather_functions
from utils import tapo_functions

# Logger configuration
logging.basicConfig(filename='./app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Loading environment variables from the .env file
load_dotenv("config.env")

# Configuration values
cloudiness_breakpoint = 33  # percentage

# Tapo's plugs and bulbs configuration
tapo_email = os.getenv("TAPO_EMAIL")
tapo_psw =   os.getenv("TAPO_PSW")
bedroom_plug_params = {
    "ip":    os.getenv("IP_BEDROOM_PLUG"),
    "email": tapo_email,
    "psw":   tapo_psw,
    "model": "P100"
}
bedroom_bulb_params = {
    "ip":    os.getenv("IP_BEDROOM_BULB"),
    "email": tapo_email,
    "psw":   tapo_psw,
    "model": "L530"
}
devices = {
    "bedroom_plug": bedroom_plug_params,
    "bedroom_bulb": bedroom_bulb_params
}

# OpenWeather parameters
latitude =  os.getenv("LATITUDE")
longitude = os.getenv("LONGITUDE")
api_key =   os.getenv("OPEN_WEATHER_API_KEY")

def start():
    # Get weather information
    weather_info = weather_functions.get_weather(latitude, longitude, api_key)

    if weather_info:
        # If the weather it's cloudy turn on the light
        cloudiness = weather_info["clouds"]["all"]
        if cloudiness > cloudiness_breakpoint:
            logging.info(f"Cloudy ({cloudiness}%)")
            for device_name, device_params in devices.items():
                tapo_functions.if_off_turn_on(device_params)
        else:
            logging.info(f"Not cloudy ({cloudiness}%)")
            for device_name, device_params in devices.items():
                tapo_functions.if_on_turn_off(device_params)
    else:
        logging.error("Unable to retrieve weather data.")

if __name__ == "__main__":
    start()
    
logging.info("------------------------------------------")

