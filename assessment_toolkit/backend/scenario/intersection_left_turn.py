# intersection left turn scenario takes place during daylight in a rural environment, 
# using a straight intersection with posted speed limit of 35mph, 
# cuts across the path of another vehicle travelling from the 
# opposite direction.

from .scenario import Scenario

import carla
from ..util.util import *
from backend.util.weather import get_weather_parameters
from backend.util.stats_recorder import StatsRecorder
from backend.interface import ros_close as rclose

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

    TRIGGER_DIST = 80

    def __init__(self, name, X, Y, Z, PITCH, YAW, ROLL, SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z, RUNNING_TIME) -> None:
        super().__init__(name, X, Y, Z, PITCH, YAW, ROLL, SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z, RUNNING_TIME)

        #Metamorphic Tests
    METAMORPHIC_TEST_FILE_LOCATION= CWD + "/backend/scenario/metamorphic_tests/intersection_left_turn.json"
    metamorphic_test_target_file = open(METAMORPHIC_TEST_FILE_LOCATION)
    metamorphic_tests = json.loads(metamorphic_test_target_file.read())
    metamorphic_test_running = False


    def run(self):
        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)

            world = client.get_world()

            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH, self.SPEC_CAM_YAW, self.SPEC_CAM_ROLL)))
    
            blueprint_library = world.get_blueprint_library()
            # Metamophic parameters for this test
            metamorphic_parameters = self.metamorphic_tests[self.get_current_metamorphic_test_index()]['parameters']
            self.VEHICLE_MODEL = metamorphic_parameters['oncoming_vehicle_model']
            self.SPAWNED_VEHICLE_VELOCITY = metamorphic_parameters['oncoming_vehicle_velocity']
            
            # Oncoming Traffic
            spawned_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)
            spawned_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)
            spawn_loc = carla.Location(self.X, self.Y, self.Z)
            rotation = carla.Rotation(self.PITCH, self.YAW, self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)
            spawned_vehicle = world.spawn_actor(spawned_vehicle_bp, transform)
            spawned_vehicle.set_light_state(carla.VehicleLightState.All)

         
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

            # Start the metamorphic test 
            self.metamorphic_test_running = True 


            while(calc_dist(spawned_vehicle, ego_vehicle) > 60):
                    try:
                        print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(spawned_vehicle, ego_vehicle))
                        pass
                    except KeyboardInterrupt:
                        #lead_vehicle.destroy()
                        pass
            
            spawned_vehicle.set_target_velocity(carla.Vector3D(0,self.SPAWNED_VEHICLE_VELOCITY,0))

            #Set the other vehicles on the other direction 
            number_of_other_vehicles = metamorphic_parameters['passing_vehicles']
            vehicle_types = metamorphic_parameters['car_types']
            npm_y_value = 120
            for vehicle in range(0,number_of_other_vehicles):
                for bp in blueprint_library:
                    if bp.id == vehicle_types[vehicle]:
                        spawned_vehicle_bp = bp
                        break
                spawn_loc = carla.Location(335, npm_y_value,self.Z)
                rotation = carla.Rotation(self.PITCH, self.YAW, self.ROLL)
                transform = carla.Transform(spawn_loc, rotation)
                npm_y_value-=20; 
                spawned_vehicle = world.spawn_actor(spawned_vehicle_bp, transform)
                spawned_vehicle.set_target_velocity(carla.Vector3D(0,5,0))

            # current_velocity = self.LEAD_VEHICLE_VELOCITY 
            # #Speed up the vehicle at y 200 
            # lead_vehicle_target_stop_y = 220
            # while(running_vehicle.get_location().y > lead_vehicle_target_stop_y):
            #     print(running_vehicle.get_location().y)
            # while current_velocity < 6:
            #     current_velocity+=0.01
            #     running_vehicle.set_target_velocity(carla.Vector3D(0,-current_velocity,0))


            self.handle_results_output(world)

            self.set_test_finished(world)
            # lead_vehicle.destroy()
            
            #After the record stats has completed in the RUNNING_TIME the scenario will finish

                
        finally:
            print("Scenario Finished :: Follow Vehicle") 

            
            #Set the metamorphic test as finished


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

        rclose.ROSClose()


    
    
    def handle_results_output(self, world):
  
        #This is where the Real scenario begins. Time to start recording stats. 
        results_file_name = 'intersection_left_turn_' + str(self.get_current_metamorphic_test_index())    
        results_file_path = CWD + "/backend/scenario/results/"+results_file_name+".txt"
        stats_recorder = StatsRecorder(world, self.RUNNING_TIME)
        stats_recorder.record_stats('ego_vehicle', self.SPAWNED_VEHICLE_ROLENAME, results_file_path)

        #Set number of collision and lane invastions to metamorphic test to save as json
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['number_of_collisions'] = stats_recorder.get_number_of_collisions()
        self.metamorphic_tests[self.get_current_metamorphic_test_index()]['number_of_lane_invasions'] = stats_recorder.get_number_of_lane_invasions()
