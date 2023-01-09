!/bin/bash
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town03 spawn_point:='2,-180,0.2,0.2,0,90'
PID=$!
sleep 10s
kill $PID