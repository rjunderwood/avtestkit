import os

class ROSLaunch:
    
    __ros__ = None

    def __init__(self):
        self.__ros__ = os.system("gnome-terminal -e 'bash -c \"sudo ~/ROS_DATA/carla-autoware/run.sh -s; exec bash\"'")
        

    def get_ros_launch(self):
        return self.__ros__