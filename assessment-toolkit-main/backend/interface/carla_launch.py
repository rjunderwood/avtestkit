import subprocess as sp

class CarlaLaunch:
    
    __carla__


    def __init__(self):
        __carla__ = sp.check_call("~/CARLA_AUTOWARE/CarlaUE4.sh", shell=True)
