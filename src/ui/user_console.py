from src.models.user import User


class UserConsole:


    def __init__(self, interface):
        self.isrunning = True
        self.interface = interface
        self.table_application = User(self)

    def run(self):
        self.isrunning = True
        while self.isrunning:
            self.menu_input()

    def print_message(self, message):
        self.interface.print_line()
        print(message)

    def menu_input(self):
        commands = [
            ("1. Add", self.table_application.save),
            ("2. edit", self.table_application.update),
            ("3. delete", self.table_application.DeleteCustomer),
            ("4. read", self.table_application.ReadCustomer),
            ("5. end", self.terminate),
        ]

        self.interface.print_line()
        print("choose operation:")
        num = 0
        for label, action in commands:
            num += 1
            print("\t" + str(num) + ". " + label)

        choosen_num = None
        while choosen_num is None:
            choosen_num = input("Zadejte číslo příkazu (1-" + str(len(commands)) + "): ").strip()
            try:
                choosen_num = int(choosen_num)
                if not 0 < choosen_num <= len(commands):
                    raise Exception()
            except:
                print("Neplatné zadání musíte zadat číslo mezi 1 až " + str(len(commands)))
                choosen_num = None

        commands[choosen_num - 1][1]()
        if self.isrunning:
            self.run()

    def terminate(self):
        self.isrunning = False

    def proces_input(self, message):
        return self.interface.new_input(message)

    def confirmation(self):
        self.interface.print_line()
        answer = None
        while not answer:
            try:
                answer = input("Opravdu chcete provést tuto akci? (ano/ne): ").lower()
                if (answer not in ["ano", "ne"]):
                    raise Exception
            except Exception:
                print("Neplatné zadání musíte zadat číslo 0 nebo 1")
                answer = None
        if (answer == "ano"):
            return True
        else:
            return False