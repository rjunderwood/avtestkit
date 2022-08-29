!/bin/bash
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town03 spawn_point:='88,-196.7,5,0,0,180'
PID=$!
sleep 10s
kill $PID