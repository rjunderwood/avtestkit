import glob 
import os
import sys
import random
import json
CONFIG = json.load(open('../config.json'));
try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass
import carla
#Weather functions
from weather import get_weather_parameters

class ScenarioFollowVehiclePriorVehicleManouver:
    #Extra Vehicle Spawning Functions
    from extra_scenario_vehicles import handle_spawn_extra_scenario_vehicles, spawn_vehicle_carla, start_extra_vehicle_velocities
    #Spectator camera
    from spectator_camera import setup_spectator_camera
    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 60
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
    TRIGGER_DIST = 40
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    #SPECTATOR CAMERA
    SPEC_CAM_X = 2
    SPEC_CAM_Y = 133
    SPEC_CAM_Z = 80
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 

    #EGO POSITION 
    EGO_VEHICLE_X= -60
    EGO_VEHICLE_Y = 135
    EGO_VEHICLE_Z = 0.2
    SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

    # LEAD_VEHICLE_VELOCITY = 3
    LEAD_VEHICLE_VELOCITY = 6


    #NAVGOAL -42.3, 129, 1, 0, 180. 0 
    
    #Metamophic Parameters Specific for this test
    metamorphic_parameters = {
        "weather": "Cloudy Noon",
        "pedestrian_number":5,
        "pedestrian_type":"adult",
        "pedestrian_adult":2,
        "pedestrian_child":2,
        "spawn_vehicle_location_1": [
            {
                "model":"sedan",
                "location":{
                    "X":2,
                    "Y":180, 
                    "Z":0.2, 
                    "PITCH":0,
                    "YAW":-90, 
                    "ROLL":0,
                   "velocity":{
                        "X":0,
                        "Y":-4,
                        "Z":0
                    }
                }
            },
            {
                "model":"motorbike",
                "location":{
                    "X":2,
                    "Y":150, 
                    "Z":0.2, 
                    "PITCH":0,
                    "YAW":-90, 
                    "ROLL":0,
                   "velocity":{
                        "X":0,
                        "Y":-6,
                        "Z":0
                    }
                }
            }
        ],
        
        "spawn_vehicle_location_2": [
            {
                "model":"sedan",
                "location":{
                    "X":-6,
                    "Y":110, 
                    "Z":0.2, 
                    "PITCH":0,
                    "YAW":90, 
                    "ROLL":0,
                    "velocity":{
                        "X":0,
                        "Y":4,
                        "Z":0
                    }
                }
            },
              {
                "model":"motorbike",
                "location":{
                    "X":-6,
                    "Y":102, 
                    "Z":0.2, 
                    "PITCH":0,
                    "YAW":90, 
                    "ROLL":0,
                    "velocity":{
                        "X":0,
                        "Y":6,
                        "Z":0
                    }
                }
            }
        ],
    } 

    #Extra scenario vehicles 
    spawned_scenario_vehicles = []
    
    ###Spawned Vehicle Traffic Controller. 
    #Holds the spawned vehicles and sets their 
   
    #Specific Scenario Parameters 
    pedestrian_controllers = []
        
    

    #Connects to the carla world and setups necessary components
    def scenario_setup(self):
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.load_world('Town03')
        self.world = world 
        self.destroy_all_vehicle_actors(world)
        blueprint_library = world.get_blueprint_library()
        self.blueprint_library = blueprint_library
        #Setup the Specator Camera
        self.setup_spectator_camera(self.SPEC_CAM_X, self.SPEC_CAM_Y, self.SPEC_CAM_Z, self.SPEC_CAM_PITCH, self.SPEC_CAM_YAW, self.SPEC_CAM_ROLL)
        #Setup Weather 
        world.set_weather(get_weather_parameters(self.metamorphic_parameters['weather']))





    #Run the scenario: Actors, Recording, Finishing
    def run(self):
        try:
            #Setup the basics of the scenario 
            self.scenario_setup() 


            #Scenario Specific Logic 
            spawn_loc = carla.Location(-13,142,0.4)
            rotation = carla.Rotation(7,1,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            # lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)
            # lead_vehicle.set_light_state(carla.VehicleLightState.All)

            #Spawn pedestrians
            self.spawn_pedestrians()

            #Spawn extra vehicles 
            self.handle_spawn_extra_scenario_vehicles()
            #Start velocities of extra vehicles
            self.start_extra_vehicle_velocities()
            return 0

            #EGO Vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            ego_spawn_loc = carla.Location(self.EGO_VEHICLE_X,self.EGO_VEHICLE_Y, self.EGO_VEHICLE_Z)
            ego_rotation = carla.Rotation(0,0,0)
            ego_transform = carla.Transform(ego_spawn_loc, ego_rotation)
            ego_vehicle = world.spawn_actor(lead_vehicle_bp, ego_transform)
            ego_vehicle.set_target_velocity(carla.Vector3D(6.8,0,0))
        
        
        
        
            # wait for the ego vehicle to spawn 
            # while(find_actor_by_rolename(world,self.EGO_VEHICLE_NAME) == None):
            #     try:
            #         print("Waiting for ego vehicle to spawn... ")
            #     except KeyboardInterrupt:
            #         # lead_vehicle.destroy()
            #         pass
            
            # ego_vehicle = find_actor_by_rolename(world, self.EGO_VEHICLE_NAME)
          
            # self.ego_vehicle = ego_vehicle

            #At this point start the metamorphic test running.
            self.metamorphic_test_running = True 
            



            # #Start Recording Scenario before the scenario loop begins
            # self.start_recording_scenario()
            

            # while(calc_dist(pedestrian, ego_vehicle) > self.TRIGGER_DIST):
            #     try:
            #         #print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(lead_vehicle, ego_vehicle))
            #         pass
            #     except KeyboardInterrupt:
            #         #lead_vehicle.destroy()
            #         pass

            

            #Run pedestrian controllers
            for pedestrian_controller in self.pedestrian_controllers:

                pedestrian_controller.start()
                pedestrian_controller.go_to_location(carla.Location(13,139,0.2))
            #pedestrian.set_target_velocity(carla.Vector3D(0,-self.LEAD_VEHICLE_VELOCITY,0))
            # # #Start Recording Scenario before the scenario loop begins
            # # self.start_recording_scenario()
   
            
            # lead_vehicle.set_target_velocity(carla.Vector3D(0,-self.LEAD_VEHICLE_VELOCITY,0))
            # #Set the other vehicles on the other direction 
            # number_of_other_vehicles = 3
            # #Other vehicles moving the opposite direction 
            # npm_y_value = 150
            # for vehicle in range(number_of_other_vehicles):
            #     npc_vehicle_blueprint = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            #     spawn_loc = carla.Location(335, npm_y_value,self.Z)
            #     rotation = carla.Rotation(self.PITCH,90,self.ROLL)
            #     transform = carla.Transform(spawn_loc, rotation)
            #     npm_y_value-=20; 
            #     npc_vehicle = world.spawn_actor(npc_vehicle_blueprint, transform)
            #     npc_vehicle.set_target_velocity(carla.Vector3D(0,7,0))


            # current_velocity = self.LEAD_VEHICLE_VELOCITY 
            # #Speed up the vehicle at y 200 
            # lead_vehicle_target_stop_y = 220
            # while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
            #     print(lead_vehicle.get_location().y)
            # while current_velocity < 10:
            #     current_velocity+=0.01
            #     lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))
            
            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish
        finally:
            pass


    def destroy_all_vehicle_actors(self,world): 
        actors = world.get_actors()
        actors = actors.filter('vehicle.*') #filter out only vehicle actors
        if(actors):
            for actor in actors:
                actor.destroy()
        else:
            print('There are currently no vehicle actors in the Carla world. ')    



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





    #Start te

scenario_follow_vehicle = ScenarioFollowVehiclePriorVehicleManouver()
scenario_follow_vehicle.run()