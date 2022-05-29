
import os
import threading
import json

def start():

    #Def
    #Opens windows
    
    os.system("start ./html/home.html")
    #Opens mac/linux
    os.system("open ./html/home.html")


    await_the_testing_settings()


def await_the_testing_settings():
   
    settings_not_found = True 
    while settings_not_found:
        print("settings_not_found")
     
        try:
            # Opening JSON file
            f = open('./json-outputs/output.json')
            data = json.load(f)
            print(data)
            settings_not_found = False
  
        except: 
           
            pass
  
    
start()