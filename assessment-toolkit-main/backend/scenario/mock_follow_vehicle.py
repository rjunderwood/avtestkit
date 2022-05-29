import glob 
import os
import sys
import random
import time
import argparse
import math
#TODO when not in development change from .mock_follow_vehicle => .follow_vehicle
from ..util.mock_util import *

class ScenarioFollowVehicle:

    scenario_finished = False

    def run(self):
        
        try:
            #Run for 3 seconds
            time.sleep(3)

        finally:
            print("Scenario Finished :: Follow Vehicle") 

            #Set the scenario as finished
            self.scenario_finished = True
        

    def is_scenario_finished(self):
        return self.scenario_finished