!/bin/bash
# #FOLLOW VEHICLE
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:='338.761,-320.678,0.2,0,0,90'

# #PEDESTRIAN CROSSING
# roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town03 spawn_point:='105,63,2.94,0.2,0,0,90'
# PID=$!

sleep 10s
kill $PID


#!/bin/bash
#roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town03 spawn_point:='105,63,0.2,0,0,90'
#PID=$!

#sleep 10s
#kill $PID