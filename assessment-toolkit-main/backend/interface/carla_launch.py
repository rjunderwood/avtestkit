import os

class CarlaLaunch:
    
    __carla__ = None

    def __init__(self):
        self.__carla__ = os.system("gnome-terminal -e 'bash -c \"~/CARLA_AUTOWARE/CarlaUE4.sh &; exec bash\"'")

    def get_carla_launch(self):
        return self.__carla__