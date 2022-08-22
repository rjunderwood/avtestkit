

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

import carla


client = carla.Client('localhost', 2000)
client.set_timeout(20.0)
world = client.load_world('Town01')
spectator = world.get_spectator()


while True:
    try:
        print(spectator.get_location())
    except:
        pass


