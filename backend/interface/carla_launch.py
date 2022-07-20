import os

class CarlaLaunch:
    
    __carla__ = None

    def __init__(self, CARLA_SIMULATOR_PATH):
        self.__carla__ = os.system("gnome-terminal -e 'bash -c \"" + CARLA_SIMULATOR_PATH +"CarlaUE4.sh -s; exec bash\"'")

    def get_carla_launch(self):
        return self.__carla__