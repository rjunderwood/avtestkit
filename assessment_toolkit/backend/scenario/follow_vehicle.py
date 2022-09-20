import glob 
import os
import sys
import random
import time
import argparse
import math
import json
from backend.util.stats_recorder import StatsRecorder
from backend.util.results.process_results import ProcessResult
#Import ROSClose 
from backend.interface import ros_close as rclose
from backend.util.weather import get_weather_parameters
CWD = os.getcwd() 

CONFIG = json.load(open(CWD+'/config.json'));

try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
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



class ScenarioFollowVehicle:

    world = None 
    scenario_finished = False
    # X = -2.1
    # Y = 120
    X = 339
    Y = 240
    Z = 0.2

    PITCH = 0
    YAW = 270
    ROLL = 0 

    EGO_VEHICLE_NAME = 'ego_vehicle'

    TRIGGER_DIST = 30
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
    LEAD_VEHICLE_VELOCITY = 5

    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 15




    ego_vehicle = None

    #Metamorphic Tests
    METAMORPHIC_TEST_FILE_LOCATION= CWD + "/backend/scenario/metamorphic_tests/follow_vehicle.json"
    metamorphic_test_target_file = open(METAMORPHIC_TEST_FILE_LOCATION)
    metamorphic_tests = json.loads(metamorphic_test_target_file.read())
    metamorphic_test_running = False



    def run(self):
        
        try:
            # if self.world == None:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)
            world = client.get_world()
            self.world = world
     
            spectator = self.world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))
            blueprint_library = self.world.get_blueprint_library()


            #Metamophic Parameters Specific for this test
            metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            


            #Lead Vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == metamorphic_parameters['lead_vehicle_model'])
            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            spawn_loc = carla.Location(self.X,self.Y,self.Z)
            rotation = carla.Rotation(self.PITCH,self.YAW,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            lead_vehicle = self.world.spawn_actor(lead_vehicle_bp, transform)
            lead_vehicle.set_light_state(carla.VehicleLightState.All)



            self.LEAD_VEHICLE_VELOCITY = metamorphic_parameters['lead_vehicle_velocity']

            self.world.set_weather(get_weather_parameters(metamorphic_parameters['weather']))



            # wait for the ego vehicle to spawn 
            while(find_actor_by_rolename(self.world,self.EGO_VEHICLE_NAME) == None):
                try:
                    print("Waiting for ego vehicle to spawn... ")
                except KeyboardInterrupt:
                    # lead_vehicle.destroy()
                    pass
            
            ego_vehicle = find_actor_by_rolename(self.world, self.EGO_VEHICLE_NAME)
            print('Ego vehicle found')
            self.ego_vehicle = ego_vehicle
            self.ego_vehicle.set_target_velocity(carla.Vector3D(0,-metamorphic_parameters['ego_vehicle_velocity'],0))
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
            
            lead_vehicle.set_target_velocity(carla.Vector3D(0,-self.LEAD_VEHICLE_VELOCITY,0))



            #Set the other vehicles on the other direction 
            number_of_other_vehicles = metamorphic_parameters['passing_vehicles']
            vehicle_types = metamorphic_parameters['car_types']
            #Other vehicles moving the opposite direction 
            npm_y_value = 150
            for vehicle in range(number_of_other_vehicles):
                npc_vehicle_blueprint = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            for vehicle in range(0,number_of_other_vehicles):
                for bp in blueprint_library:
                    if bp.id == vehicle_types[vehicle]:
                        npc_vehicle_blueprint = bp
                        break
                spawn_loc = carla.Location(335, npm_y_value,self.Z)
                rotation = carla.Rotation(self.PITCH,90,self.ROLL)
                transform = carla.Transform(spawn_loc, rotation)
                npm_y_value-=20; 
                npc_vehicle = self.world.spawn_actor(npc_vehicle_blueprint, transform)
                npc_vehicle.set_target_velocity(carla.Vector3D(0,7,0))


            current_velocity = self.LEAD_VEHICLE_VELOCITY 
            #Speed up the vehicle at y 200 
            lead_vehicle_target_stop_y = 220
            while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
                print(lead_vehicle.get_location().y)
            while current_velocity < 6:
                current_velocity+=0.01
                lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))



            #Slow down the vehicle at y 150
            lead_vehicle_target_stop_y = 200
            while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
                pass
         
            while current_velocity > 4:
                current_velocity-=0.01
                lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))

            
            #Slow down to stop the vehicle at y 100
            lead_vehicle_target_stop_y = 180
            while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
                pass
         
            while current_velocity > 0:
                current_velocity-=0.01
                lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))

            
            #Speed up 
            #Slow Down To stol
            lead_vehicle.set_target_velocity(carla.Vector3D(0,0,0))



            self.handle_results_output(self.world)
  
            #Set the metamorphic test as finished
            self.set_test_finished(self.world)
 
            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish

            
        finally:
            print("Scenario Finished :: Follow Vehicle") 

            
            
        
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



        #Set metamorphic test as done. 
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['done'] = True
        self.metamorphic_test_running = False
        #Save metamorphic test json in file directory
        with open(self.METAMORPHIC_TEST_FILE_LOCATION, 'w') as outfile:
            outfile.write(json.dumps(self.metamorphic_tests, indent=4, sort_keys=True))


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
        self.clear_world_state()
    
    def clear_world_state(self):
        #Clear the world actors
        print("clear_world_state(self)")
        for actor in self.world.get_actors().filter('vehicle.*'):
            # if actor is a vehicle
            actor.destroy()
            print("destroyed actor")

          


    def handle_results_output(self, world):
  
        #This is where the Real scenario begins. Time to start recording stats. 
        results_file_name = 'follow_vehicle_' + str(self.get_current_metamorphic_test_index())    
        results_file_path = CWD + "/backend/scenario/results/"+results_file_name+".txt"
        stats_recorder = StatsRecorder(world, self.RUNNING_TIME)
        stats_recorder.record_stats('ego_vehicle', 'stationary_vehicle', results_file_path)

        #Set number of collision and lane invastions to metamorphic test to save as json
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['number_of_collisions'] = stats_recorder.get_number_of_collisions()
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['number_of_lane_invasions'] = stats_recorder.get_number_of_lane_invasions()
