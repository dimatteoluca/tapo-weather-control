import logging
import os
import threading
from dotenv import load_dotenv  # pip install python-dotenv
try:
    from utils import weather_functions
    from utils import tapo_functions
except ImportError:             # handle the case when the direct import fails, likely when executing through an external file
    from .utils import weather_functions
    from .utils import tapo_functions

# Absolute path of the current folder
folder_path = os.path.dirname(os.path.abspath(__file__))

# Logger configuration
log_file = os.path.join(folder_path, 'app.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Loading environment variables from the .env file
config_file = os.path.join(folder_path, 'config.env')
load_dotenv(config_file)

# Configuration values
cloudiness_breakpoint = int(os.getenv("CLOUDINESS_BREAKPOINT"))

# Tapo's plugs and bulbs configuration
tapo_email =   os.getenv("TAPO_EMAIL")
tapo_psw =     os.getenv("TAPO_PSW")
devices_info = os.getenv("DEVICES")
device_info_list = devices_info.split(";")  # split the elements using a semicolon as the delimiter
devices = []
for device_info in device_info_list:
    ip, model = device_info.split(":")      # split ip from model number using a colon as the delimiter
    device = {
        "ip":    ip,
        "email": tapo_email,
        "psw":   tapo_psw,
        "model": model
    }
    devices.append(device)

# OpenWeather parameters
latitude =  os.getenv("LATITUDE")
longitude = os.getenv("LONGITUDE")
api_key =   os.getenv("OPEN_WEATHER_API_KEY")

def start_control():
    # Get weather information
    weather_info = weather_functions.get_weather(latitude, longitude, api_key)

    if weather_info:
        # If the weather it's cloudy turn on the light
        cloudiness = weather_info["clouds"]["all"]
        threads = []
        if cloudiness > cloudiness_breakpoint:
            logging.info(f"Cloudy ({cloudiness}%), turing on the devices.")
            for device in devices:
                try:
                    thread = threading.Thread(target=tapo_functions.if_off_turn_on, args=([device]))
                    threads.append(thread)
                    thread.start()
                except Exception as e:
                    logging.error(f"Error occurred in the thread management (1): {str(e)}")
        else:
            logging.info(f"Not cloudy ({cloudiness}%), turning off the devices.")
            for device in devices:
                try:
                    thread = threading.Thread(target=tapo_functions.if_on_turn_off, args=([device]))
                    threads.append(thread)
                    thread.start()
                except Exception as e:
                    logging.error(f"Error occurred in the thread management (1): {str(e)}")
        for thread in threads:
            thread.join()
    else:
        logging.error("Unable to retrieve weather data.")
    
logging.info("------------------------------------------")

if __name__ == "__main__":
    start_control()
