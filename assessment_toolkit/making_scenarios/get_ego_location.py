

import glob 
import os
import sys
import random
import json
CONFIG = json.load(open('../config.json'));
try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

EGO_VEHICLE_NAME = 'ego_vehicle'

import carla



def find_actor_by_rolename(world, role_name_tofind):
    print("25555")
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







client = carla.Client('localhost', 2000)
client.set_timeout(10.0)
world = client.get_world()

ego_vehicle = None

# wait for the ego vehicle to spawn 
while(ego_vehicle == None):
    try:
        print("Waiting for ego vehicle to spawn... ")

        ego_vehicle = find_actor_by_rolename(world,EGO_VEHICLE_NAME)
    except KeyboardInterrupt:
        # lead_vehicle.destroy()
        pass


print("EGO LOCATION : ")

print(ego_vehicle.get_location())