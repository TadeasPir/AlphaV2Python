import logging

from src.models.game import Game


class GameConsole:
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
        game1 = Game(title=input("title"),release_date= input("relese date: YYYY-MM-DD"), genre=input("genre"),price=float(input("price")),is_multiplayer=bool(input("is multiplayer? ")))
        game1.save()
    def update(self):
            game1 = Game(game_id=int(input("game_id")), title=input("title"),release_date= input("relese date: YYYY-MM-DD"), genre=input("genre"),price=float(input("price")),is_multiplayer=bool(input("is multiplayer? ")))
            game1.save()
    def delete(self):
            game1 = Game(game_id=input("id"))
            game1.delete()


    def find(self):
        game_temp = Game(game_id=input("id")).find()
        game1 = Game(game_id=game_temp[0], title=game_temp[1], release_date=game_temp[2], genre=game_temp[3], price=game_temp[4], is_multiplayer=game_temp[5])
        print(repr(game1))

