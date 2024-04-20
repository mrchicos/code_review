import hashlib
import os
import pickle
from getpass import getpass
import statistics
from collections import defaultdict

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = self._encrypt_password(password)
        self.account = BankAccount()

    def _encrypt_password(self, password):
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return salt + key
    
    def check_password(self, password):
        salt = self.password[:32]
        key = self.password[32:]
        attempt_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return key == attempt_key

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
                self.save_users()
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

def load_users(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
def calculate_insights(users):
    balances = [user.account.get_balance() for user in users.values()]
    max_balance = max(balances) if balances else 0
    min_balance = min(balances) if balances else 0
    avg_balance = statistics.mean(balances) if balances else 0

    return {
        'max_balance': max_balance,
        'min_balance': min_balance,
        'avg_balance': avg_balance,
        'total_balance': sum(balances),
        'balance_distribution': calculate_balance_distribution(balances)
    }

def calculate_balance_distribution(balances):
    distribution = defaultdict(int)
    for balance in balances:
        if balance < 1000:
            distribution['<1000'] += 1
        elif balance < 5000:
            distribution['1000-4999'] += 1
        else:
            distribution['5000+'] += 1
    return distribution

def display_insights(insights):
    print("Banking Insights Report")
    print("-----------------------")
    print(f"Max Balance: ${insights['max_balance']:.2f}")
    print(f"Min Balance: ${insights['min_balance']:.2f}")
    print(f"Avg Balance: ${insights['avg_balance']:.2f}")
    print(f"Total Bank Balance: ${insights['total_balance']:.2f}")
    print("Balance Distribution:")
    for range, count in insights['balance_distribution'].items():
        print(f"  {range}: {count} users")

if __name__ == "__main__":
    if os.path.exists('users.dat'):
        users = load_users('users.dat')
        insights = calculate_insights(users)
        display_insights(insights)
    system = BankSystem()
    system.run()