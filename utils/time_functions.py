import datetime
import logging
import time

def get_remaining_minutes_until_next_hour():
    current_time = datetime.datetime.now()
    remaining_minutes = 60 - current_time.minute
    return remaining_minutes

# Wait to make sure the scheduled event is executed on the hour
def wait_until(target_time):
    try:
        now = datetime.datetime.now().time()
        target = datetime.time(*target_time)  # target_time is a tuple (hours, minutes, seconds)
        # Calculate the time difference between the current time and the desired time
        delta = datetime.datetime.combine(datetime.date.today(), target) - datetime.datetime.combine(datetime.date.today(), now)
        # Wait until the desired hour
        logging.info("Waiting until:           %s", target.strftime('%H:%M'))
        time.sleep(delta.seconds)
    except Exception as e:
        logging.error(f"Error occurred while waiting: {str(e)}")

# Wait until the next hour
def wait_until_next_hour():
    try:
        next_hour = datetime.datetime.now().hour + 1
        wait_until([next_hour, 0, 0])
    except Exception as e:
        logging.error(f"Error occurred while waiting until next hour: {str(e)}")
