import os
import sys
import glob 
import json
CWD = os.getcwd() 

CONFIG = json.load(open('../config.json'));
try:
    sys.path.append(glob.glob(CONFIG['CARLA_SIMULATOR_PATH']+'PythonAPI/carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

#Converts english representation of weather in the /metamorphic_tests to carla.WeatherParameters 


def get_weather_parameters(weather):
    if weather == 'Clear Noon':
        return carla.WeatherParameters.ClearNoon 
    elif weather == 'Cloudy Noon':
        return carla.WeatherParameters.CloudyNoon 
    elif weather == 'Wet Noon':
        return carla.WeatherParameters.WetNoon
    elif weather == 'Wet Cloudy Noon':
        return carla.WeatherParameters.WetCloudyNoon
    elif weather == 'Mid Rain Noon': 
        return carla.WeatherParameters.MidRainyNoon
    elif weather == 'Hard Rain Noon': 
        return carla.WeatherParameters.HardRainNoon
    elif weather == 'Soft Rain Noon':
        return carla.WeatherParameters.SoftRainNoon
    elif weather == 'Clear Sunset':
        return carla.WeatherParameters.ClearSunset
    elif weather == 'Cloudy Sunset':
        return carla.WeatherParameters.CloudySunset
    elif weather == 'Wet Sunset':
        return carla.WeatherParameters.WetSunset
    elif weather == 'Wet Cloudy Sunset':
        return carla.WeatherParameters.WetCloudySunset
    elif weather == 'Mid Rain Sunset':
        return carla.WeatherParameters.MidRainSunset
    elif weather == 'Hard Rain Sunset':
        return carla.WeatherParameters.HardRainSunset
    elif weather == 'Soft Rain Sunset':
        return carla.WeatherParameters.SoftRainSunset
    
