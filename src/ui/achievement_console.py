import logging
from datetime import datetime

from src.models.achievement import Achievement


class AchievementConsole:
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
            ("add", self.add),
            ("edit", self.update),
            ("delete", self.delete),
            ("read", self.find),
            ("end", self.terminate),
        ]

        self.interface.print_line()
        print("choose operation:")
        num = 0
        for label, action in commands:
            num += 1
            print("\t" + str(num) + ". " + label)

        choosen_num = None
        while choosen_num is None:
            choosen_num = input("iput operation number (1-" + str(len(commands)) + "): ").strip()
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
    # self, achievement_id=None, user_id=None, game_id=None, achievement_title=None, date_earned=None, points_earned=0.0
    def add(self):
        achievement1 = Achievement(user_id= int(input("user id")),game_id=int(input(" game id")), achievement_title=input("achievement title"),date_earned=datetime.now().strftime('%Y-%m-%d'),points_earned=float(input("points earned ")))
        achievement1.save()
    def update(self):
            achievement1 = Achievement(achievement_id=int(input("achievement_id id")),user_id=int(input("user id")),game_id= int(input(" game id")), achievement_title=input("achievement title"),date_earned=datetime.now().strftime('%Y-%m-%d'),points_earned=float(input("points earned ")))
            achievement1.save()
    def delete(self):
            achievement1 = Achievement(game_id=input("id"))
            achievement1.delete()


    def find(self):
        achievement_temp = Achievement(game_id=input("id")).find()
        achievement1 = Achievement(achievement_id=achievement_temp[0], title=achievement_temp[1], release_date=achievement_temp[2], genre=achievement_temp[3], price=achievement_temp[4], is_multiplayer=achievement_temp[5])
        print(repr(achievement1))

