
from http import client
from logging import exception
import glob
import os
import sys
import random 
import time
import argparse
import math
# import matplotlib.pyplot as plt
import numpy as np
import json

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

# euclidean distance
def calc_dist(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()
    return math.sqrt((loc_a.x - loc_b.x)**2 + (loc_a.y - loc_b.y)**2 +(loc_a.y - loc_b.y)**2 )


def mag(vec): #return magnitude of Carla 3D vector 
    return math.sqrt(vec.x**2 - vec.y**2 + vec.z**2)



def find_actor_by_rolename(world, role_name_tofind):
    actors = world.get_actors()
    actors = actors.filter('vehicle.*') #filter out only vehicle actors
    print("ACTORS find_actor_by_rolename " + str(actors))
    if(actors):
        for actor in actors:
            role_name = "None"
            if 'role_name' in actor.attributes:
                if(actor.attributes['role_name'] == role_name_tofind):

                    print("ACTOR FOUND" + str(actor))
                    return actor
        
        return None
    
    else:
        return None


def retrieve_actors(world):
    actors = world.get_actors()
    actors = actors.filter('vehicle.*') #filter out only vehicle actors

    if(actors):
        for actor in actors:
            role_name = "None"
            if 'role_name' in actor.attributes:
                role_name = actor.attributes['role_name']
            loc = actor.get_location()
            print("ID: %s | Type: %s | Role Name: %s | Location(x,y,x): %0.2f,  %0.2f, %0.2f " % (actor.type_id, role_name, loc.x, loc.y,loc.z))

    else:
        print('There are currently no vehicle actors in the Carla world. ')    



def destroy_all_vehicle_actors(world): 

    actors = world.get_actors()
    actors = actors.filter('vehicle.*') #filter out only vehicle actors

    if(actors):
        for actor in actors:
            actor.destroy()

   
    else:
        print('There are currently no vehicle actors in the Carla world. ')    


#returns actor object for a specified id
def ret_actor(world, actor_id):
    actors = world.get_actors().filter('vehicle.*') #filter out only vehicle actors

    for actor in actors:
        if str(actor.id) == str(actor_id):
            return actor
    
    return None


def destroy_actor(world, actor_id):
    actor = ret_actor(world, actor_id)

    if(actor != None):
        actor.destroy()
        print("Successfully destroyed actor")
    else:
        print("No actor with that ID found.")
    
    return


def on_collision(flag,event):
    flag.append(event.normal_impulse)

def on_lane_invasion(flag,event):
    flag.append(True)


def record_stats(world, role_name_to_track, accessory_rolename=None, filename=None, param_value=0):
    #records various stats about an actor and optionally logs to file in the following format
    # simulation time, location x, location y, location z, velocity mag, acceleration mag, collision sensor, distance between this actor and another actor(optional)

    actor_to_track = find_actor_by_rolename(world, role_name_to_track)

    if(actor_to_track == None):
        print("No actor with that rolename exists") 
    

    #setup collision sensor
    collision_flag = []
    collision_bp = world.get_blueprint_library().find('sensor.other.collision')
    collision_sensor = world.spawn_actor(collision_bp, carla.Transform(), attach_to=actor_to_track)
    collision_sensor.listen(lambda event: on_collision(collision_flag, event))

    lane_inv_flag = []
    lane_inv_bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
    lane_inv_sensor = world.spawn_actor(lane_inv_bp, carla.Transform(), attach_to=actor_to_track)
    lane_inv_sensor.listen(lambda event: on_lane_invasion(lane_inv_flag, event)) 

    if(filename):
        f = open(filename,"w")
    
    start_t = time.time()


    while(actor_to_track != None):
        try:
            t=time.time() - start_t
            loc=actor_to_track.get_location()
            vel = actor_to_track.get_velocity()
            acc = actor_to_track.get_acceleration()

            #retrieve distance to other actor data 
            dist_to_actor = -10
            accessory_actor = find_actor_by_rolename(world, accessory_rolename)
            if(accessory_actor != None):#lane_invasion
                dist_to_actor = calc_dist(actor_to_track, accessory_actor)
            
            #retrieve collision data
            collision = 0 
            if(len(collision_flag) > 0): #sensor has flagged a collision 
                collision = mag(collision_flag[0])
                collision_flag = [] # reset collision flag 
            
            #retrieve lane invasion data 
            lane_invasion = 0 # 0 means no lane invasions detected 
            if(len(lane_inv_flag)>0):
                lane_invasion = 1 #lane invasion has occurred 
                lane_inv_flag = [] #reset collision flag

            #print data to screen
            print("Time: %0.2f | Loc: %0.2f,%0.2f,%0.2f | Vel: %0.2f | Acc: %0.2f | Collision: %s | Lane Invasion: %s | Dist to Other Actor: %0.2f" %(t,loc.x,loc.y,loc.z,mag(vel),mag(acc),collision,lane_invasion,dist_to_actor))

            #write data to file
            if(filename):
                f.write("%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f\r" % (t,loc.x,loc.y,loc.z,mag(vel),mag(acc),collision,lane_invasion,dist_to_actor))

            #Check the actor we are tracking still exists
            actor_to_track = find_actor_by_rolename(world, role_name_to_track) #check actor still exists
        
        except KeyboardInterrupt:
            print("")

            if(filename):
                f.close()
            
            return 
    
    if(filename):
        f.close()
    
    print("")
    print("Actor destroyed, no longer need to record data") 
    
    return 

def track_location(args, world):
    actors = world.get_actors()
    actors = actors.filter('vehicle.*') # filter out just the vehicle actors

    actor_to_track = ret_actor(args.actor_id)

    if(args.out_file):
        f = open(args.out_file, "w")

    previous_loc = carla.Location(0,0,0)

    while True:
        try:
            current_loc = actor_to_track.get_location()

            if(current_loc != previous_loc): # only record or print location if it has changed. i.e., car is not stationary.
                print('Location: %0.2f, %0.2f, %0.2f\r' % (current_loc.x, current_loc.y, current_loc.z), end = "\r")

                if(args.out_file):
                    f.write('%0.2f, %0.2f, %0.2f\r' % (current_loc.x, current_loc.y, current_loc.z)) 

            previous_loc = current_loc

        except KeyboardInterrupt:
            print("")

            if(args.out_file):
                f.close()
            
            return

def plot_stats(axs, data, start_index = None, end_index = None):

    #axs[0, 0].plot(data[:,0], data[:,4], color = "blue")
    axs[0, 0].plot(data[:,0], data[:,4])
    axs[0, 0].set_title('Velocity vs Simulation Time')
    axs[0, 0].set(xlabel = 'Simulation Time (s)', ylabel = 'Magnitude Velocity (m/s)')

    #axs[0, 1].plot(data[:,0], data[:,5], color = "green")
    axs[0, 1].plot(data[:,0], data[:,5])
    axs[0, 1].set_title('Acceleration vs Simulation Time')
    axs[0, 1].set(xlabel = 'Simulation Time (s)', ylabel = 'Magnitude Acceleration (m/s^2)')
    axs[0, 1].set_ylim([0, 25])

    #axs[1, 0].plot(data[:,1], data[:,2], color = "black")
    axs[1, 0].plot(data[:,1], data[:,2])
    axs[1, 0].set_title('Vehicle Location: y-coord vs x-coord')
    axs[1, 0].set(xlabel = 'x-coord', ylabel = 'y-coord')

def main(args):
    try:
        client = carla.Client('localhost', 2000) # create client to connect to simulator
        client.set_timeout(2.0)

        world = client.get_world() # retrieve carla world object

        print('Successfully connected and retrieved CARLA world.')

        if(args.get_actors):
            retrieve_actors(world)
        elif(args.track_actor_loc):
            if(args.actor_id):
                track_location(args, world)
            else:
                print("Please specify actor Id.")
        elif(args.destroy_actor):
            destroy_actor(world, args.destroy_actor)
        elif(args.follow_actor):
            #follow_actor(world, args.follow_actor)
            pass
        elif(args.change_town): 
            #change_town(client, args.change_town)
            pass
        elif(args.visualize_stats):
            #visualize_stats(args.out_file)
            pass
        elif(args.record_stats):
            if(args.accessory_rolename):
                print(args.accessory_rolename)
                record_stats(world=world,role_name_to_track=args.record_stats, accessory_rolename=args.accessory_rolename, filename=args.out_file, param_value=float(args.param_value))
        else:
            print('No functionality specified')
    finally:
        print('Finally')



def await_ego_spawn(self):
    # wait for the ego vehicle to spawn 
    while(find_actor_by_rolename(self.world,self.EGO_VEHICLE_NAME) == None):
        try:
            print("Waiting for ego vehicle to spawn... ")
        except KeyboardInterrupt:
            # lead_vehicle.destroy()
            pass
    
    ego_vehicle = find_actor_by_rolename(self.world, self.EGO_VEHICLE_NAME)
    print('Ego vehicle found')
    self.ego_vehicle = ego_vehicle

#Distance trigger from carla actor to ego vehicle that activates the scenario
def await_scenario_trigger(self):
    print("await_scenario_trigger")
    while(calc_dist(self.scenario_trigger_actor, self.ego_vehicle) > self.TRIGGER_DIST):

        try:
            print("Waiting for ego vehicle to enter within trigger distance. Current distance: %im " % calc_dist(self.scenario_trigger_actor, self.ego_vehicle))
            pass
        except KeyboardInterrupt:
            #lead_vehicle.destroy()
            pass

    



if __name__ == '__main__':
    description = 'Carla-Autoware Manual Test Case - Stationary Vehicle' 
    parser = argparse.ArgumentParser(description=description)