import os
from Information_Gathering import information_gathering

# Color definitions
green = "\33[92m"
red = "\33[91m"
blue = "\33[94m"


def banner_fun():
    banner = rf"""
{green}
=====================================================
     _   __      _       _     _      __      _ _ 
    | | / /     (_)     | |   | |    / _|    | | |
    | |/ / _ __  _  __ _| |__ | |_  | |_ __ _| | |
    |    \| '_ \| |/ _` | '_ \| __| |  _/ _` | | |
    | |\  \ | | | | (_| | | | | |_  | || (_| | | |
    \_| \_/_| |_|_|\__, |_| |_|\__| |_| \__,_|_|_|
                    __/ |                         
                   |___/              
{blue}
Created by : Parth Baldha
Github : https://github.com/ParthB2007/knightfall
{green}              
=====================================================
"""
    print(banner)


def main_option_panel():
    temp = True
    print(f"{green}"
          "\n 1. Information_Gathering"
          "\n 2. Vulnerability Scanning"
          "\n 3. Help"
          "\n 0. Exit")

    while temp:
        option = int(input("\nSelect Option > "))

        if option == 1:
            information_gathering.main()
            break

        # elif option == 2:
        #     s_main.main()  # Assuming s_main is defined elsewhere
        #     break

        elif option == 3:
            help_panel()


        elif option == 0:
            temp = False

        else:
            print("Please select a valid option")


def help_panel():
    tree = r"""
Project KnightFall
    ├── Information_Gathering
    │   ├── Web Web_Crawler
    │   ├── Hidden File Enumeration
    │   └── Open Port Scanner
    │
    └── Vulnerability Scanning
        └── Security Header Scanner
"""
    print(tree)


def main():
    banner_fun()
    main_option_panel()


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
