import subprocess as sp

class ROSLaunch:
    
    __ros__ = None

    def __init__(self):
        self.__ros__ = sp.check_call("sudo ~/ROS_DATA/carla-autoware/run.sh -s", shell=True)

    def get_ros_launch(self):
        return self.__ros__