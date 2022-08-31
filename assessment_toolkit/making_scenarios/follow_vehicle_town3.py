import glob 
import os
import sys
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

class ScenarioFollowVehicleTown3: 

    scenario_finished = False

    # X = 70
    # Y = 196.7
    X = 207 
    Y = -1.73
    Z = 1
    PITCH = 0
    YAW = 180
    ROLL = 0 

    EGO_VEHICLE_NAME = 'ego_vehicle'

    TRIGGER_DIST = 50
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    #Setup the spectator camera


    SPEC_CAM_X = 123
    SPEC_CAM_Y = -14
    SPEC_CAM_Z = 112
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 90
    SPEC_CAM_ROLL = 0 


    SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

    # LEAD_VEHICLE_VELOCITY = 3
    LEAD_VEHICLE_VELOCITY = 6

    
    #How long the scenario actually should run once recording is triggered. 
    RUNNING_TIME = 30

    def run(self):
            
        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(10.0)

            world = client.load_world('Town03')

            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))




        
            blueprint_library = world.get_blueprint_library()


            #Lead Vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            spawn_loc = carla.Location(self.X,self.Y,self.Z)
            rotation = carla.Rotation(self.PITCH,self.YAW,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)
            print("SPAWN")
            return 0


 





        
            # #Start Recording Scenario before the scenario loop begins
            # self.start_recording_scenario()
   
            
            lead_vehicle.set_target_velocity(carla.Vector3D(0,-self.LEAD_VEHICLE_VELOCITY,0))
            #Set the other vehicles on the other direction 
            number_of_other_vehicles = 3
            #Other vehicles moving the opposite direction 
            npm_y_value = 150
            for vehicle in range(number_of_other_vehicles):
                npc_vehicle_blueprint = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
                spawn_loc = carla.Location(335, npm_y_value,self.Z)
                rotation = carla.Rotation(self.PITCH,90,self.ROLL)
                transform = carla.Transform(spawn_loc, rotation)
                npm_y_value-=20; 
                npc_vehicle = world.spawn_actor(npc_vehicle_blueprint, transform)
                npc_vehicle.set_target_velocity(carla.Vector3D(0,7,0))


            current_velocity = self.LEAD_VEHICLE_VELOCITY 
            #Speed up the vehicle at y 200 
            lead_vehicle_target_stop_y = 220
            while(lead_vehicle.get_location().y > lead_vehicle_target_stop_y):
                print(lead_vehicle.get_location().y)
            while current_velocity < 10:
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
            #Slow Down 
            # lead_vehicle.set_target_velocity(carla.Vector3D(0,0,0))


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
        

scenario_follow_vehicle = ScenarioFollowVehicleTown3()
scenario_follow_vehicle.run()