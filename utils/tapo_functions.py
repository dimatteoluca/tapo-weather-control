import logging
import time
from PyP100 import PyP100   # pip install PyP100
from PyP100 import PyL530
try:
    from time_functions import get_remaining_minutes_until_next_hour
except ImportError:         # handle the case when the direct import fails, likely when executing through an external file
    from .time_functions import get_remaining_minutes_until_next_hour

def setup_p100(ip, email, psw):
    device = PyP100.P100(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the plug and creates AES Key and IV for further methods
    device.login()
    #logging.info(f"Plug info: {ip}, {device.getDeviceInfo()}")
    return device

def setup_l530(ip, email, psw):
    device = PyL530.L530(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the bulb and creates AES Key and IV for further methods
    device.login()
    #logging.info(f"Bulb info: {ip}, {device.getDeviceInfo()}")
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
        logging.error(f"{model} model is not supported.")

def try_to_setup(params):
    max_attempts = 6  # Maximum number of allowed attempts
    attempt = 1
    remaining_minutes_until_next_hour = get_remaining_minutes_until_next_hour()
    while True:
        try:
            device = device_setup(params)
            return device
        except Exception as e:
            #logging.error("Error during device setup: %s", str(e))
            logging.error("Error during device setup: the device is probably offline.")
            logging.info("Retrying setup in 10 minutes.")
            attempt += 1
            remaining_minutes_until_next_hour = get_remaining_minutes_until_next_hour()
            if attempt >= max_attempts or remaining_minutes_until_next_hour < 10:  # Perform retries for up to 50 mins
                break
            time.sleep(600)  # Wait for 10 minutes before retrying
    logging.info("Couldn't setup the device. Another attempt will be made later.")

def if_off_turn_on(params):
    device = try_to_setup(params)
    ip = params["ip"]
    try:
        info = device.getDeviceInfo()
        if info["result"]["device_on"] == False:
            device.turnOn()
        else:
            logging.info(f"The device {ip} was already on.")
    except AttributeError:
        logging.error(f"Couldn't setup the device {ip}.")

def if_on_turn_off(params):
    device = try_to_setup(params)
    ip = params["ip"]
    try:
        info = device.getDeviceInfo()
        if info["result"]["device_on"] == True:
            device.turnOff()
        else:
            ip = params["ip"]
            logging.info(f"The device {ip} was already off.")
    except AttributeError:
        logging.error(f"Couldn't setup the device {ip}.")
    
