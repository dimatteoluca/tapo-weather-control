import logging, os

# Absolute path of the current folder
folder_path = os.path.dirname(os.path.abspath(__file__))

# Logger setup
logger_tw = logging.getLogger("TW")
logger_tw.setLevel(logging.INFO)
formatter_tw = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')
# File handler
tw_log_file = os.path.join(folder_path, 'app.log')
tw_file_handler = logging.FileHandler(tw_log_file)
tw_file_handler.setLevel(logging.INFO)
tw_file_handler.setFormatter(formatter_tw)
logger_tw.addHandler(tw_file_handler)
# Stream handler
tw_stream_handler = logging.StreamHandler()
tw_stream_handler.setLevel(logging.INFO)
tw_stream_handler.setFormatter(formatter_tw)
logger_tw.addHandler(tw_stream_handler)
