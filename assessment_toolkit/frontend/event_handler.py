import time
import PySimpleGUI as sg
#Import CarlaLaunch
from backend.interface import carla_launch as claunch
#Import ROSLaunch
from backend.interface import ros_launch as rlaunch
#Import ROSClose 
from backend.interface import ros_close as rclose
from backend.interface import patch_ros as patchros
import json
CONFIG = json.load(open('./config.json'))

#Handle Object Events and return the action that needs to be taken
def parse_event(window):
    event, values = window.read(timeout=100)
        # keep an animation running so show things are happening

    if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
        pass
        # print('============ Event = ', event, ' ==============')
        # print('-------- Values Dictionary (key=value) --------')
        # for key in values:
        #     print(key, ' = ',values[key])


    if event in (None, 'Exit'):
        print("[LOG] Clicked Exit!")
        return {"event_name":"close_window"}

    ## If Start CALRA Button Clicked
    elif event == '1. Start CARLA':
        print("1. Start CARLA")
      
        ## Launch CARLA & Sleep for 5 seconds.
        claunch.CarlaLaunch(CONFIG['CARLA_SIMULATOR_PATH'])
        time.sleep(1)

    ## If Start ROS Button Clicked
    elif event == '2. Start ROS':
        print("2. Start ROS")
       
        ## Launch CARLA & Sleep for 5 seconds.
        ros = rlaunch.ROSLaunch(CONFIG['CARLA_AUTOWARE_PATH'])
        time.sleep(1)
       

    elif event == '3. Patch ROS':
        print("3. Patch ROS")
       
        ## Launch CARLA & Sleep for 5 seconds.
        patchros.PatchRos()
        time.sleep(1)

    elif event == '4. Start Test':
        #Add Data
        form_data = {}
        for key in values:
            print(key, ' = ',values[key])
            form_data[key] = values[key]

        return {"event_name":"start_scenario_setup", "data":form_data}


    elif event == 'CLOSE ROS':
        #Add Data
        print("CLOSE ROS")
        rclose.ROSClose()
        time.sleep(1)


    elif event == '2D Pose Estimation Has Been Set':
        return {"event_name":"start_scenario_run"}


    elif event == '1. Launch Carla':   
        return {"event_name":"launch_carla"}

    elif event == '2. Launch Carla Autoware':   
        return {"event_name":"launch_carla_autoware"}
  
    #Continue is within the event because multiple continue buttons rendered make Continue, Continue2, Continue3
    elif 'Continue' in event:
        form_data = {}
        for key in values:
            print(key, ' = ',values[key])
            form_data[key] = values[key]
        return {"event_name":"continue", "data":form_data}
    
    elif event == 'Next':
        print('elif event == Next:')

        return {"event_name":"next"}

    elif event == '(CONFIRM) Step(3) is complete':

        print("event_handler.py (CONFIRM) Step(3) is complete");
        return {"event_name":"carla_autoware_docker_container_loaded"}

    elif event == 'Run Patch':
        return {'event_name': 'run_patch'}

    elif event == 'Patch has Finished':
        return {'event_name': 'patch_has_finished'}

    elif '(CONFIRM) RVIZ has loaded' in event:
        print("event_handler.py (CONFIRM) RVIZ has loaded");
        return {'event_name': 'start_scenario_run'}

    elif event == '(CONFIRM) Terminal process has stopped':
        return {'event_name': 'next_metamorphic_test'}

    elif event == 'View Results':
        return {'event_name': 'view_results'}


    return {"event_name":"none"}
        
