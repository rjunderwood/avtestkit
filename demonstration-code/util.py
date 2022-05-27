
import os
import sys
import random 
import time
import argparse
import math
import matplotlib.pyplot as plt
import numpy as np

import carla

def calc_dist(actor_a, actor_b):
    loc_a = actor_a.get_location()
    loc_b = actor_b.get_location()
    return math.sqrt((loc_a.x - loc_b.x)**2 + (loc_a.y - loc_b.y)**2 +(loc_a.y - loc_b.y)**2 )


def mag(vec): #return magnitude of Carla 3D vector 
    return math.sqrt(vec.x**2 - vec.y**2 + vec.z**2)



def find_actor_by_rolename(world, role_name_tofind):
    actors = world.get_actors()
    actors = actors.filter('vehicle.*') #filter out only vehicle actors

    if(actors):
        for actor in actors:
            role_name = "None"
            if 'role_name' in actor.attributes:
                if(actor.attributes['role_name'] == role_name_tofind):
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


def on_conllision(flag,event):
    flag.append(event.normal_impulse)

def on_laneinvasion(flag,event):
    flag.append(True)


def record_stats(world, role_name_to_track, accessory_rolename=None, filename=None, param_value=0):
    #records various stats about an actor and optionally logs to file in the following format
    # simulation time, location x, location y, location z, velocity mag, acceleration mag, collision sensor, distance between this actor and another actor(optional)

    actor_to_track = find_actor_by_rolename(world, role_name_to_track)

    if(actor_to_track == None):
        print("No actor with that rolename exists") 
    

    #setup collision sensor
    collision_flag = []
    collision_sensor = world.get_blueprint_library().find('sensor.other.collision')
    collision_sensor.listen(lambda event: on_conllision(collision_flag, event))

    lane_inv_flag = []
    lane_inv_bp = world.get_blueprint_library().find('sensor.other.lane_invasion')
    lane_inv_sensor = world.spawn_actor(lane_inv_bp, carla.Transform(), attach_to=actor_to_track)
    lane_inv_sensor.listen(lambda event: on_laneinvasion(lane_inv_flag, event)) 

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
            if(accessory_actor != None):
                dist_to_actor = calc_dist(actor_to_track, accessory_actor)
            
            #retrieve collision data
            collision = 0 
            if(len(collision_flag) > 0): #sensor has flagged a collision 
                collision = mag(collision_flag[0])
                collision_flag = [] # reset collision flag 
            
            #retrieve lane invasion data 
            laneinvasion = 0 # 0 means no lane invasions detected 
            if(len(lane_inv_flag)>0):
                laneinvation = 1 #lane invasion has occurred 
                lane_inv_flag = [] #reset collision flag

            #print data to screen
            print("Time: %0.2f | Loc: %0.2f,%0.2f,%0.2f | Vel: %0.2f | Acc: %0.2f | Collision: %s | Lane Invasion: %s | Dist to Other Actor: %0.2f" %(t,loc.x,loc.y,loc.z,mag(vel),mag(acc),collision,laneinvasion,dist_to_actor))

            #write data to file
            if(filename):
                f.write("%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f,%0.2f\r" % (t,loc.x,loc.y,loc.z,mag(vel),mag(acc),collision,laneinvasion,dist_to_actor))

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


    