import subprocess as sp

class CarlaLaunch:
    
    __carla__ = None

    def __init__(self):
        self.__carla__ = sp.check_call("~/CARLA_AUTOWARE/CarlaUE4.sh &", shell=True)

    def get_carla_launch(self):
        return self.__carla__