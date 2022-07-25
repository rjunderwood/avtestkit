#!/bin/bash

###########################
##  Live Docker Updates  ##
###########################

# # COPY AUTOWARE-CONTENTS DIR TO RUNNING DOCKER
# docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp ~/carla-autoware/autoware-contents %%:/home/autoware/autoware-contents

    ##################

# CREATE DOCUMENTS FOLDER IN RUNNING DOCKER
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% mkdir ./Documents

    ##################

# COPY PATCH FILE TO RUNNING DOCKER
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp /home/riley/Desktop/AV-Tester/assessment-toolkit-main/ros_patch/patch_files/update_vehicle_model.launch.patch %%:/home/autoware/Documents

# RUN THE PATCH FILE
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% patch Autoware/install/vehicle_description/share/vehicle_description/launch/vehicle_model.launch ./Documents/update_vehicle_model.launch.patch

    ##################

# COPY PATCH FILE TO RUNNING DOCKER
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp /home/riley/Desktop/AV-Tester/assessment-toolkit-main/ros_patch/patch_files/update_my_mission_planning.patch %%:/home/autoware/Documents

# RUN THE PATCH FILE
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% patch carla-autoware/carla-autoware-agent/agent/launch/my_mission_planning.launch ./Documents/update_my_mission_planning.patch

    ##################

# COPY EGOCAR SCRIPT TO RUNNING DOCKER
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp /home/riley/Desktop/AV-Tester/assessment-toolkit-main/ros_patch/create_ego_car_csv.sh %%:/home/autoware/Documents

# RUN THE EGOCAR SCRIPT
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% bash /home/autoware/Documents/create_ego_car_csv.sh

# MAKE SCRIPT EXECUTABLE
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec %% chmod +x /home/autoware/Documents/create_ego_car_csv.sh

# RUN SCRIPT
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% /home/autoware/Documents/create_ego_car_csv.sh

#COPY THE RUN SIMULATION SCRIPT 
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker cp /home/riley/Desktop/AV-Tester/assessment-toolkit-main/ros_patch/run-simulation.bash %%:/home/autoware/Documents

# # MAKE SCRIPT EXECUTABLE
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec %% chmod +x /home/autoware/Documents/run-simulation.bash


# RUN THE ROSLAUNCH SCRIPT
docker ps | grep -Eo '([0-9]|[a-z]){12}' | xargs -I %% docker exec --user autoware -i %% bash /home/autoware/Documents/run-simulation.bash



