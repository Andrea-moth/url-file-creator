import os
import time
import datetime
import requests
from os.path import exists
from http import HTTPStatus
from tkinter import filedialog
from tkinter import *

def check_site(url):
    #checks if a site 1) exists and 2) is up
    #11 - site unreachable
    #12 - site unavailable
    try:
        get = requests.get(url)
        if get.status_code != HTTPStatus.OK: return 11, url

        return True

    except: return 12, url

def find_path():
    #selects a directory to add the url file to
    #21 - path does not exist
    while True:
        print("Please select path")
        root = Tk()
        root.withdraw()
        folder_selected = filedialog.askdirectory()
        
        print(f"\n-- {folder_selected}")
        if not folder_selected: return 21, folder_selected

        return True, folder_selected

def vars():
    #defines the vars
    #url - the site to be added
    #path - path to be added to
    #name - name of the file to be added
    url = str(input("URL\n\n-- "))
    if (check := check_site(url)) != True: return check

    path = find_path()
    if path[0] != True: return path 

    name = str(input("Name\n\n-- "))

    return True, path[1], name, url

def file_creation(info):
    #creates the file and the info to be added to it

    if info[0] != True: return info
            
    file = f"{info[1]}\{info[2]}.url"
    text = f"[InternetShortcut]\nURL={info[3]}"

    with open(f'{file}','w') as file:
        file.write(text)

    return True, info[1], info[2], info[3]

def main():
    #creates the log file
    if not exists("./log.txt"):
        with open("./log.txt","w") as log:
            log.write("[Start]\n\n")
    

    while True:
        #start up and vars
        start = str(input("Do you want to start\n\n-- ")).lower()
        os.system("cls")

        if not start.startswith("y"): return 
        
        result = file_creation(vars())
        record = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')

        #checks for errors and records what's happened 
        if result[0] == True:
            reason = f"[FINISH] {record}: Site-{result[3]} added to {result[1]}/{result[2]}.url\n"
            print("completed")     
        if result[0] == 11:
            reason = f"[ERROR] {record}: Reason - Site ({result[1]}) unreachable\n"
            print("Site unreachable")
        if result[0] == 12:
            reason = f"[ERROR] {record}: Reason - Site ({result[1]}) does not exist\n"
            print("Site does not exist")
        if result[0] == 21:
            reason = f"[ERROR] {record}: Reason - Path ({result[1]}) does not exist\n"   
            print("Path does not exist")

        #writes to the log file
        with open("./log.txt","a") as log:
                log.write(reason)

        time.sleep(3)
        os.system("cls")

if __name__ == "__main__": 
    main()