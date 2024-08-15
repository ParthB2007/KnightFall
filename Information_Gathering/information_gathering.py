import os

# Adjust the import statements based on your actual file names
from Web_Crawler import crawler
from Hidden_File_Enumeration import fuzz
from Port_Scanner import port_scanner

green = "\33[92m"
print(green)

def print_help():
    help_text = """
1. Web Web_Crawler:
   A tool for crawling websites to gather data from web pages, such as links and content.

2. Hidden File Enumeration:
   A tool for identifying and enumerating hidden files and directories on a web server.

3. Open Port Scanner:
   A tool for scanning a range of ports on a target server to identify open and potentially vulnerable ports.
    """
    print(help_text)

def ig_panel():
    wp_banner = """
-----------------------------------------------------
                Information Gathering
-----------------------------------------------------
    """
    print(wp_banner)

    temp = True
    while temp:
        print(f"""
    1. Web Crawler  
    2. Hidden File Enumeration
    3. Open Port Scanner
    4. Help
    """)
        try:
            option = int(input("\nSelect option > "))

            if option == 1:
                crawler.main()

            elif option == 2:
                fuzz.main()

            elif option == 3:
                Port_scanner.main()

            elif option == 4:
                print_help()

            else:
                print("Please select a valid option")

        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    ig_panel()

if __name__ == '__main__':
    os.system("cls")
    main()
