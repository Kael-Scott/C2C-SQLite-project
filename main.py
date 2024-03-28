import os
import time

while True:
    os.system('clear')
    print(
"""
\\---------------------------------------------------/
|                        Welcome!                   |
|    Please select one of the following options:    |
|                                                   |
| 1 )  Create account                               |
| 2 )  Log in                                       |
|                                                   |
/---------------------------------------------------\\
"""
    )
    try:
        choice = int(input("\nEnter a number:\n\n> "))
        if choice == 1:
            "Do something"
        elif choice == 2:
            "Do something else"
        else:
            raise ValueError
        break
    except ValueError:
        print("Bad value! Try again.")
        time.sleep(2)