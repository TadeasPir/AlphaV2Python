import logging

from src.models.user import User


class UserConsole:


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
            ("transfer points", self.transaction),
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
        user1 = User(username=input("name"),email= input("email"), credit_points=input("credit points"))
        user1.save()
    def update(self):
            user1 = User(user_id=input("id"),username=input("name"),email= input("email"), credit_points=input("credit points"))
            user1.save()
    def delete(self):
            user1 = User(user_id=input("id"))
            user1.delete()
    def transaction(self):
        user1 = input("from: id")
        user2 = input("to: id")
        ammount =int(input("ammount of credits"))
        User.transfer_credits(user1,user2,ammount)



    def find(self):
        user_temp = User(user_id=input("id")).find()
        user1 = User(user_id=user_temp[0], username=user_temp[1], email=user_temp[2],is_active=user_temp[3],credit_points=user_temp[4])
        print(repr(user1))


