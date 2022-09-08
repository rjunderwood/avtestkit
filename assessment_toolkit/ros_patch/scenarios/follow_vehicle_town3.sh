#!/bin/bash

####################################
##        Start/Goal Pose         ##
####################################

# Create SimulationData folder and EgoCar.csv file
mkdir -p autoware_openplanner_logs/SimulationData
echo 'X,Y,Z,A,C,V,name,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv 
echo '205,5.47.73,1,0,196.7,0,0,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
echo '160,5.47,1,0,0,0,destination_1,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv