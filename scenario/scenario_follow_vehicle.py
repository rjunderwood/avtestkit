
from ast import While
import carla 


import matplotlib.pyplot as plt
import numpy as np
import math




class ScenarioFollowVehicle:

    #Carla World
    world = None
    WEATHER = carla.WeatherParameters()
    #Ego Vehicle
    ego_vehicle = None 
    EGO_X = 301
    EGO_Y = 327.049988
    EGO_Z = 0.036313
    EGO_PITCH = 0
    EGO_YAW = 0
    EGO_ROLL = 0
    #Lead Vehicle
    lead_vehicle = None
    LEAD_VEHICLE_MODEL = 'vehicle.toyota.prius'
    LEAD_VEHICLE_ROLENAME = 'lead_vehicle'
    LEAD_X = 280
    LEAD_Y = 327.049988
    LEAD_Z = 0.2
    LEAD_PITCH = 0
    LEAD_YAW = 0
    LEAD_ROLL = 0
    #Spectator Camera
    spectator = None
    SPEC_CAM_X = 301
    SPEC_CAM_Y = 327.049988
    SPEC_CAM_Z = 120
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 


    #Set the world and ego vehicle from ScenarioBase call
    def __init__(self,world,ego_vehicle):
        self.world = world 
        self.ego_vehicle = ego_vehicle

     

    





    def setup_world(self):
        self.world.set_weather(self.WEATHER) #Set the weather

    
    def setup_ego_vehicle(self):
        ego_transform = carla.Transform(
            carla.Location(self.EGO_X, self.EGO_Y, self.EGO_Z),
            carla.Rotation(self.EGO_PITCH,self.EGO_YAW,self.EGO_ROLL)
        ) 
        self.ego_vehicle.set_transform(ego_transform)  

    def setup_lead_vehicle(self):
        #Clear Previous Leading Vehicle
        actor_list = self.world.get_actors()
        for actor in actor_list:
            try:
                if(actor.attributes['role_name'] == 'lead_vehicle'):
                    actor.destroy()
            except: 
                pass
        
        lead_transform = carla.Transform(
            carla.Location(self.LEAD_X,self.LEAD_Y,self.LEAD_Z),
            carla.Rotation(self.LEAD_PITCH,self.LEAD_YAW,self.LEAD_ROLL)
        )
            
        #Library that is used for spawning actors
        blueprint_library = self.world.get_blueprint_library()
        #Select a blueprint for our lead vehicle
        lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.LEAD_VEHICLE_MODEL)
        lead_vehicle_bp.set_attribute('role_name', self.LEAD_VEHICLE_ROLENAME)
        #Spawn Vehicle
        vehicle = self.world.spawn_actor(lead_vehicle_bp, lead_transform)

         #Vehicle properties setup
        physics_control = vehicle.get_physics_control()
        max_steer = physics_control.wheels[0].max_steer_angle
        rear_axle_center = (physics_control.wheels[2].position + physics_control.wheels[3].position)/200
        offset = rear_axle_center - vehicle.get_location()
        wheelbase = np.linalg.norm([offset.x, offset.y, offset.z])
        vehicle.set_simulate_physics(True)
        self.lead_vehicle = vehicle
        spectator = self.world.get_spectator()

        vehicle.set_autopilot(True) 

        # self.lead_vehicle.set_autop

        while True: 
            #vehicle.apply_control(carla.VehicleControl(throttle=0.1, steer=0))
            spectator_transform = carla.Transform(carla.Location(vehicle.get_transform().location.x, vehicle.get_transform().location.y, self.SPEC_CAM_Z),carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL))
            spectator.set_transform(spectator_transform)
    
    def setup_spectator(self):
      
        spectator = self.world.get_spectator()
        spectator_transform = carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y, self.SPEC_CAM_Z),carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL))
        spectator.set_transform(spectator_transform)
        self.spectator = spectator


    
        

    #Run the Scenario
    def run(self):

        #1 Setup World
        self.setup_world()

        #4 Setup Spectator
        self.setup_spectator()   

        #2 Setup Ego Vehicle 
        #self.setup_ego_vehicle()

        #3 Setup Lead Vehicle
        self.setup_lead_vehicle()

        #Self Vehicle Movements
        #self.move_lead_vehicle()

    def move_lead_vehicle(self):
        map = self.world.get_map()
        waypoint_list = map.generate_waypoints(40)
        print("Length: " + str(len(waypoint_list)))
       
        targetLane = -3
        waypoints = self.single_lane(waypoint_list, targetLane)

        #
        curvy_waypoints = self.get_curvy_waypoints(waypoints)
        x = [p.transform.location.x for p in curvy_waypoints]
        y = [p.transform.location.y for p in curvy_waypoints]
        plt.plot(x, y, marker = 'o')
        plt.savefig("bezier.png")

        #Set spawning location as initial waypoint
        waypoint = curvy_waypoints[0]
        blueprint = self.world.get_blueprint_library().filter('vehicle.*model3*')[0]
        location = waypoint.transform.location + carla.Vector3D(0, 0, 1.5)
        rotation = waypoint.transform.rotation
        
        print("location of initial waypoint :::" + waypoint.transform.location)

        vehicle = self.world.spawn_actor(blueprint, carla.Transform(location, rotation))
        print("SPAWNED!")

        #Vehicle properties setup
        physics_control = vehicle.get_physics_control()
        max_steer = physics_control.wheels[0].max_steer_angle
        rear_axle_center = (physics_control.wheels[2].position + physics_control.wheels[3].position)/200
        offset = rear_axle_center - vehicle.get_location()
        wheelbase = np.linalg.norm([offset.x, offset.y, offset.z])
        vehicle.set_simulate_physics(True)


        while True:

            #Update the camera view
            #spectator.set_transform(camera.get_transform())
            #Get next waypoint
            waypoint = self.get_next_waypoint(self.world, vehicle, curvy_waypoints)
            self.world.debug.draw_point(waypoint.transform.location, life_time=5)

            #Control vehicle's throttle and steering
            throttle = 0.85
            vehicle_transform = vehicle.get_transform()
            vehicle_location = vehicle_transform.location
            steer = self.control_pure_pursuit(vehicle_transform, waypoint.transform, max_steer, wheelbase)
            control = carla.VehicleControl(throttle, steer)
            vehicle.apply_control(control)

            #Control vehicle's throttle and steering
            throttle = 0.85
            vehicle_transform = vehicle.get_transform()
            vehicle_location = vehicle_transform.location
            steer = self.control_pure_pursuit(vehicle_transform, waypoint.transform, max_steer, wheelbase)
            control = carla.VehicleControl(throttle, steer)
            vehicle.apply_control(control)




    #https://medium.com/@chardorn/creating-carla-waypoints-9d2cc5c6a656https://medium.com/@chardorn/creating-carla-waypoints-9d2cc5c6a656

    #Returns only the waypoints in one lane
    def single_lane(waypoint_list, lane):
        waypoints = []
        for i in range(len(waypoint_list) - 1):
            if waypoint_list[i].lane_id == lane:
                waypoints.append(waypoint_list[i])
        return waypoints
        


    def get_curvy_waypoints(waypoints):
        curvy_waypoints = []
        for i in range(len(waypoints) - 1):
            x1 = waypoints[i].transform.location.x
            y1 = waypoints[i].transform.location.y
            x2 = waypoints[i+1].transform.location.x
            y2 = waypoints[i+1].transform.location.y
            if (abs(x1 - x2) > 1) and (abs(y1 - y2) > 1):
                print("x1: " + str(x1) + "  x2: " + str(x2))
                print(abs(x1 - x2))
                print("y1: " + str(y1) + "  y2: " + str(y2))
                print(abs(y1 - y2))
                curvy_waypoints.append(waypoints[i])
        
        #To make the path reconnect to the starting location
        curvy_waypoints.append(curvy_waypoints[0])

        return curvy_waypoints


    def control_pure_pursuit(vehicle_tr, waypoint_tr, max_steer, wheelbase):
        # TODO: convert vehicle transform to rear axle transform
        wp_loc_rel = self.relative_location(vehicle_tr, waypoint_tr.location) + carla.Vector3D(wheelbase, 0, 0)
        wp_ar = [wp_loc_rel.x, wp_loc_rel.y]
        d2 = wp_ar[0]**2 + wp_ar[1]**2
        steer_rad = math.atan(2 * wheelbase * wp_loc_rel.y / d2)
        steer_deg = math.degrees(steer_rad)
        steer_deg = np.clip(steer_deg, -max_steer, max_steer)
        return steer_deg / max_steer


    def relative_location(frame, location):
        origin = frame.location
        forward = frame.get_forward_vector()
        right = frame.get_right_vector()
        up = frame.get_up_vector()
        disp = location - origin
        x = np.dot([disp.x, disp.y, disp.z], [forward.x, forward.y, forward.z])
        y = np.dot([disp.x, disp.y, disp.z], [right.x, right.y, right.z])
        z = np.dot([disp.x, disp.y, disp.z], [up.x, up.y, up.z])
        return carla.Vector3D(x, y, z)




    def get_next_waypoint(world, vehicle, waypoints):
        vehicle_location = vehicle.get_location()
        min_distance = 1000
        next_waypoint = None

        for waypoint in waypoints:
            waypoint_location = waypoint.transform.location

            #Only check waypoints that are in the front of the vehicle (if x is negative, then the waypoint is to the rear)
            #TODO: Check if this applies for all maps
            if (waypoint_location - vehicle_location).x > 0:

                #Find the waypoint closest to the vehicle, but once vehicle is close to upcoming waypoint, search for next one
                if vehicle_location.distance(waypoint_location) < min_distance and vehicle_location.distance(waypoint_location) > 5:
                    min_distance = vehicle_location.distance(waypoint_location)
                    next_waypoint = waypoint

        return next_waypoint



