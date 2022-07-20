import os
import subprocess

class ROSLaunch:
    
    __ros__ = None

    def __init__(self, CARLA_AUTOWARE_PATH):
        self.__ros__ = os.system("gnome-terminal -e 'bash -c \"sudo " + CARLA_AUTOWARE_PATH + "/run.sh -s; exec bash\"'")
  
    def get_ros_launch(self):
        return self.__ros__

    

            