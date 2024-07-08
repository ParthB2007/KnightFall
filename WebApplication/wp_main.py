import os
import crawler

green = "\33[92m"
print(green)
def wp_optionpanel():
    
   
    wp_banner ="""

-----------------------------------------------------
                    Web-Application
-----------------------------------------------------

    """
    print(wp_banner+"\n")

    temp = True 
    while temp:
        print("1.Web Crawler "
              "\n2.BruteForce"
              )
        option = int(input("\nSelect option > "))
        if option == 1:
            crawler.main()
            break
        
        if option == 2:  
            print("Working on it")
            break
        else:
            print("Please select valid option")




def main():
    
    wp_optionpanel()

if __name__ == '__main__':
    
    os.system("cls")
    main()