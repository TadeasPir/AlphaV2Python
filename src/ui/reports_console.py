import logging

from Tools.scripts.fixdiv import report

from src.models.game import Game
from src.models.report import Report


class ReportConsole:
    def __init__(self, interface):
        self.isrunning = True
        self.interface = interface

    def run(self):
        self.isrunning = True
        while self.isrunning:
            self.menu_input()

    def print_message(self, message):
        self.interface.print_line()
        print(message)

    def menu_input(self):
        commands = [
            ("game overview", self.v_game_overview),
            ("user library stats", self.v_user_library_stats),
            ("exit", self.terminate()),
        ]

        self.interface.print_line()
        print("choose operation:")
        num = 0
        for label, action in commands:
            num += 1
            print("\t" + str(num) + ". " + label)

        choosen_num = None
        while choosen_num is None:
            choosen_num = input("input operation number (1-" + str(len(commands)) + "): ").strip()
            try:
                choosen_num = int(choosen_num)
                if not 0 < choosen_num <= len(commands):
                    raise Exception()
            except:
                logging.exception("invalid input do 1 to " + str(len(commands)))
                choosen_num = None

        commands[choosen_num - 1][1]()
        if self.isrunning:
            self.run()

    def terminate(self):
        self.isrunning = False

    def v_game_overview(self):
        report1 = Report()
        report1.v_game_overview()

    def v_user_library_stats(self):
        report1 = Report()
        report1.v_user_library_stats()

