import logging
from src.config import Config
from src.ui.achievement_console import AchievementConsole
from src.ui.game_console import GameConsole
from src.ui.library_console import LibraryConsole
from src.ui.reports_console import ReportConsole
from src.ui.review_console import ReviewConsole
from src.ui.user_console import UserConsole
from src.utils import setup_logging
from src.models.importing import import_users_from_csv




class AppConsole:

    def __init__(self,config: Config):
        self.isrunning = True
        self.config = config
        self._setup()
        self.table_console = [
            UserConsole(self),
            GameConsole(self),
            LibraryConsole(self),
            ReviewConsole(self),
            AchievementConsole(self),
            ReportConsole(self),
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

    def terminate(self):
        self.isrunning = False

    def print_line(self, symbol="-"):
        print(symbol * 60)

    def menu_input(self):
        commands = [
            ("Edit User ", self.table_console[0].menu_input),
            ("Edit Games", self.table_console[1].menu_input),
            ("Edit Library", self.table_console[2].menu_input),
            ("Edit review", self.table_console[3].menu_input),
            ("Edit achievements", self.table_console[4].menu_input),
            ("reports", self.table_console[5].menu_input),
            ("import users from csv", import_users_from_csv("./imports/users.csv")),


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

