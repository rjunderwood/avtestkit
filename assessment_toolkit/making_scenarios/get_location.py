

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
world = client.load_world('Town03')
spectator = world.get_spectator()


SPEC_CAM_X = -10
SPEC_CAM_Y = 117
SPEC_CAM_Z = 52
SPEC_CAM_PITCH = -70
SPEC_CAM_YAW = 90
SPEC_CAM_ROLL = 0 

spectator.set_transform(carla.Transform(carla.Location(SPEC_CAM_X, SPEC_CAM_Y,SPEC_CAM_Z),carla.Rotation(SPEC_CAM_PITCH,SPEC_CAM_YAW,SPEC_CAM_ROLL)))



while True:
    try:
        print(spectator.get_transform())
    except:
        pass


