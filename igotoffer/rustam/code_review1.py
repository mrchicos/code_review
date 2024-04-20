import pickle
from getpass import getpass

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account = BankAccount()

    def check_password(self, password):
        return password == self.password

class BankAccount:
    def __init__(self):
        self.balance = 0.0

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance

class BankSystem:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self):
        try:
            with open('users.dat', 'rb') as file:
                return pickle.load(file)
        except (FileNotFoundError, EOFError):
            return {}

    def save_users(self):
        with open('users.dat', 'wb') as file:
            pickle.dump(self.users, file)

    def register(self, username, password):
        if username in self.users:
            return False
        self.users[username] = User(username, password)
        self.save_users()
        return True

    def login(self, username, password):
        user = self.users.get(username)
        if user and user.check_password(password):
            return user
        return None

    def run(self):
        while True:
            print("\nWelcome to Simple Bank System")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                username = input("Enter a new username: ")
                password = getpass("Enter a new password: ")
                if self.register(username, password):
                    print("Registration successful.")
                else:
                    print("Username already exists.")
            elif choice == '2':
                username = input("Enter your username: ")
                password = getpass("Enter your password: ")
                user = self.login(username, password)
                if user:
                    self.user_menu(user)
                else:
                    print("Invalid username or password.")
            elif choice == '3':
                break
            else:
                print("Invalid choice. Please try again.")

    def user_menu(self, user):
        while True:
            print("\nWelcome, {}".format(user.username))
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == '1':
                print("Your current balance is: ${:.2f}".format(user.account.get_balance()))
            elif choice == '2':
                amount = float(input("Enter amount to deposit: "))
                if user.account.deposit(amount):
                    print("Deposit successful.")
                else:
                    print("Invalid amount.")
            elif choice == '3':
                amount = float(input("Enter amount to withdraw: "))
                if user.account.withdraw(amount):
                    print("Withdrawal successful.")
                else:
                    print("Insufficient funds or invalid amount.")
            elif choice == '4':
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    system = BankSystem()
    system.run()