import PySimpleGUI as sg




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
        
