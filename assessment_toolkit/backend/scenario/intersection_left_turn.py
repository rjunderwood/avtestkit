# intersection left turn scenario takes place during daylight in a rural environment, 
# using a straight intersection with posted speed limit of 35mph, 
# cuts across the path of another vehicle travelling from the 
# opposite direction.

from .scenario import Scenario

import carla
from ..util.util import *
from .weather import get_weather_parameters

CWD = os.getcwd() 

CONFIG = json.load(open(CWD+'/config.json'));

try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

class IntersectionLeftTurn(Scenario):

    def __init__(self, name, X, Y, Z, PITCH, YAW, ROLL, SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z, RUNNING_TIME) -> None:
        super().__init__(name, X, Y, Z, PITCH, YAW, ROLL, SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z, RUNNING_TIME)


    def run(self):

        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)

            world = client.get_world()

            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform((carla.Location)))
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))
    
            blueprint_library = world.get_blueprint_library()


            # Running Red Light Vehicle
            running_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            running_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            spawn_loc = carla.Location(self.X,self.Y,self.Z)
            rotation = carla.Rotation(self.PITCH,self.YAW,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            running_vehicle = world.spawn_actor(running_vehicle_bp, transform)
            running_vehicle.set_light_state(carla.VehicleLightState.All)

            # TODO: Probably set the red light traffic signals here?


            #Metamophic Parameters Specific for this test
            metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            
            world.set_weather(get_weather_parameters(metamorphic_parameters['weather']))


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
            

            # TODO: trigger dist for sending running red light vehicle?
            # while(calc_dist(running_vehicle, ego_vehicle) > self.TRIGGER_DIST):
            #     try:
            #         #print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(lead_vehicle, ego_vehicle))
            #         pass
            #     except KeyboardInterrupt:
            #         #lead_vehicle.destroy()
            #         pass
            
            running_vehicle.set_target_velocity(carla.Vector3D(self.RUNNING_VEHICLE_VELOCITY,0,0))

            #Set the other vehicles on the other direction 
            number_of_other_vehicles = metamorphic_parameters['passing_vehicles']
            vehicle_types = metamorphic_parameters['car_types']
            #Other vehicles moving the opposite direction 
            npm_y_value = 150
            for vehicle in range(0,number_of_other_vehicles):
                for bp in blueprint_library:
                    if bp.id == vehicle_types[vehicle]:
                        npc_vehicle_blueprint = bp
                        break
                # npc_vehicle_blueprint = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
                spawn_loc = carla.Location(335, npm_y_value,self.Z)
                rotation = carla.Rotation(self.PITCH,90,self.ROLL)
                transform = carla.Transform(spawn_loc, rotation)
                npm_y_value-=20; 
                npc_vehicle = world.spawn_actor(npc_vehicle_blueprint, transform)
                npc_vehicle.set_target_velocity(carla.Vector3D(0,7,0))

            # current_velocity = self.LEAD_VEHICLE_VELOCITY 
            # #Speed up the vehicle at y 200 
            # lead_vehicle_target_stop_y = 220
            # while(running_vehicle.get_location().y > lead_vehicle_target_stop_y):
            #     print(running_vehicle.get_location().y)
            # while current_velocity < 6:
            #     current_velocity+=0.01
            #     running_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))


            self.handle_results_output(world)


            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish

                
        finally:
            print("Scenario Finished :: Follow Vehicle") 

            
            #Set the metamorphic test as finished
            self.set_test_finished(world)