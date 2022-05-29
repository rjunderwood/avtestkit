
#####MOCK Does not include the carla functionality





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

# Get CARLA .egg file
# try:
#     sys.path.append(glob.glob('/home/luuquanghung/CARLA_AUTOWARE/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg')[0])
# except IndexError:
#     print("Error: carla-0.9.10-py3.7-linux-x86_64.egg file doesn't exsit.")
#     pass
# else:
#     try:
#         sys.path.append(glob.glob('/home/luuquanghung/CARLA_AUTOWARE/PythonAPI/carla/dist/carla-0.9.10-py2.7-linux-x86_64.egg')[0])
#     except IndexError:
#         print("Error: carla-0.9.10-py2.7-linux-x86_64.egg file doesn't exist.")
#         pass
#     else:
#         print("Error: .egg file doesn't exist.")



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
    pass

#returns actor object for a specified id
def ret_actor(world, actor_id):
    pass


def destroy_actor(world, actor_id):
    pass


def on_collision(flag,event):
    pass

def on_lane_invasion(flag,event):
    pass


def record_stats(world, role_name_to_track, accessory_rolename=None, filename=None, param_value=0):
    pass

def track_location(args, world):
    pass

def plot_stats(axs, data, start_index = None, end_index = None):
    pass

def main(args):
    pass



if __name__ == '__main__':
    description = 'Carla-Autoware Manual Test Case - Stationary Vehicle' 
    parser = argparse.ArgumentParser(description=description)