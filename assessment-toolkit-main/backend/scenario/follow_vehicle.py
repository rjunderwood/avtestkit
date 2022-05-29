import glob 
import os
import sys
import random
import time
import argparse
import math
import carla
import subprocess
import pathlib

from ..util.util import *

class ScenarioFollowVehicle:

    scenario_finished = False
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



    def run(self):
        
        try:
            client = carla.Client('localhost', 2000)
            client.set_timeout(2.0)
        
            world = client.get_world()

            spectator = world.get_spectator()
            spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
            carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))

            world.set_weather(carla.WeatherParameters())

            blueprint_library = world.get_blueprint_library()

            #Blueprint for the lead vehicle
            lead_vehicle_bp = next(bp for bp in blueprint_library if bp.id == self.VEHICLE_MODEL)

            lead_vehicle_bp.set_attribute('role_name', self.SPAWNED_VEHICLE_ROLENAME)


            spawn_loc = carla.Location(self.X,self.Y,self.Z)
            rotation = carla.Rotation(self.PITCH,self.YAW,self.ROLL)
            transform = carla.Transform(spawn_loc, rotation)

            lead_vehicle = world.spawn_actor(self.lead_vehicle_bp, transform)

            lead_vehicle.set_light_state(carla.VehicleLightState.All)


            # wait for the ego vehicle to spawn 

            while(find_actor_by_rolename(world,self.EGO_VEHICLE_NAME) == None):
                try:
                    print("Waiting for ego vehicle to spawn... ")
                except KeyboardInterrupt:
                    lead_vehicle.destroy()
            
            ego_vehicle = find_actor_by_rolename(world, self.EGO_VEHICLE_NAME)
            print('Ego vehicle found')




            #Start Recording Scenario before the scenario loop begins
            self.start_recording_scenario()
            

            while(calc_dist(lead_vehicle, ego_vehicle) > self.TRIGGER_DIST):
                try:
                    print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(lead_vehicle, ego_vehicle))
                except KeyboardInterrupt:
                    lead_vehicle.destroy()
            
            lead_vehicle.set_target_velocity(carla.Vector3D(0,self.LEAD_VEHICLE_VELOCITY,0))

            time.sleep(60)

            lead_vehicle.destroy()
        finally:
            print("Scenario Finished :: Follow Vehicle") 

            #Set the scenario as finished
            self.scenario_finished = True
        
            #Start recording the scenario in a separate process
    def start_recording_scenario(self):
        if os.name == 'nt':
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'\record_stats.py'], stdout=sys.stdout)
        else:
            subprocess.Popen(args=['python', str(pathlib.Path(__file__).parent.resolve())+r'/record_stats.py'], stdout=sys.stdout)

    def is_scenario_finished(self):
        return self.scenario_finished


