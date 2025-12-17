"""
Loggers exercise logging_e001:
Basic Logger Setup with Multiple Handlers

Concepts: Logger initialization, handlers, log levels, formatting
Domain: General-purpose application logging
"""

import logging
from pathlib import Path

# Get the current script directory as a Path object
root_folder = Path(__file__).parent

# Define the logs folder path
logs_folder = root_folder / "logs"

# TODO: Create a logger for your application
# HINT: Use logging.getLogger() with a descriptive name (e.g., 'data_pipeline')
logger = logging.getLogger("data_pipeline")  # Replace with your logger creation

# TODO: Set the logger's level to capture all messages
# HINT: Use logger.setLevel() with logging.DEBUG
logger.setLevel(logging.DEBUG)
# Approach: The logger level is the FIRST filter; messages below this level won't
# proceed to handlers

# TODO: Create a console handler (StreamHandler)
# HINT: logging.StreamHandler() outputs to sys.stderr by default
console_handler = logging.StreamHandler()  # Replace with StreamHandler

# TODO: Set the console handler's level to INFO
# HINT: Handler level is the SECOND filter applied after the logger level
# This means console_handler.setLevel(logging.INFO) will filter out DEBUG messages
# from console
console_handler.setLevel(logging.INFO)  # Replace with logging.INFO

# TODO: Create a file handler (FileHandler)
# HINT: logging.FileHandler('filename.log') creates a file handler
# For this exercise, use a filename like 'app.log'
log_file_path = logs_folder / "app.log"

file_handler = logging.FileHandler(log_file_path)  # Replace with FileHandler

# TODO: Set the file handler's level to DEBUG
# HINT: File handlers often capture more detail than console
file_handler.setLevel(logging.DEBUG)  # Replace with logging.DEBUG

# TODO: Create a formatter that includes timestamp, level name, and message
# HINT: Use logging.Formatter() with a format string like:
# '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Approach: The formatter controls how the log message appears
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  # Replace with Formatter

# TODO: Attach the formatter to both handlers
# HINT: Use handler.setFormatter(formatter) for each handler
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# TODO: Add handlers to the logger
# HINT: Use logger.addHandler(handler) for each handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# TODO: Test your logger with messages at different levels
# Include: DEBUG, INFO, WARNING, ERROR
# HINT: Use logger.debug(), logger.info(), logger.warning(), logger.error()

# Sample test
if __name__ == "__main__":
    # Create the logs folder if it doesn't exist (including parents)
    logs_folder.mkdir(parents=True, exist_ok=True)
    logger.info(f"Logs folder directory: {logs_folder}")

    # Test your logger setup by logging at different levels
    # Expected output: Console shows INFO+, file shows DEBUG+
    logger.debug("Debugging test message")
    logger.info("Info test message")
    logger.warning("Warning test message")
    logger.error("Error test message")
