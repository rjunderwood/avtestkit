import glob 
import os
import sys
import random
import time
import argparse
import math


import carla

import util #import utility file

X = -2.1
Y = 120
Z = 0.2

PITCH = 0
YAW = 90
ROLL = 0 

EGO_VEHICLE_NAME = 'ego_vehicle'

TRIGGER_DIST = 25 
VEHICLE_MODEL = 'vehicle.toyota.prius'

#Setup the spectator camera

SPEC_CAM_X = 25
SPEC_CAM_Y = 120 
SPEC_CAM_Z = 120
SPEC_CAM_PITCH = -90
SPEC_CAM_YAW = 0
SPEC_CAM_ROLL = 0 


SPAWNED_VEHICLE_ROLENAME = 'stationary_vehicle'

LEAD_VEHICLE_VELOCITY = 3



def main(args):

    try:
        