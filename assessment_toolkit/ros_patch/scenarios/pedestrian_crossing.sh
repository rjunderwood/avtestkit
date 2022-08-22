# #!/bin/bash

# ####################################
# ##        Start/Goal Pose         ##
# ####################################

# Create SimulationData folder and EgoCar.csv file
mkdir -p autoware_openplanner_logs/SimulationData
echo 'X,Y,Z,A,C,V,name,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv 
echo '-60.761, -135.1, 0.2, 0, 0,0,0,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv
echo '190,63,0,0.2,0,0,destination_1,' >> ~/autoware_openplanner_logs/SimulationData/EgoCar.csv