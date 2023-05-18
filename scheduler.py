import datetime
import logging
import schedule
import sys
import time
from astral.sun import sun          # pip install astral
from astral import LocationInfo
from TapoWeatherControl import *

# Logger configuration
logging.basicConfig(filename='./app.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Configuration values
first_hour = 9

# Global variables
sunset_time = None

# Get the sunset time for the specified coordinates
def set_sunset_time(latitude, longitude):
    global sunset_time
    try:
        if not (-90 <= float(latitude) <= 90 and -180 <= float(longitude) <= 180):  # check the validity of coordinates
            raise ValueError("Invalid coordinates")
        city = LocationInfo(latitude, longitude)
        sun_info = sun(city.observer, date=datetime.date.today())
        sunset_time = sun_info['sunset']
    except ValueError as ve:
        logging.error(f"Invalid coordinates: {str(ve)}")
        # Terminate execution in case of invalid coordinates
        sys.exit(1)  
    except Exception as e:
        logging.error(f"Error occurred while getting sunset time: {str(e)}")
        # Emit a warning but continue execution using a default sunset time
        logging.warning("Continuing execution with default sunset time.")
        sunset_time = datetime.datetime.now().replace(hour=18, minute=40, second=0)

# Get the range of hours in which the script needs to be executed
def get_target_range():
    global sunset_time
    last_hour = sunset_time.hour-1
    current_hour = datetime.datetime.now().hour
    if (current_hour > first_hour) and (current_hour < last_hour):
        target_range = range(current_hour-1, last_hour)
    else:
        target_range = range(first_hour-1, last_hour)
    return target_range

# Schedule for 1 minute before every hour between 9AM and the sunset time
def schedule_action():
    try:
        target_range = get_target_range()
        for hour in target_range:
            schedule.every().day.at(f"{hour}:59").do(start)
    except Exception as e:
        logging.error(f"Error occurred while scheduling action: {str(e)}")

def reschedule_action():
    schedule.clear()
    schedule_action()

# Wait to make sure the scheduled event is executed on the hour
def wait_until(target_time):
    try:
        now = datetime.datetime.now().time()
        target = datetime.time(*target_time)  # target_time is a tuple (hours, minutes, seconds)
        # Calculate the time difference between the current time and the desired time
        delta = datetime.datetime.combine(datetime.date.today(), target) - datetime.datetime.combine(datetime.date.today(), now)
        # Wait until the desired hour
        time.sleep(delta.seconds)
    except Exception as e:
        logging.error(f"Error occurred while waiting: {str(e)}")

# Wait until the next hour
def wait_until_next_hour():
    try:
        now = datetime.datetime.now()
        next_hour = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
        time_difference = (next_hour - now).total_seconds()
        time.sleep(time_difference)
    except Exception as e:
        logging.error(f"Error occurred while waiting for the next hour: {str(e)}")

def main_loop():
    global sunset_time
    try:
        set_sunset_time(latitude, longitude)
        logging.info(f"Today's sunset time is: {sunset_time}")
        reschedule_action()
        target_range = get_target_range()
        current_hour = datetime.datetime.now().hour
        last_hour = sunset_time.hour - 1
        logging.info(f"Last hour is: {last_hour}")
        if (current_hour > first_hour) and (current_hour < last_hour):
            start()
            logging.info("Waiting for the next hour.")
            wait_until_next_hour()
        else:
            logging.info("Waiting for 9AM.")
            wait_until([9, 0, 0])  # wait until 9AM
        for hour in target_range:
            # Check if there are pending scheduled events and execute them
            schedule.run_pending()
            # Wait 1 hour
            wait_until_next_hour()
        wait_until([1, 0, 0])      # wait until 1AM
    except KeyboardInterrupt:
        logging.info("Program interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Error occurred in the main loop: {str(e)}")
        # Terminate execution in case of critical errors
        sys.exit(1) 

if __name__ == "__main__":
    while True:
        main_loop()
