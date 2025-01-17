import logging
from src.config import Config
from src.ui.user_console import UserConsole
from src.utils import setup_logging





class AppConsole:

    def __init__(self,config: Config):
        self.config = config
        self._setup()
        self.table_user_console = [
            UserConsole(self),

        ]
        logging.info("AppConsole initialized.")

    def _setup(self):
        setup_logging(self.config.logging_level, self.config.logging_file)
        logging.info("Application setup started.")
        try:


            logging.info("Application setup completed.")
        except Exception:
            logging.exception("Application setup failed.")

    def run(self):
        while self.isrunning:
            self.menu_input()

    def menu_input(self):
        commands = [
            ("1 Edit User ", self.table_user_interface[0].menu_input),
            ("2", self.table_user_interface[1].menu_input),
            ("3", self.table_user_interface[2].menu_input),
            ("4", self.table_user_interface[3].menu_input),
            ("5", self.table_user_interface[4].menu_input),
            ("5", self.table_user_interface[5].menu_input),
            ("6", self.table_user_interface[6].menu_input),
            ("7 reports", self.table_user_interface[7].menu_input),
            ("end ", self.terminate),
        ]

        self.print_line()
        print("Choose operation:")
        num = 0
        for label, action in commands:
            num += 1
            print("\t" + str(num) + ". " + label)

        choosen_num = None
        while (choosen_num == None):
            choosen_num = input("input a number of command (1-" + str(len(commands)) + "): ").strip()
            try:
                choosen_num = int(choosen_num)
                if (not 0 < choosen_num <= len(commands)):
                    logging.exception("Invalid input.")
                    raise Exception()
            except:
                logging.error("invalid input you must input a number i range 1 to " + str(len(commands)))
                choosen_num = None

        commands[choosen_num - 1][1]()

        def terminate(self):
            self.isrunning = False