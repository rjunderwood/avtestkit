import os

class CarlaLaunch:
    
    __carla__ = None

    def __init__(self, CARLA_SIMULATOR_PATH):
        print(CARLA_SIMULATOR_PATH)
        #self.__carla__ = os.system("gnome-terminal -e 'bash -c \"" + CARLA_SIMULATOR_PATH +"CarlaUE4.sh -quality-level=Low -s; exec bash\"'")
        self.__carla__ = os.system("gnome-terminal --working-directory="+CARLA_SIMULATOR_PATH+" -e 'bash -c \"echo \'░█████╗░░█████╗░██████╗░██╗░░░░░░█████╗░\';echo \'██╔══██╗██╔══██╗██╔══██╗██║░░░░░██╔══██╗\';echo \'██║░░╚═╝███████║██████╔╝██║░░░░░███████║\';echo \'██║░░██╗██╔══██║██╔══██╗██║░░░░░██╔══██║\';echo \'╚█████╔╝██║░░██║██║░░██║███████╗██║░░██║\';echo \'░╚════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝\'; echo ;echo ;echo ===INSTRUCTIONS===;echo ; echo =START CARLA=;echo ./CarlaUE4.sh; echo ;echo =STOP CARLA=; echo CONTROL+C; echo ; echo =RESTART CARLA=; echo CONTROL+C;echo ./CarlaUE4.sh; echo ; exec bash\"'")
#echo ;echo ; echo ; echo ===INSTRUCTIONS===; echo ; echo (TO START); echo ./CarlaUE4.sh; echo ; echo =TO STOP=; echo CONTROL+C; echo ; echo =TO RESTART=; echo CONTROL+C;echo ./CarlaUE4.sh;
    def get_carla_launch(self):
        return self.__carla__