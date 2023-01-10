#!/bin/bash

####################################
##        Start/Goal Pose         ##
####################################

# Create SimulationData folder and EgoCar.csv file
mkdir -p autoware_openplanner_logs/SimulationData
echo 'X,Y,Z,A,C,V,name,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv 
echo '338.761,-320.678,0.2,1.58954,0,0,0,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
echo '339.013,-209.597,0,1.58954,0,0,destination_1,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
