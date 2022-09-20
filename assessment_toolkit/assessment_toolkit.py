#from subprocess import call
import os
import threading
import json
import time
import sys
import multiprocessing
from unittest import case

#Import CarlaLaunch
from backend.interface import carla_launch as claunch
#Import ROSLaunch
from backend.interface import ros_launch as rlaunch
#Import ROSClose 
from backend.interface import ros_close as rclose
#Import ROSPatch
from backend.interface import patch_ros as patchros
## Backend
#Import the scenario maker
from backend.scenario.scenario_manager import ScenarioManager
#Import the process data
from backend.util.results.process_results import ProcessResult

## Frontend
#Import the front end
from frontend.front_end_main import FrontEndMain
CONFIG = json.load(open('config.json'))



class AssessmentToolkit:

    current_scenario = None
    gui = None

    #Scenarios that are going to be runned during this session. 
    scenario_queue = []
    setup_controller = {"carla":False, "carla_autoware":False}

    def __init__(self):
        #Start GUI
        gui = FrontEndMain(self)
        #Save GUI
        self.gui = gui
        #start the gui
        self.gui.start()
  

   
    def start_carla(self):
        # Launch CARLA & Sleep for 5 seconds.
        claunch.CarlaLaunch(CONFIG['CARLA_SIMULATOR_PATH'])
        time.sleep(1)
        self.setup_controller["carla"] = True

    def start_carla_autoware(self):
        # Launch CARLA AUTOWARE/ROS & Sleep for 5 seconds.
        rlaunch.ROSLaunch(CONFIG['CARLA_AUTOWARE_PATH'])
        time.sleep(2)
        self.setup_controller["carla_autoware"] = True 

    
    #Setup controller GET from the gui on the view_setup_toolkit 
    def get_setup_controller(self):
        return self.setup_controller
    


    #Setup multiple Scenarios
    def setup_scenarios(self, data):

        print("\n\nsetup_scenarios\n")
        for key in data:
                print(key, ' : ',data[key])

        try:
            if data['scenario_check_follow_vehicle'] == True:
                self.scenario_queue.append(ScenarioManager("follow_vehicle", data))
            if data['scenario_check_follow_vehicle0'] == True:
                self.scenario_queue.append(ScenarioManager("follow_vehicle", data))    
            try:

                if data['scenario_check_pedestrian_crossing'] == True:
                    self.scenario_queue.append(ScenarioManager("pedestrian_crossing", data))
            except: 
                pass
            try:
                if data['scenario_check_pedestrian_crossing0'] == True:
                    self.scenario_queue.append(ScenarioManager("pedestrian_crossing", data))    
            except: 
                pass

            try:

                if data['scenario_check_pedestrian_crossing_prior_vehicle_manouver'] == True:
                    self.scenario_queue.append(ScenarioManager("pedestrian_crossing_prior_vehicle_manouver", data))
            except: 
                pass
            try:
                if data['scenario_check_pedestrian_crossing_prior_vehicle_manouver0'] == True:
                    self.scenario_queue.append(ScenarioManager("pedestrian_crossing_prior_vehicle_manouver", data))    
            except: 
                pass


            try:

                if data['scenario_check_follow_vehicle_town3'] == True:
                    
                    self.scenario_queue.append(ScenarioManager("follow_vehicle_town3", data))
            except: 
                pass

            try:
                if data['scenario_check_follow_vehicle_town30'] == True:
                    self.scenario_queue.append(ScenarioManager("follow_vehicle_town3", data))    
            except: 
                pass

            try:
                if data['scenario_check_red_light'] == True:
                    self.scenario_queue.append(ScenarioManager("red_light", data))
                if data['scenario_check_red_light0'] == True:
                    self.scenario_queue.append(ScenarioManager("red_light", data))
            except:
                pass
            try:
                if data['scenario_check_intersection_left_turn'] == True:
                    self.scenario_queue.append(ScenarioManager("intersection_left_turn", data))
                if data['scenario_check_intersection_left_turn0'] == True:
                    self.scenario_queue.append(ScenarioManager("intersection_left_turn", data))
            except:
                pass
            # if data['scenario_check_pedestrian_crossing_road'] == True:
            #     self.scenario_queue.append()


            #If there are no selected Scenarios
            if(len(self.scenario_queue) == 0):
                print("NO SCENARIO QUEUE SET ::: ")
                self.gui.change_view("view_setup_scenarios_none")
                return 0


            #Setup the current scenario
            self.current_scenario = self.scenario_queue[0]
            self.gui.change_view("view_scenario_starter_"+self.current_scenario.get_scenario_name())

        finally:
            print("Scenarios Ready") 

            # self.gui.change_view("view_set_2d_pose_estimation")

    #This runs the scenario along with the recording of the scenario data
    #CALLED after the 2D pose estimation is set in RVIS and the user clicks done on that page
    def run_scenario(self):
        #Run
        print("Running Scenario ::" + self.current_scenario.get_scenario_name())
    
        #change view to running scenario text

        


        #Run
        self.current_scenario.run()
        

        # #Wait for the scenario metamorphic test to finish running. 
        while(self.current_scenario.is_metamorphic_test_running()):
            pass
        
        
        #Is scenario finished | all the metamorphic tests have been completed 
        if self.current_scenario.is_scenario_finished():

            #Is there more scenarios left in queue? 
            if len(self.scenario_queue) > 1:
                #Go to next scenario 
                self.scenario_queue.pop(0)
                self.current_scenario = self.scenario_queue[0]
          
                #Set view_loading_next_scenario 
                self.gui.change_view('view_loading_next_scenario')

                #Go to the view_scenario_starter (next scenario)
                self.gui.change_view("view_scenario_starter_"+ self.get_current_scenario_name())
                
                
                
            else:
                #All Scenarios are completed running.
                print("All scenarios are complete.")
                self.gui.change_view("view_all_scenario_complete")

        else:
            #Go to next metamorphic test for current scenario 
            
            self.gui.change_view("view_next_metamorphic")
            







    



    
    def get_current_scenario_name(self):
        
        try: 
            print("get_current_scenario_name :: " + self.current_scenario.get_scenario_name())
            return self.current_scenario.get_scenario_name()
        except: 
            print("get_current_scenario_name :: ")
            return ""

    
    #Run the ros patch
    #Only is going to be successful if the docker is run. 
    def run_ros_patch(self):
        print("run_ros_patch :: "+ self.get_current_scenario_name())
        patchros.PatchRos(self.get_current_scenario_name())        

    
    



    

if __name__ == '__main__':
    
    assessment_toolkit = AssessmentToolkit()
    assessment_toolkit.main()
   


    


