import json
import os
config = json.load(open('config.json'))


#Carla Simulator Path
CARLA_SIMULATOR_PATH = config['CARLA_SIMULATOR_PATH']
#Carla Autoware Path 
CARLA_AUTOWARE_PATH = config['CARLA_AUTOWARE_PATH']
print(CARLA_AUTOWARE_PATH)
print(CARLA_SIMULATOR_PATH)



def setup_patch_files():
    directory = os.getcwd() 

    ros_patch = open('./ros_patch/setup_carla_autoware_docker_container.sh')
    ros_patch_lines = ros_patch.readlines()
    ros_patch.close()
    line_number=1

    ros_patch_new = open('./ros_patch/setup_carla_autoware_docker_container.sh', 'w')
    edit_ros_patch_file=""

    for line in ros_patch_lines:
        if line_number == 18:
            line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ directory +"/ros_patch/patch_files/update_vehicle_model.launch.patch %%:/home/autoware/Documents\n"
        if line_number == 26:
            line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ directory +"/ros_patch/patch_files/update_my_mission_planning.patch %%:/home/autoware/Documents\n"
        if line_number == 34:
            line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ directory +"/ros_patch/create_ego_car_csv.sh %%:/home/autoware/Documents\n"
        if line_number == 52:
            line = "docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp "+ directory +"/ros_patch/run-simulation.bash %%:/home/autoware/Documents\n"
        ros_patch_new.write(line)
        line_number+=1
        

def run_patch_files():
    
