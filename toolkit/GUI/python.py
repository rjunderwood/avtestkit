
import os
import sched, time
s = sched.scheduler(time.time, time.sleep)

def start():

    #Def
    os.system("start ./html/home.html")
    os.system("man./html/results.html")


def await_the_testing_settings(sc):

    try:
        #Open the toolkit_settings.json
        print("open")

    except:
        sc.enter(60, 1, await_the_testing_settings, (sc,))

    
start()