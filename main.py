import os
# from WebApplication import wp_main
from Security import s_main
from Networking import n_main
from SocialEngineering import se_main


red = "\33[91m"
blue = "\33[94m"
green = "\33[92m"


def banner_fun():

    banner = f"""
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
    Github : https://github.com/ParthB2007/knightfall {green}
              
===================================================== """

    print(banner)


def main_option_panel():
    temp = True

    print(f"{green}"
          "\n 1. WebApplication"
          "\n 2. Security"
          "\n 3. Networking"
          "\n 4. Social Engineering"
          "\n 9. help"
          "\n 0. Exit")


    while temp:
        option = int(input("\nSelect Option > "))
        if option == 1:
            #print("\nWorking on it")
            # wsp_main.main()
            break

        elif option == 2:
            s_main.main()
            break

        elif option == 3:
            n_main.main()
            break

        elif option == 4:
            se_main.main()
            break

        elif option == 9:
            tree ="""
        Project KnightFall
            ├── WebApplication
            │   ├── Crawler
            │   └── BruteForce
            ├── Security
            │   ├── EncryptionTool
            │   ├── DecryptionTool
            │   └── SteganographyTool
            └── Networking
                ├── PacketCaptureTool
                └── PortScannerTool
            """

            print(tree)


        elif option == 0:
            temp = False

        else:
            print("Enter from above option")
def main():
    banner_fun()
    main_option_panel()

if __name__ == "__main__":
    os.system("cls")
    main()