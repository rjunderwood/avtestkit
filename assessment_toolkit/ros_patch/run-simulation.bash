!/bin/bash
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town01 spawn_point:='338.761,-230,0.2,0,0,90'
PID=$!
sleep 10s
kill $PID