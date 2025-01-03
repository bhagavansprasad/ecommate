import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Adjust the logging level as needed
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Log to a file
            logging.StreamHandler()  # Print logs to the console
        ],
    )
