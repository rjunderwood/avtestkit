#!/bin/bash

####################################
##        Start/Goal Pose         ##
####################################

# Create SimulationData folder and EgoCar.csv file
mkdir -p autoware_openplanner_logs/SimulationData
echo 'X,Y,Z,A,C,V,name,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv 
echo '88,-196.7,5,0,196.7,0,0,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
echo '-41,-194.7,0.5,0,0,0,destination_1,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
