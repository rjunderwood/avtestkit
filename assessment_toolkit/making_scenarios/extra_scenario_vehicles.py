

import glob 
import os
import sys
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

from toolkit_vehicles import ToolkitVehicles 



#Spawn distraction vehicles
def handle_spawn_extra_scenario_vehicles(self):

    #Vehicle Blueprint Creator 
    toolkit_vehicles = ToolkitVehicles(self.blueprint_library)
    #SPAWN LOCATION 1 VEHICLES
    for spawn_vehicle in self.metamorphic_parameters['spawn_vehicle_location_1']:
        self.spawn_vehicle_carla(spawn_vehicle,toolkit_vehicles)
    #SPAWN LOCATION 2 VEHICLES
    for spawn_vehicle in self.metamorphic_parameters['spawn_vehicle_location_2']:
        self.spawn_vehicle_carla(spawn_vehicle,toolkit_vehicles)

#Spawn individual vehicle
def spawn_vehicle_carla(self, spawn_vehicle, toolkit_vehicles):

    vehicle_bp = toolkit_vehicles.create(spawn_vehicle['model'])
    #There is a line up of vehicles 
    spawn_loc = carla.Location(spawn_vehicle['location']['X'],spawn_vehicle['location']['Y'],spawn_vehicle['location']['Z'])
    rotation = carla.Rotation(spawn_vehicle['location']['PITCH'],spawn_vehicle['location']['YAW'],spawn_vehicle['location']['ROLL'])
    transform = carla.Transform(spawn_loc, rotation)
    self.world.spawn_actor(vehicle_bp, transform)
