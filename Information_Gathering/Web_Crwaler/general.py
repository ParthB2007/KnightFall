import os
import shutil


# import argparse

#Make New project folder
def create_project_dir(directory):
    print("Creating Directory")
    if not os.path.exists(directory):

        print("initiating Project " + directory)
        os.mkdir(directory)
        print("\nDirectory created Successfully at "  + os.path.abspath(directory))
    else:
        print("Directory already exists at following parth to change the parth use [-p] or [--path]")


#make data file in project folder
def create_data_files(project_name,base_url):

    print("Creating Data files")
    queue = project_name + "/tequeue.txt"
    crawled = project_name + "/recrawled.txt"

    if not os.path.isfile(queue):
        print("\nCreating " + queue)
        write_file(queue,base_url)
        print("queue.txt created Successfully at " + os.path.abspath(queue))

    if not os.path.isfile(crawled):
        print("\nCreating " + crawled)
        write_file(crawled,"")
        print("link.txt created Successfully at " + os.path.abspath(crawled))

#write onto file
def write_file(path,data):
    f = open(path,'w')
    f.write(data)
    f.close()

#append new content
def append_data(path,data):
    with open(path,'a') as file:
        file.write(data + "\n")

#delete content only not the file
def delete_file_contents(path):
    with open(path,'w'):
        pass

def delete_project_dir(directory):
    print("\nDeleting",directory ,"Directory")
    if os.path.exists(directory):
        shutil.rmtree(directory)
        print("Directory deleted successfully at", os.path.abspath(directory))
    else:
        print("No such Directory exist at ", os.path.abspath(directory))

#convert file content into set
def file_to_set(file_name):
    result = set()
    with open(file_name,'rt',encoding='utf=8') as f:
        for line in f:
            result.add(line.replace('\n',''))
    return result

#convert set content into file
def set_to_file(links,file):
    delete_file_contents(file)
    for link in links:
        append_data(file,link)

