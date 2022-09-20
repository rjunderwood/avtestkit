import os
import subprocess
from playsound import playsound
class ROSClose:
    
    __rosclose__ = None

    def __init__(self):
        directory = os.getcwd() + "/backend/interface/close_carla_autoware_docker.sh"
        print("DIRECTORY" + directory)
        #self.__ros__ = os.system("gnome-terminal -e 'bash -c \"sudo " + CARLA_AUTOWARE_PATH + "run.sh -s; exec bash\"'")
        #self.__ros__ = os.system("gnome-terminal -- sudo " + CARLA_AUTOWARE_PATH + "run.sh")
        self.__rosclose__ = subprocess.call(directory)
        
        #Notify the test has finished running. 
        playsound(os.getcwd() + "/backend/interface/test_finished.wav")



    

            