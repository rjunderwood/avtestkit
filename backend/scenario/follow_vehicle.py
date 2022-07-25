import glob 
import os
import sys
import random
import time
import argparse
import math
import json
from backend.scenario.stats_recorder import StatsRecorder
from backend.util.results.process_results import ProcessResult
#Import ROSClose 
from backend.interface import ros_close as rclose


try:
    sys.path.append(glob.glob('/home/riley/Desktop/CARLA_0.9.11/PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


# import carla
import subprocess
import pathlib

from ..util.util import *


CWD = os.getcwd() 

class ScenarioFollowVehicle:

    scenario_finished = False
    # X = -2.1
    # Y = 120
    X = 340
    Y = 240
    Z = 0.2

    PITCH = 0
    YAW = 270
    #YAW = 270
    ROLL = 0 

    EGO_VEHICLE_NAME = 'ego_vehicle'

    TRIGGER_DIST = 80 
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    #Setup the spectator camera

    SPEC_CAM_X = 340
    SPEC_CAM_Y = 240
    SPEC_CAM_Z = 120
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 


    SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

    # LEAD_VEHICLE_VELOCITY = 3
    LEAD_VEHICLE_VELOCITY = 8

    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 30




    ego_vehicle = None

    #Metamorphic Tests
    metamorphic_test_target_file = open(CWD + "/backend/scenario/metamorphic_tests/follow_vehicle.json")
    metamorphic_tests = json.loads(metamorphic_test_target_file.read())
    metamorphic_test_running = False



    def run(self):
        
        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)
        
            world = client.get_world()


            #Speed
            # settings = world.get_settings()
            # settings.fixed_delta_seconds = 0.05
            # world.apply_settings(settings)




            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))

            world.set_weather(carla.WeatherParameters())

            blueprint_library = world.get_blueprint_library()

            #Blueprint for the lead vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)

            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)


            spawn_loc = carla.Location(self.X,self.Y,self.Z)
            rotation = carla.Rotation(self.PITCH,self.YAW,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)

            lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)

            lead_vehicle.set_light_state(carla.VehicleLightState.All)


            # wait for the ego vehicle to spawn 

            while(find_actor_by_rolename(world,self.EGO_VEHICLE_NAME) == None):
                try:
                    print("Waiting for ego vehicle to spawn... ")
                except KeyboardInterrupt:
                    # lead_vehicle.destroy()
                    pass
            
            ego_vehicle = find_actor_by_rolename(world, self.EGO_VEHICLE_NAME)
            print('Ego vehicle found')
            self.ego_vehicle = ego_vehicle

            #At this point start the metamorphic test running.
            self.metamorphic_test_running = True 
            



            # #Start Recording Scenario before the scenario loop begins
            # self.start_recording_scenario()
            

            while(calc_dist(lead_vehicle, ego_vehicle) > self.TRIGGER_DIST):
                try:
                    #print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(lead_vehicle, ego_vehicle))
                    pass
                except KeyboardInterrupt:
                    #lead_vehicle.destroy()
                    pass
            
            lead_vehicle.set_target_velocity(carla.Vector3D(0,self.LEAD_VEHICLE_VELOCITY,0))
            print("SCENARIO RUNNER :: Set Lead Vehicle" + str(self.LEAD_VEHICLE_VELOCITY))



            self.handle_results_output(world)
  

            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish

            
        finally:
            print("Scenario Finished :: Follow Vehicle") 

            
            #Set the metamorphic test as finished
            self.set_test_finished(world)
 
        
            #Start recording the scenario in a separate process
    def start_recording_scenario(self):
        
        if os.name == 'nt':
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'\record_stats.py'], stdout=sys.stdout)
        else:
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'/record_stats.py'], stdout=sys.stdout)
        

    def is_scenario_finished(self):
        return self.scenario_finished


    #For the assessment toolkit processor to know if it needs to start running the next metamorphic test in queue for this scenario. 
    def is_metamorphic_test_running(self):
        return self.metamorphic_test_running 



    def get_current_metamorphic_test_index(self):
        index =0
        for test in self.metamorphic_tests:
            # print(test)
            if test['done'] == False:
                return index
            index+=1
        return False

        
    def all_metamorphic_tests_complete(self):

        result = True 
        for test in self.metamorphic_tests:
            # print(test)
            if test['done'] == False:
                result = False
        return result

    #When the metamorphic test is finished.
    def set_test_finished(self, world):

        self.process_result()

        #Set metamorphic test as done. 
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['done'] = True
        self.metamorphic_test_running = False

        #Completed all tests, hence scenario complete
        if self.all_metamorphic_tests_complete():
            self.scenario_finished = True 
            # self.ego_vehicle.destroy()
            #Close the Carla Autoware docker that is setup.
            rclose.ROSClose()

        # self.ego_vehicle.destroy()
        rclose.ROSClose()
        # #Destroy the ego vehicle to get ready for the next scenario / metamorphic test change.
        # self.ego_vehicle.destroy()
        # #Close the Carla Autoware docker that is setup.
        # rclose.ROSClose()
        destroy_all_vehicle_actors(world)
         
          
    def process_result(self):
        
        
        #Process the data
        process_result = ProcessResult('T0.txt')

        #Pass?
        #any collisions/lane invasions 
        result_pass = False
        if (not process_result.had_collision()) and (not process_result.had_lane_invasion()):
            result_pass = True
        

        #TODO Write Result to the JSON line. 

    def handle_results_output(self, world):
  
        #This is where the Real scenario begins. Time to start recording stats. 
        results_file_name = 'follow_vehicle_' + str(self.get_current_metamorphic_test_index())    
        results_file_path = CWD + "/backend/scenario/results/"+results_file_name+".txt"
        stats_recorder = StatsRecorder(world, self.RUNNING_TIME)
        stats_recorder.record_stats('ego_vehicle', 'stationary_vehicle', results_file_path)
