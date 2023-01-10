
##Set the Spectator Camera

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



def setup_spectator_camera(self,X,Y,Z,PITCH,YAW,ROLL):
    spectator = self.world.get_spectator()
    spectator.set_transform(carla.Transform(carla.Location(self.SPEC_CAM_X, self.SPEC_CAM_Y,self.SPEC_CAM_Z),
    carla.Rotation(self.SPEC_CAM_PITCH,self.SPEC_CAM_YAW,self.SPEC_CAM_ROLL)))

