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


class ScenarioFollowVehicle:

    scenario_finished = False
    # X = -2.1
    # Y = 120
    X = 330
    Y = 240
    Z = 0.2

    PITCH = 0
    YAW = 0
    #YAW = 270
    ROLL = 0 

    EGO_VEHICLE_NAME = 'ego_vehicle'

    TRIGGER_DIST = 40
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    #Setup the spectator camera

    SPEC_CAM_X = 155
    SPEC_CAM_Y = 65
    SPEC_CAM_Z = 100
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 90
    SPEC_CAM_ROLL = 0 




    # EGO_VEHICLE_X= 105
    # EGO_VEHICLE_Y = 63
    # EGO_VEHICLE_Z = 0.2


    EGO_VEHICLE_X= 190
    EGO_VEHICLE_Y = 63
    EGO_VEHICLE_Z = 0.2

    SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

    # LEAD_VEHICLE_VELOCITY = 3
    LEAD_VEHICLE_VELOCITY = 6

    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 30

    def run(self):
            
        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)

            world = client.load_world('Town03')
            self.destroy_all_vehicle_actors(world)
            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))


            blueprint_library = world.get_blueprint_library()

            spawn_loc = carla.Location(152,53,0.4)
            rotation = carla.Rotation(self.PITCH,90,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            # lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)
            # lead_vehicle.set_light_state(carla.VehicleLightState.All)



            #Metamophic Parameters Specific for this test
            # metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            
            world.set_weather(self.get_weather_parameters('Cloudy Sunset'))

          
            blueprintsWalkers = blueprint_library.filter("walker.pedestrian.*")
            walker_bp = random.choice(blueprintsWalkers)

            # #Pedestrian
            pedestiran = world.spawn_actor(walker_bp, transform)
            walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
            controller = world.spawn_actor(walker_controller_bp,carla.Transform(), pedestiran)

            #EGO Vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            ego_spawn_loc = carla.Location(self.EGO_VEHICLE_X,self.EGO_VEHICLE_Y, self.EGO_VEHICLE_Z)
            ego_rotation = carla.Rotation(0,0,0)
            ego_transform = carla.Transform(ego_spawn_loc, ego_rotation)
            ego_vehicle = world.spawn_actor(lead_vehicle_bp, ego_transform)

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
            

            # while(calc_dist(pedestiran, ego_vehicle) > self.TRIGGER_DIST):
            #     try:
            #         #print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(lead_vehicle, ego_vehicle))
            #         pass
            #     except KeyboardInterrupt:
            #         #lead_vehicle.destroy()
            #         pass


            controller.start()
            controller.go_to_location(carla.Location(153,69,0.2))
            #pedestiran.set_target_velocity(carla.Vector3D(0,-self.LEAD_VEHICLE_VELOCITY,0))
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



            # #Slow down the vehicle at y 150
            # lead_vehicle_target_stop_y = 200
            # while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
            #     pass
         
            # while current_velocity > 4:
            #     current_velocity-=0.01
            #     lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))

            
            # #Slow down to stop the vehicle at y 100
            # lead_vehicle_target_stop_y = 180
            # while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
            #     pass
         
            # while current_velocity > 0:
            #     current_velocity-=0.01
            #     lead_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))

            
            #Speed up 
            #Slow Down 
            # lead_vehicle.set_target_velocity(carla.Vector3D(0,0,0))
            while(True):
                # spectator_location = spectator.get_location()
                # print(spectator_location.x)
                # print(spectator_location.y) 
                spectator_rotation = spectator.get_transform()
                print(str(spectator_rotation)+"\n\n")
          
            

            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish
        finally:
            pass


    def get_weather_parameters(self,weather):

        if weather == 'Clear Noon':
            return carla.WeatherParameters.ClearNoon 

        elif weather == 'Cloudy Noon':
            return carla.WeatherParameters.CloudyNoon 
        elif weather == 'Wet Noon':
            return carla.WeatherParameters.WetNoon
        elif weather == 'Wet Cloudy Noon':
            return carla.WeatherParameters.WetCloudyNoon
        elif weather == 'Mid Rain Noon': 
            return carla.WeatherParameters.MidRainyNoon
        elif weather == 'Hard Rain Noon': 
            return carla.WeatherParameters.HardRainNoon
        elif weather == 'Soft Rain Noon':
            return carla.WeatherParameters.SoftRainNoon
        elif weather == 'Clear Sunset':
            return carla.WeatherParameters.ClearSunset
        elif weather == 'Cloudy Sunset':
            return carla.WeatherParameters.CloudySunset
        elif weather == 'Wet Sunset':
            return carla.WeatherParameters.WetSunset
        elif weather == 'Wet Cloudy Sunset':
            return carla.WeatherParameters.WetCloudySunset
        elif weather == 'Mid Rain Sunset':
            return carla.WeatherParameters.MidRainSunset
        elif weather == 'Hard Rain Sunset':
            return carla.WeatherParameters.HardRainSunset
        elif weather == 'Soft Rain Sunset':
            return carla.WeatherParameters.SoftRainSunset




    def destroy_all_vehicle_actors(self,world): 

        actors = world.get_actors()
        actors = actors.filter('vehicle.*') #filter out only vehicle actors

        if(actors):
            for actor in actors:
                actor.destroy()

    
        else:
            print('There are currently no vehicle actors in the Carla world. ')    
        

scenario_follow_vehicle = ScenarioFollowVehicle()
scenario_follow_vehicle.run()