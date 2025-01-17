import logging
from datetime import datetime

from src.models.review import Review


class ReviewConsole:
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

        review1 = Review(game_id=int(input("game id")),user_id=int(input("user id")),review_date= datetime.now().strftime('%Y-%m-%d'), rating=float(input("rating")),review_text=input("review"))
        review1.save()
    def update(self):
            review1 = Review(review_id=int(input("review id")),game_id=int(input("game id")),user_id=int(input("user id")),review_date= datetime.now().strftime('%Y-%m-%d'), rating=float(input("rating")),review_text=input("review "))
            review1.save()
    def delete(self):
            review1 = Review(review_id=input("id"))
            review1.delete()

    def find(self):
        review_temp = Review(review_id=input("id")).find()
        review1 = Review(review_id=review_temp[0], game_id=review_temp[1], user_id=review_temp[2], rating=review_temp[3], review_text=review_temp[4], review_date=review_temp[5])
        print(repr(review1))