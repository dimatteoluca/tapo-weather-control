import os, time
from dotenv import load_dotenv  # pip install python-dotenv
from PyP100 import PyP100, PyL530   # pip install PyP100
try:
    from log_setup import *
    from time_functions import get_remaining_minutes_until_next_hour
except ImportError:         # handle the case when the direct import fails, likely when executing through an external file
    from .log_setup import *
    from .time_functions import get_remaining_minutes_until_next_hour

# Absolute path of the current folder
folder_path = os.path.dirname(os.path.abspath(__file__))
# Absolute path of the parent folder
parent_folder_path = os.path.dirname(folder_path)

# Loading environment variables from the .env file
config_file = os.path.join(parent_folder_path, 'config.env')
load_dotenv(config_file)

# Config values
default_bulb_brightness =        int(os.getenv("DEFAULT_BULB_BRIGHTNESS"))
default_bulb_color_temperature = int(os.getenv("DEFAULT_BULB_COLOR_TEMPERATURE"))

def setup_p100(ip, email, psw):
    device = PyP100.P100(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the plug and creates AES Key and IV for further methods
    device.login()
    #logger_tw.info(f"Plug info: {ip}, {device.getDeviceInfo()}")
    return device

def setup_l530(ip, email, psw):
    device = PyL530.L530(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the bulb and creates AES Key and IV for further methods
    device.login()
    #logger_tw.info(f"Bulb info: {ip}, {device.getDeviceInfo()}")
    return device

def device_setup(params):
    ip =    params["ip"]
    email = params["email"]
    psw =   params["psw"]
    model = params["model"]
    if model == "P100":
        return setup_p100(ip, email, psw)
    elif model == "L530":
        return setup_l530(ip, email, psw)
    else:
        logger_tw.error(f"{model} model is not supported.")

def try_to_setup(params):
    max_attempts = 6  # Maximum number of allowed attempts
    attempt = 1
    remaining_minutes_until_next_hour = get_remaining_minutes_until_next_hour()
    while True:
        try:
            device = device_setup(params)
            return device
        except Exception as e:
            #logger_tw.error("Error during device setup: %s", str(e))
            logger_tw.error("Error during device setup: the device is probably offline.")
            logger_tw.info("Retrying setup in 10 minutes.")
            attempt += 1
            remaining_minutes_until_next_hour = get_remaining_minutes_until_next_hour()
            if attempt >= max_attempts or remaining_minutes_until_next_hour < 10:  # Perform retries for up to 50 mins
                break
            time.sleep(600)  # Wait for 10 minutes before retrying
    logger_tw.info("Couldn't setup the device. Another attempt will be made later.")

def if_off_turn_on(params):
    device = try_to_setup(params)
    ip = params["ip"]
    try:
        device_name = device.getDeviceName()
        info = device.getDeviceInfo()
        if info["result"]["device_on"] == True:
            logger_tw.info(f"The device '{device_name}' ({ip}) was already on.")
        elif params["model"] == "P100":
            device.turnOn()
        if params["model"] == "L530":
            device.setBrightness(default_bulb_brightness)
            device.setColorTemp(default_bulb_color_temperature)
            logger_tw.info(f"'{device_name}'s brightness and color temperature were set to default values.")
        #else:
        #    logger_tw.info(f"The device '{device_name}' ({ip}) was already on.")
    except AttributeError:
        logger_tw.error(f"Couldn't setup the device {ip}.")

def if_on_turn_off(params):
    device = try_to_setup(params)
    ip = params["ip"]
    try:
        device_name = device.getDeviceName()
        info = device.getDeviceInfo()
        if info["result"]["device_on"] == True:
            device.turnOff()
        else:
            logger_tw.info(f"The device '{device_name}' ({ip}) was already off.")
    except AttributeError:
        logger_tw.error(f"Couldn't setup the device {ip}.")
