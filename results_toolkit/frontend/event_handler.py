import time
import PySimpleGUI as sg
#Import CarlaLaunch

import json


#Handle Object Events and return the action that needs to be taken
def parse_event(window):
    event, values = window.read(timeout=100)
        # keep an animation running so show things are happening
    
    if event not in (sg.TIMEOUT_EVENT, sg.WIN_CLOSED):
        pass
    

    if event in (None, 'Exit'):
        return {"event_name":"close_window"}

    elif event == 'results_summary_table':
        print("RESUU")
        print(values)
        print(values['results_summary_table'])
        return {'event_name':'open_result_from_summary_table', 'scenario_index':values['results_summary_table']}
    # elif event == '4. Start Test':
    #     #Add Data
    #     form_data = {}
    #     for key in values:
    #         print(key, ' = ',values[key])
    #         form_data[key] = values[key]

    #     return {"event_name":"start_scenario_setup", "data":form_data}


    elif event == 'follow_vehicle':
        print("FOLLOW")
        return {'event_name': 'open_result','scenario':'follow_vehicle'}



    return {"event_name":"none"}
        
