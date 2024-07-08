#web crawler
#above line should not be change 


import os
import argparse

green = "\33[92m"
print(green)


def create_project_dir(directory):
    if not os.path.exists(directory):
        print("initiating Project " + directory)
        os.mkdir(directory)
        print("Directory created Successfully...")
    else:
        print("Directory already exists...")

def create_data_files(project_name,base_url):
    queue = project_name + "/queue.txt"
    crawled = project_name + "/crewled.txt"
    if not os.path.isfile(queue):
        write_file(queue,base_url)
    if not os.path.isfile(crawled):
        write_file(crawled,"")


def write_file(path,data):
    f = open(path,'w')
    f.write(data)
    f.close()

def append_data(path,data):
    with open(path,'a') as file:
        file.write(data + "\n")

def promote():
    input(__file__)

def main():

    
    create_project_dir(dir)

    

if __name__ == '__main__':

    os.system('cls')
    main()