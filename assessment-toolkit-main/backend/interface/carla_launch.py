import subprocess as sp

class CarlaLaunch:

    def __init__(self):
        sp.check_call("~/CARLA_AUTOWARE/CarlaUE4.sh", shell=True)
