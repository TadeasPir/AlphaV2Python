import logging
from datetime import datetime

from src.models.library import Library


class LibraryConsole:
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

    def add(self):
        library1 = Library(user_id=int(input("user_id")), game_id=int(input("game_id")), purchase_date= datetime.now().strftime('%Y-%m-%d'), has_dlc=bool(input("has DLC ")))
        library1.save()
    def update(self):
       library1 = Library(user_id=int(input("user_id")), game_id=int(input("game_id")), purchase_date=datetime.now().strftime('%Y-%m-%d'), has_dlc=bool(input("has DLC ")))
       library1.save()
    def delete(self):
       library1 = Library(user_id=int(input("user_id")), game_id=int(input("game_id")))
       library1.delete()


    def find(self):
        library_temp = Library(user_id=int(input("id of user")),game_id=int(input("id of game"))).find()
        library1 = Library(user_id=library_temp[0], game_id=library_temp[1], purchase_date=library_temp[2], has_dlc=library_temp[3])
        print(repr(library1))

