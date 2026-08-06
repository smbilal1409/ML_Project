import logging
import os
from datetime import datetime

# Create a unique log file name using the current date and time
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the logs directory path
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# Create the logs folder if it doesn't exist
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

# Full path of the log file
LOG_FILE_PATH = logs_path

# Configure the logger
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Create a logger object
logger = logging.getLogger(__name__)