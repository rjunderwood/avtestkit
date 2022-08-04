import json
CONFIG = json.load(open('../../config.json'));
print(CONFIG['CARLA_SIMULATOR_PATH'])