import PySimpleGUI as sg
#Import CarlaLaunch
from backend.interface import carla_launch as claunch
#Import ROSLaunch
from backend.interface import ros_launch as rlaunch




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
    elif event == 'Start CARLA':
        ## Launch CARLA & Sleep for 5 seconds.
        claunch.CarlaLaunch()
        time.sleep(10)

    ## If Start ROS Button Clicked
    elif event == 'Start ROS':
        ## Launch CARLA & Sleep for 5 seconds.
        rlaunch.ROSLaunch()
        time.sleep(10)

    elif event == 'Start Test':
        #Add Data
        form_data = {}
        for key in values:
            print(key, ' = ',values[key])
            form_data[key] = values[key]

        return {"event_name":"start_scenario_setup", "data":form_data}

    elif event == '2D Pose Estimation Has Been Set':
        return {"event_name":"start_scenario_run"}
        



    return {"event_name":"none"}
        
