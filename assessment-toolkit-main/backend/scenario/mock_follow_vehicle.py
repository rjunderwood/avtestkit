import glob 
import os
import sys
import random
import time
import argparse
import math
import subprocess
import pathlib
#TODO when not in development change from .mock_follow_vehicle => .follow_vehicle
from ..util.mock_util import *

class ScenarioFollowVehicle:

    scenario_finished = False
    
    def run(self):
        
        try:
            #self.start_recording_scenario()
            
            time.sleep(5)
        finally:
            print("Scenario Finished :: Follow Vehicle") 
            #Set the scenario as finished
            self.scenario_finished = True



    #Start recording the scenario in a separate process
    def start_recording_scenario(self):
        if os.name == 'nt':
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'\record_stats.py'], stdout=sys.stdout)
        else:
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'/record_stats.py'], stdout=sys.stdout)


    def is_scenario_finished(self):
        return self.scenario_finished