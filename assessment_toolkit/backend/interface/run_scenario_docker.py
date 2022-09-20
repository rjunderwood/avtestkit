import os
import sys


class RunScenarioDocker():

    script_path=""
    
    def __init__(self):
        print("RunScenarioDocker() :: __init__")
        directory = os.getcwd() 
        directory = directory.replace("/backend/interface","")
        script_path = directory +"/ros_patch/run_scenario_docker.sh"
        print(script_path)
        self.script_path = script_path 
    
    
    def run(self):
        print("RunScenarioDocker() :: run")
        os.system("gnome-terminal -e 'bash -c \"" + self.script_path +" -s; exec bash\"'")

