import glob 
import os
import sys
import random
import time
import argparse
import math



import carla

import util #import utility file

# X = -2.1
# Y = 120
X = 340
Y = 240
Z = 0.2

PITCH = 0
YAW = 270
ROLL = 0 

EGO_VEHICLE_NAME = 'ego_vehicle'

TRIGGER_DIST = 25 
VEHICLE_MODEL = 'vehicle.toyota.prius'

#Setup the spectator camera

SPEC_CAM_X = 340
SPEC_CAM_Y = 240
SPEC_CAM_Z = 120
SPEC_CAM_PITCH = -90
SPEC_CAM_YAW = 0
SPEC_CAM_ROLL = 0 


SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

LEAD_VEHICLE_VELOCITY = 3



def main(args):

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(2.0)
    
        world = client.get_world()

        spectator = world.get_spectator()
        spectator.set_transform(carla.Transform(carla.Location(SPEC_CAM_X, SPEC_CAM_Y,SPEC_CAM_Z),
        carla.Rotation(SPEC_CAM_PITCH,SPEC_CAM_YAW,SPEC_CAM_ROLL)))

        world.set_weather(carla.WeatherParameters())

        blueprint_library = world.get_blueprint_library()

        #Blueprint for the lead vehicle
        lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == VEHICLE_MODEL)

        lead_vehicle_bp.set_attribute('role_name', SPAWNED_VEHICLE_ROLENAME)


        spawn_loc = carla.Location(X,Y,Z)
        rotation = carla.Rotation(PITCH,YAW,ROLL)
        transform = carla.Transform(spawn_loc, rotation)

        lead_vehicle = world.spawn_actor(lead_vehicle_bp, transform)

        lead_vehicle.set_light_state(carla.VehicleLightState.All)


        # wait for the ego vehicle to spawn 

        while(util.find_actor_by_rolename(world,EGO_VEHICLE_NAME) == None):
            try:
                print("Waiting for ego vehicle to spawn... ")
            except KeyboardInterrupt:
                lead_vehicle.destroy()
        
        ego_vehicle = util.find_actor_by_rolename(world, EGO_VEHICLE_NAME)
        print('Ego vehicle found')

        while(util.calc_dist(lead_vehicle, ego_vehicle) > TRIGGER_DIST):
            try:
                print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % util.calc_dist(lead_vehicle, ego_vehicle))
            except KeyboardInterrupt:
                lead_vehicle.destroy()
        
        lead_vehicle.set_target_velocity(carla.Vector3D(0,LEAD_VEHICLE_VELOCITY,0))

        time.sleep(60)

        lead_vehicle.destroy()
    finally:
        print("Finished Executing Test Case!") 

if __name__ == '__main__':
    description = 'Carla-Autoware Manual Test Case - Stationary Vehicle' 
    parser = argparse.ArgumentParser(description=description)