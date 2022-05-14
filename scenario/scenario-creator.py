
import glob
import os
import sys
import random 
import time
import argparse
import math

# try:
#     sys.path.append(glob.glob('/home/luuquanghung/CARLA_AUTOWARE/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg'))
# except IndexError:
#     print("Error finding Carla .egg file")
#     pass

import carla 



def clear_world_actors(world):
    actor_list = world.get_actors()
    
    for actor in actor_list:
        actor.destroy()
    
    return 0 

def spawn_ego_vehicle(world,transform):

    ego_bp = world.get_blueprint_library().find('vehicle.tesla.model3')
    ego_bp.set_attribute('role_name','ego')
    print('\nEgo role_name is set')
    ego_color = random.choice(ego_bp.get_attribute('color').recommended_values)
    ego_bp.set_attribute('color',ego_color)
    print('\nEgo color is set')
    ego_vehicle = world.spawn_actor(ego_bp,transform)




    return ego_vehicle



def main():
    #Lead Vehicle
    X = -2.1
    Y = 120
    Z = 0.2 

    PITCH = 0
    YAW = 90
    ROLL = 0

    EGO_VEHICLE_NAME = 'ego_vehicle'

    TRIGGER_DIST = 25
    VEHICLE_MODEL = 'vehicle.toyota.prius'

    SPEC_CAM_X = 25
    SPEC_CAM_Y = 120
    SPEC_CAM_Z = 120
    SPEC_CAM_PITCH = -90
    SPEC_CAM_YAW = 0
    SPEC_CAM_ROLL = 0 

    SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

    LEAD_VEHICLE_VELOCOTY = 3
    client = carla.Client('localhost', 2000)
    client.set_timeout(2.0)
  
    world = client.get_world()
    spawn_points = world.get_map().get_spawn_points()
    spectator = world.get_spectator()
    lead_tranform = spawn_points[1]
    #spectator.set_transform(carla.Transform(carla.Location(SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z),carla.Rotation(SPEC_CAM_PITCH,SPEC_CAM_YAW,SPEC_CAM_ROLL)))
    spectator.set_transform(lead_tranform)
    world.set_weather(carla.WeatherParameters()) #Set the default weather 

    clear_world_actors(world)

    ego_transform = spawn_points[0]
    lead_tranform = spawn_points[1]




    #Library that is used for spawning actors
    blueprint_library = world.get_blueprint_library()

    #Select a blueprint for our lead vehicle
    lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == VEHICLE_MODEL)
    


    #set lead vehicle role_name attribute to reflect lead_vehicle so that it is easily distinguishable in debugging
    lead_vehicle_bp.set_attribute('role_name', SPAWNED_VEHICLE_ROLENAME)

    #set the physics of the lead vehicle 



    spawn_loc = carla.Location(X,Y,Z)
    rotation = carla.Rotation(PITCH, YAW, ROLL)
    transform = carla.Transform(spawn_loc, rotation)

    #spawn the vehicle
    lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)

    #spawn the ego vehicle
    #ego_vehicle = spawn_ego_vehicle(world,ego_transform)

    #Get the bounding Box
    bounding_box = lead_vehicle.bounding_box
    print(bounding_box.location)
    print(bounding_box.extent)
    
    
    lead_vehicle.set_autopilot(True)


main()











# class ScenarioCreator:
    

#     #Lead Vehicle
#     X = -2.1
#     Y = 120
#     Z = 0.2 

#     PITCH = 0
#     YAW = 90
#     ROLL = 0

#     EGO_VEHICLE_NAME = 'ego_vehicle'

#     TRIGGER_DIST = 25
#     VEHICLE_MODEL = 'vehicle.toyota.prius'

#     SPEC_CAM_X = 25
#     SPEC_CAM_Y = 120
#     SPEC_CAM_Z = 120
#     SPEC_CAM_PITCH = -90
#     SPEC_CAM_YAW = 0
#     SPEC_CAM_ROLL = 0 

#     SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

#     LEAD_VEHICLE_VELOCOTY = 3

  
#     world = client.get_world()
#     spectator = world.get_spectator()
#     spectator.set_transform(carla.Transform(carla.Location(SPEC_CAM_X, SPEC_CAM_Y, SPEC_CAM_Z),carla.Rotation(SPEC_CAM_PITCH,SPEC_CAM_YAW,SPEC_CAM_ROLL)))
#     world.set_weather(carla.WeatherParameters()) #Set the default weather 


#     #Library that is used for spawning actors
#     blueprint_library = world.get_blueprint_library()

#     #Select a blueprint for our lead vehicle
#     lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == VEHICLE_MODEL)


#     #set lead vehicle role_name attribute to reflect lead_vehicle so that it is easily distinguishable in debugging
#     lead_vehicle_bp.set_attribute('role_name', SPAWNED_VEHICLE_ROLENAME)


#     spawn_loc = carla.Location(X,Y,Z)
#     rotation = carla.Rotation(PITCH, YAW, ROLL)
#     transform = carla.Transform(spawn_loc, rotation)

#     #spawn the vehicle
#     lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)


#     def __init__(self):
#         return None


#     # def create_carla_client(self):
#     #     client = carla.Client('localhost', 2000)
#     #     client.set_timeout(2.0)
    
#     # def spawn_leading_vehicle(self):

        