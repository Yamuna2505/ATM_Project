import json
import os
from getpass import getpass
from datetime import datetime

DB_FILE = 'users.json'

# Load or initialize data
def load_data():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump({}, f)
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class ATM:
    def __init__(self):
        self.users = load_data()
        self.current_user = None

    def login(self):
        card = input("Enter Card Number: ")
        pin = getpass("Enter PIN: ")

        user = self.users.get(card)
        if user and user["pin"] == pin:
            self.current_user = card
            print(f"\nWelcome {user['name']}!")
            return True
        else:
            print("Invalid card number or PIN.\n")
            return False

    def main_menu(self):
        while True:
            print("\n--- ATM Main Menu ---")
            print("1. Balance Inquiry")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Change PIN")
            print("5. View Mini Statement")
            print("6. Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                self.check_balance()
            elif choice == '2':
                self.deposit()
            elif choice == '3':
                self.withdraw()
            elif choice == '4':
                self.change_pin()
            elif choice == '5':
                self.mini_statement()
            elif choice == '6':
                print("Thank you for using the ATM. Goodbye!")
                break
            else:
                print("Invalid option.")

    def check_balance(self):
        print(f"Current Balance: ₹{self.users[self.current_user]['balance']}")

    def deposit(self):
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Invalid amount.")
            return
        self.users[self.current_user]['balance'] += amount
        self.add_transaction(f"Deposited ₹{amount}")
        save_data(self.users)
        print("Deposit successful.")

    def withdraw(self):
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0:
            print("Invalid amount.")
            return
        if amount > self.users[self.current_user]['balance']:
            print("Insufficient balance.")
        else:
            self.users[self.current_user]['balance'] -= amount
            self.add_transaction(f"Withdrew ₹{amount}")
            save_data(self.users)
            print("Withdrawal successful.")

    def change_pin(self):
        old_pin = getpass("Enter current PIN: ")
        if old_pin != self.users[self.current_user]["pin"]:
            print("Incorrect PIN.")
            return
        new_pin = getpass("Enter new PIN: ")
        confirm_pin = getpass("Confirm new PIN: ")
        if new_pin != confirm_pin:
            print("PINs do not match.")
            return
        self.users[self.current_user]["pin"] = new_pin
        save_data(self.users)
        print("PIN changed successfully.")

    def mini_statement(self):
        transactions = self.users[self.current_user].get("transactions", [])
        print("\n--- Mini Statement ---")
        for txn in transactions[-5:]:
            print(txn)

    def add_transaction(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txn = f"{timestamp} - {description}"
        self.users[self.current_user].setdefault("transactions", []).append(txn)

    def register_sample_user(self):
        if "12345678" not in self.users:
            self.users["12345678"] = {
                "name": "John Doe",
                "pin": "1234",
                "balance": 1000.0,
                "transactions": []
            }
            save_data(self.users)
            print("Sample user added: Card Number=12345678, PIN=1234")

if __name__ == "__main__":
    atm = ATM()
    atm.register_sample_user()

    if atm.login():
        atm.main_menu()
