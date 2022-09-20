import glob 
import os
import sys
import random
import time
import argparse
import math 
import json
from backend.util.stats_recorder import StatsRecorder
from backend.interface.run_scenario_docker import RunScenarioDocker 
from backend.util.results.process_results import ProcessResult
#Import ROSClose 
from backend.interface import ros_close as rclose
from backend.util.weather import get_weather_parameters

# RUN_SCENARIO_DOCKER= RunScenarioDocker() 
# RUN_SCENARIO_DOCKER.run()

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

CWD = os.getcwd() 

class ScenarioPedestrianCrossingPriorVehicleManouver:
    #Ego Vehicle Functions
    from backend.util.util import await_ego_spawn,await_scenario_trigger
    #Extra Vehicle Spawning Functions
    from backend.util.extra_scenario_vehicles import handle_spawn_extra_scenario_vehicles, spawn_vehicle_carla, start_extra_vehicle_velocities
    #Spectator camera
    from backend.util.spectator_camera import setup_spectator_camera
    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 30
    scenario_finished = False
    world=None
    blueprint_library=None
    X = 330
    Y = 240
    Z = 0.2
    PITCH = 0
    YAW = 0
    ROLL = 0 
    EGO_VEHICLE_NAME = 'ego_vehicle'
    TRIGGER_DIST = 38
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    #Setup the spectator camera
    SPEC_CAM_X = -10
    SPEC_CAM_Y = 117
    SPEC_CAM_Z = 52
    SPEC_CAM_PITCH = -70
    SPEC_CAM_YAW = 90
    SPEC_CAM_ROLL = 0 

    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 10

    ego_vehicle = None

    #Metamorphic Tests
    metamorphic_test_target_file = open(CWD + "/backend/scenario/metamorphic_tests/pedestrian_crossing_prior_vehicle_manouver.json")
    metamorphic_tests = json.loads(metamorphic_test_target_file.read())
    metamorphic_test_running = False
    metamorphic_parameters = None
    spawned_scenario_vehicles=[]


    #Scenario Specific 
    pedestrian_controllers=[] 
    scenario_trigger_actor=None #The carla actor that is used as trigger when distance from the ego 


    first_run=True 

    #Connects to the carla world and setups necessary components
    def scenario_setup(self):

        if self.world == None:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)
            world = client.load_world('Town03')
            self.world = world 


        # self.destroy_all_vehicle_actors(world)
        blueprint_library = self.world.get_blueprint_library()
        self.blueprint_library = blueprint_library
        #Setup the Specator Camera
        self.setup_spectator_camera(self.SPEC_CAM_X, self.SPEC_CAM_Y, self.SPEC_CAM_Z, self.SPEC_CAM_PITCH, self.SPEC_CAM_YAW, self.SPEC_CAM_ROLL)
        #Setup Weather 
        self.world.set_weather(get_weather_parameters(self.metamorphic_parameters['weather']))




    def run_continuous(self):
        try:
              #Set current metamorphic parameters
            self.metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            #Setup the basics of the scenario 
            self.scenario_setup() 
                    #Spawn pedestrians
            self.spawn_pedestrians()
            #Spawn extra vehicles 
            self.handle_spawn_extra_scenario_vehicles()

            #At this point start the metamorphic test running.
            self.metamorphic_test_running = True 
            self.await_ego_spawn()
                        #SCENARIO Logic
            #Pedestrian controllers
            for pedestrian_controller in self.pedestrian_controllers:
                pedestrian_controller.start()
                pedestrian_controller.go_to_location(carla.Location(13,139,0.2))
            
            #Start velocities of extra vehicles
            self.start_extra_vehicle_velocities()
           
           

           ###Loop to run for 5 seconds 
            start_t = self.current_time()
            end_time = start_t + 5
          
            while(self.current_time() < end_time):
                pass

        except Exception as e:
            print("RUNNING SCENARIO EXCEPTION")
            print(e)




        finally:
            print("Scenario Finished :: Pedestrian Crossing Crossing Prior Vehicle Manouver") 
            #Set the metamorphic test as finished
            self.set_test_finished_automation(self.world)

    def current_time(self): 
        return time.time()


    def run(self):
        try:
            #Set current metamorphic parameters
            self.metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            #Setup the basics of the scenario 
            self.scenario_setup() 
            #Spawn pedestrians
            self.spawn_pedestrians()
            #Spawn extra vehicles 
            self.handle_spawn_extra_scenario_vehicles()
            #Wait for ego to spawn 
            self.await_ego_spawn()
            #Set Target velocity of ego 
            
            #At this point start the metamorphic test running.
            self.metamorphic_test_running = True 
            # Await scenario trigger after this line the function 
            self.await_scenario_trigger()


            #SCENARIO Logic
            #Pedestrian controllers
            for pedestrian_controller in self.pedestrian_controllers:
                pedestrian_controller.start()
                pedestrian_controller.go_to_location(carla.Location(13,139,0.2))
            
            #Start velocities of extra vehicles
            self.start_extra_vehicle_velocities()


            self.handle_results_output()
        
        except Exception as e:
            print("RUNNING SCENARIO EXCEPTION")
            print(e)
        
        finally: 


            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish
        
            
            print("Scenario Finished :: Pedestrian Crossing") 
            #Set the metamorphic test as finished
            self.set_test_finished_automation(self.world)

        
            #Start recording the scenario in a separate process
    

        #Handles the spawning of pedestrians
    def spawn_pedestrians(self):
        childBlueprintWalkers = self.blueprint_library.filter('walker.pedestrian.0013')[0]
        adultBlueprintWalkers = self.blueprint_library.filter('walker.pedestrian.0021')[0]
        walker_controller_bp = self.world.get_blueprint_library().find('controller.ai.walker')

        #Pedestrians. 
        pedestrian_actors = []
       
        
        pedestrian_x = -10
        #Spawn Children 
        for i in range(0, self.metamorphic_parameters['pedestrian_adult']):
            spawn_loc = carla.Location(pedestrian_x,142,0.4)
            pedestrian_x+=0.5
            rotation = carla.Rotation(7,1,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            pedestrian_actor=self.world.spawn_actor(adultBlueprintWalkers, transform)
            pedestrian_actors.append(pedestrian_actor)
            self.pedestrian_controllers.append(self.world.spawn_actor(walker_controller_bp,transform, pedestrian_actor))
        #Spawn Adults
        for i in range(0, self.metamorphic_parameters['pedestrian_child']):
            spawn_loc = carla.Location(pedestrian_x,142,0.4)
            pedestrian_x+=0.5
            rotation = carla.Rotation(7,1,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            pedestrian_actor=self.world.spawn_actor(childBlueprintWalkers, transform)
            pedestrian_actors.append(pedestrian_actor)
            self.pedestrian_controllers.append(self.world.spawn_actor(walker_controller_bp,transform, pedestrian_actor))

        #One of the pedestrian actor is the trigger
        try:

            if(self.scenario_trigger_actor == None):
                self.scenario_trigger_actor=pedestrian_actors[0]
        except: 
            #No pedestrian. Spawn a single pedestrian that does not move on road. 
            pedestrian_x = -10
            #Spawn Children 
            spawn_loc = carla.Location(pedestrian_x,142,0.4)
            pedestrian_x+=0.5
            rotation = carla.Rotation(7,1,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            pedestrian_actor=self.world.spawn_actor(adultBlueprintWalkers, transform)
            self.scenario_trigger_actor = pedestrian_actor 

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


    #Auto restart the test. 
    def set_test_finished_automation(self, world):
        #Set metamorphic test as done. 
        # self.metamorphic_tests[self.get_current_metamorphic_test_index()]['done'] = True
        # self.metamorphic_test_running = False
        try:
            actors = self.world.get_actors()
            walker_actors = actors.filter('walker.*') 
            vehicle_actors = actors.filter('vehicle.*') #filter out only vehicle actors
            
            if(actors):
                for walker in walker_actors:
                    walker.destroy()
                for vehicle in vehicle_actors:
                    if(vehicle.attributes['role_name'] != self.EGO_VEHICLE_NAME):
                        vehicle.destroy()
              
            else:
                print('There are currently  actors in the Carla world. ')    
            #
            self.pedestrian_controllers = []
            
            #self.run()
            self.run_continuous()
        except:
            pass

    #When the metamorphic test is finished.
    def set_test_finished(self, world):
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
        # destroy_all_vehicle_actors(world)
          

    def handle_results_output(self):
        #This is where the Real scenario begins. Time to start recording stats. 
        results_file_name = 'pedestrian_crossing_prior_vehicle_manouver_' + str(self.get_current_metamorphic_test_index())    
        results_file_path = CWD + "/backend/scenario/results/"+results_file_name+".txt"
        stats_recorder = StatsRecorder(self.world, self.RUNNING_TIME)
        stats_recorder.record_stats('ego_vehicle', 'stationary_vehicle', results_file_path)
