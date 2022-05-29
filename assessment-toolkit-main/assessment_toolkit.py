#from subprocess import call
import os
import threading
import json
import time
import sys
import multiprocessing

## Backend
#Import the scenario maker
from backend.scenario.scenario import Scenario

## Frontend
#Import the front end
from frontend.front_end_main import FrontEndMain

class AssessmentToolkit:

    current_scenario = None
    gui = None


    def __init__(self):
        #Start GUI
        gui = FrontEndMain(self)
        #Save GUI
        self.gui = gui
        #start the gui
        self.gui.start()
              

    #Setup Scenario is called after the setup on the first GUI page has been entered and the 'start' button pressed
    #Creates a specified scenario 
    def setup_scenario(self, data):

        print("\n\nSetting Up Scenario....")
        for key in data:
                print(key, ' : ',data[key])
        
        try:
            #Setup the scenario
            if(data["scenario"] == 'Follow Vehicle'):
                print("Creating Scenario :: Follow Vehicle")
                #Create
                self.current_scenario = Scenario("follow_vehicle", data)

        finally:
            print("Scenario Ready") 
            self.gui.change_view("view_set_2d_pose_estimation")
    


    #This runs the scenario along with the recording of the scenario data
    #CALLED after the 2D pose estimation is set in RVIS and the user clicks done on that page
    def run_scenario(self):
        #Run
        print("Running Scenario ::" + self.current_scenario.get_scenario_name())
        #During Running scenario the user needs to set the 2d nav goal.
        #change view to that
        
        #Run
        self.current_scenario.run()
    

        # #Wait for the scenario to finish running. 
        while(not self.current_scenario.is_scenario_finished()):
            pass
        
        # #Change the gui view to results
        self.gui.change_view("view_result")

        #TODO some sort of data input to the view_result GUI with the processed data
    


            
            

            


    

if __name__ == '__main__':
    
    assessment_toolkit = AssessmentToolkit()
    assessment_toolkit.main()
   


    


