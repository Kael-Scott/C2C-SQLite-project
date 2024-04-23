from os import system

from pwinput import pwinput

import messages as msg
from banking import Banking

bank = Banking()

def create():
    print(msg.create)
    email = input("\nPlease enter a valid email: ")
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    while True:
        passcode = pwinput("Please enter a passcode: ")
        confirmed = pwinput("Re-enter your passcode to confirm: ") == passcode
        if confirmed:
            break
        else:
            print("Password missmatch. Try again.")
    result = bank.create_account(email, first_name, last_name, passcode)
    if result:
        print("\nCreated account successfully!")
    else:
        print("\nAccount creation failed! This email may already be registered!")
    return result

def login():
    choice = int(input(f"{msg.login}\n\n> "))-1
    id = int(input("\nPlease enter a valid account number: ")) if choice else 0
    email = input("\nPlease enter a valid email: ") if not choice else ""
    passcode = pwinput("Please enter your password: ")
    result = bank.login(passcode, id, email)
    if result:
        print("\nSucessfully logged in!")
    else:
        print("\nCouldn't log in. Did you enter the correct information?")
    return result

def confirm(message):
    while True:
        system('clear')
        choice = input(f"{message}\n\n> ").lower()
        if choice == "y":
            return True
        elif choice != "n":
            continue
        return False

def delete():
    global bank
    if not confirm(msg.delete):
        print("\nCanceled deletion.")
        return False
    passcode = pwinput("\nPlease enter your passcode: ")
    res = bank.delete_account(passcode)
    if not res:
        print("\nInvalid passcode.")
    else:
        print("\nSucessfully deleted account.")
        bank = Banking()
    return True

def logout():
    global bank
    if not confirm(msg.delete):
        print("\nCanceled log out.")
        return False
    bank = Banking()
    print("Sucessfully logged out.")
    return True

def deposit():
    ""

def withdraw():
    ""

def transfer():
    ""

def menu(options):
    try:
        userinp = int(input("\nEnter a number:\n\n> "))-1
        system('clear')
        for i, f in enumerate(options):
            if userinp == i:
                return f()
        raise ValueError
    except ValueError:
        print("\nBad value! Try again.")

# Main loop

start_options = [create, login, exit]
account_options = [1, 2, 3, logout, delete]

while True:
    system('clear')
    if not bank.account_data:
        print(msg.welcome)
        menu(start_options)
    else:
        print(msg.account)
        menu(account_options)
    input("Hit enter to continue.")