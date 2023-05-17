import logging
from PyP100 import PyP100   # pip install PyP100
from PyP100 import PyL530

def setup_p100(ip, email, psw):
    device = PyP100.P100(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the plug and creates AES Key and IV for further methods
    device.login()
    logging.info(f"Plug {ip}: {device.getDeviceInfo()}")
    return device

def setup_l530(ip, email, psw):
    device = PyL530.L530(ip, email, psw)
    # Create the cookies required for further methods
    device.handshake()
    # Send credentials to the bulb and creates AES Key and IV for further methods
    device.login()
    logging.info(f"Bulb {ip}: {device.getDeviceInfo()}")
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

def if_off_turn_on(params):
    device = device_setup(params)
    info = device.getDeviceInfo()
    if info["result"]["device_on"] == False:
        device.turnOn()
    else:
        logging.info("The device was already on.")

def if_on_turn_off(params):
    device = device_setup(params)
    info = device.getDeviceInfo()
    if info["result"]["device_on"] == True:
        device.turnOff()
    else:
        logging.info("The device was already off.")