import os
import subprocess
from playsound import playsound
class ROSClose:
    
    __rosclose__ = None

    def __init__(self):
        directory = os.getcwd() + "/backend/interface/close_carla_autoware_docker.sh"
        self.__rosclose__ = subprocess.call(directory)
        #Notify the test has finished running. 
        playsound(os.getcwd() + "/backend/interface/test_finished.wav")



    

            