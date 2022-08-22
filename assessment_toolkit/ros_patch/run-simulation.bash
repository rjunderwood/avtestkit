!/bin/bash
roslaunch carla_autoware_agent carla_autoware_agent.launch town:=Town03 spawn_point:='-60.761,-135.1,0.2,0.2,0,0'
PID=$!
sleep 10s
kill $PID
