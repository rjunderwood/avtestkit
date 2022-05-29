
import glob
import os
import sys
import random 
import time
import argparse
import math

# try:
#     sys.path.append(glob.glob('/home/luuquanghung/CARLA_AUTOWARE/PythonAPI/carla/dist/carla-0.9.10-py3.7-linux-x86_64.egg'))
# except IndexError:
#     print("Error finding Carla .egg file")
#     pass

import carla 
import time




client = carla.Client('localhost', 2000)
client.set_timeout(2.0)




client.start_recorder("/home/luuquanghung/SDC_ASSESSMENT_TOOLKIT/recordings/recording01.log")



now = time.time()
future = now + 10

while time.time() < future:
    # do stuff
    client.stop_recorder()
    pass





