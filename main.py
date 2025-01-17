import logging

from src.config import Config
from src.database.database import Database
from src.ui.app_console import AppConsole

def main():

    # Load configuration
    try:
        config = Config("config/config.yaml")
    except Exception as e:
        logging.error(f"Error during execution: {e}")

    # Create and run the crawler application
    app = AppConsole(config)


    try:
        app.run()

    except Exception as e:
        logging.error(f"Error during execution: {e}")
        app.run()



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        logging.info(f"interuped by keyboard: {e}")