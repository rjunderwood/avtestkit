

from cProfile import label
import PySimpleGUI as sg
import pathlib
import os

font = ("courier 10 pitch", 16)
sg.set_options(font=font)

def view_container(gui):
    layout = [[
        #sg.Column(view_setup(gui), key='view_setup'),
        sg.Column(view_setup_toolkit(gui), key='view_setup_toolkit',visible=True),
        sg.Column(view_setup_scenarios(gui), key='view_setup_scenarios',visible=False),
        sg.Column(view_setup_scenarios_none(gui), key='view_setup_scenarios_none',visible=False),
        sg.Column(view_set_2d_nav(gui), key='view_set_2d_nav',visible=False),
        sg.Column(view_set_2d_pose_estimation(gui), key='view_set_2d_pose_estimation',visible=False),
        sg.Column(view_result(gui), key='view_result',visible=False),
        sg.Column(view_setup(gui), key='view_setup',visible=False),
        

        #Scenario Stuff 
        sg.Column(view_scenario_starter(gui), key='view_scenario_starter',visible=False),
        sg.Column(view_scenario_starter_follow_vehicle(gui), key='view_scenario_starter_follow_vehicle',visible=False),
        sg.Column(view_start_autoware(gui), key='view_start_autoware',visible=False),
        sg.Column(view_patch_autoware(gui), key='view_patch_autoware',visible=False),
        sg.Column(view_patch_autoware_finished(gui), key='view_patch_autoware_finished',visible=False),
        sg.Column(view_metamorphic_test_state_page(gui), key='view_metamorphic_test_state_page',visible=False),
        sg.Column(view_test_is_running(gui), key='view_test_is_running',visible=False),
        sg.Column(view_next_metamorphic(gui), key='view_next_metamorphic',visible=False),
        sg.Column(view_loading_next_scenario(gui), key='view_loading_next_scenario',visible=False),
        sg.Column(view_all_scenario_complete(gui), key='view_all_scenario_complete',visible=False),
        
        ]]
  
    return layout


def view_setup(gui):

    layout = [
        [sg.Text('Test Runner', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Scenario: ')],
        [sg.Combo(values=("Default", "Follow Vehicle"), default_value='Follow Vehicle',readonly=True, k='scenario', auto_size_text=True, size=(100, 5))],
        [sg.Text('Metrics:')],
        [sg.Text('Speed:'), sg.Input(key='metric_speed'), sg.Text('km/ph')],
        [sg.Text('Distance:'), sg.Spin([i for i in range(1, 4)],initial_value=1, k='metric_distance'), sg.Text('sec')],
        [sg.Button('1. Start CARLA', size=(100, 2))],
        [sg.Button('2. Start ROS', size=(100, 2))],
        [sg.Button('3. Patch ROS', size=(100, 2))],
        [sg.Button('4. Start Test', size=(100, 2))],
        [sg.Button('CLOSE ROS', size=(100, 2))]
    ]
    return layout


def view_set_2d_nav(gui):

    layout = []
    if os.name == 'nt':
        layout = [
            [sg.Text('Set 2D Nav', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)], 
            [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'\img\scenarios\follow_vehicle\2d_nav.png')]
        ]
    else:
        layout = [
            [sg.Text('Set 2D Nav', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)], 
            [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/scenarios/follow_vehicle/2d_nav.png')]
        ]


    return layout


def view_set_2d_pose_estimation(gui):

    layout = []
    if os.name == 'nt':
        layout = [
        
        [sg.Text('Set 2D Pose', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        #The Image that is shown depends on what scenario is ran #TODO when more scenarios are implemented
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'\img\scenarios\follow_vehicle\2d_pose.png',key='view_set_2d_pose_estimation_follow_vehicle')],
        [sg.Button('2D Pose Estimation Has Been Set', size=(100, 2))]
        ]
    else:
        layout = [
        
        [sg.Text('Set 2D Pose', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        #The Image that is shown depends on what scenario is ran #TODO when more scenarios are implemented
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/scenarios/follow_vehicle/2d_pose.png',key='view_set_2d_pose_estimation_follow_vehicle')],
        [sg.Button('2D Pose Estimation Has Been Set', size=(100, 2))]
        ]

    return layout


def view_result(gui):
    layout = [
        [sg.Text('Set Result', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
    ]
    return layout


def view_setup_toolkit(gui):
    layout = [
        [sg.Text('Assessment Toolkit Setup', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
         [sg.Text("\n\n")],
        [sg.Button('1. Launch Carla', size=(100, 2))],
                 [sg.Text("\n")],
        [sg.Button('2. Launch Carla Autoware', size=(100, 2))],
        [sg.Text('\n\nNOTE:\nThe \'Carla Terminal\' and \'Carla Autoware Terminal\' both will be interacted with throughout running the scenario tests.\n\nPlease read the INSTRUCTIONS of each terminal window and arange them on screen so that they are easily accessible', font=("courier 10 pitch", 14))],
    ]
    return layout


def view_setup_scenarios(gui):
    layout = [
        [sg.Text('Scenarios Setup', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        
        [sg.Text('Select Scenarios')],
        # [sg.Combo(values=("Select","All","Follow Vehicle","Pedestrian Crossing Road"), default_value='Select', key='scenario_selector', auto_size_text=True, size=(50, 5))],


        [sg.Checkbox('Follow Vehicle', default=False, key='scenario_check_follow_vehicle')],
        [sg.Checkbox('Pedestrian Crossing Road', default=False, key='scenario_check_pedestrian_crossing_road')],
        [sg.Text('\n')],
        [sg.Button('Continue', size=(100, 2))],
    ]
    return layout

def view_setup_scenarios_none(gui):
    layout = [
        [sg.Text('Scenarios Setup', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        
        [sg.Text('Select Scenarios')],
        # [sg.Combo(values=("Select","All","Follow Vehicle","Pedestrian Crossing Road"), default_value='Select', key='scenario_selector', auto_size_text=True, size=(50, 5))],


        [sg.Checkbox('Follow Vehicle', default=False, key='scenario_check_follow_vehicle')],
        [sg.Checkbox('Pedestrian Crossing Road', default=False, key='scenario_check_pedestrian_crossing_road')],
        [sg.Text('** You need to select a minimum of 1 Scenario')],
        [sg.Text('\n')],
        [sg.Button('Continue', size=(100, 2))],
    ]
    return layout






#Scenario Starter Views

def view_scenario_starter(gui):
    scenario_name = gui.get_current_scenario_name()
    print(" view_scenario_starter | " + scenario_name)
    title = "Start Scenario : " + scenario_name
    layout = [
        [sg.Text(title, size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Button('Next', size=(100, 2))],
    ]
    return layout    

def view_scenario_starter_follow_vehicle(gui):
    scenario_name = gui.get_current_scenario_name()
    layout = [
        [sg.Text('Start Scenario', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("\nFollow Vehicle\n")],
        [sg.Button('Continue', size=(100, 2))],
    ]
    return layout   


def view_scenario_launch_carla_autoware(gui):
    scenario_name = gui.get_current_scenario_name()
    layout = [
        [sg.Text('Start Scenario : Follow Vehicle' + scenario_name, size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Button('Next', size=(100, 2))],
    ]
    return layout   



def view_start_autoware(gui):
   

    layout = [
        [sg.Text('Connect Carla Autoware', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("Step (1)")],
        [sg.Text("START CARLA: Carla Terminal\n")],
        [sg.Text("Step (2)")],
        [sg.Text("START DOCKER: Carla Autoware Terminal\n")],
        # [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/carla-autoware-terminal.png')],
        # [sg.Text('\nENTER COMMAND:\n\nsudo ./run.sh\n\n')],

        [sg.Text("Step (3)")],
        [sg.Text("Wait for the docker container to load in : Carla Autoware Terminal.\n")],
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/carla_autoware_docker_loaded.png')],
        [sg.Text("")],
        [sg.Button('(CONFIRM) Step(3) is complete', size=(100, 2))],
        [sg.Text('Warning. Do not click button above until docker has loaded (will cause errors)', font=("courier 10 pitch", 14))],
    ]
    return layout   


def view_patch_autoware(gui):
    
    layout = [
        [sg.Text('Setup Carla Autoware', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("")],
        [sg.Text("Scenario Patch for Carla Autoware.\n\nA new terminal that will require you to enter [sudo] password\n")],
        [sg.Button('Run Patch', size=(100, 2))],
        [sg.Text("")],
   
    ]
    return layout   

def view_patch_autoware_finished(gui):
    
    layout = [
        [sg.Text('Setup Carla Autoware', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("")],
        [sg.Text("Scenario Patch for Carla Autoware.\n\nA new terminal that will require you to enter [sudo] password\n")],
        [sg.Button('Run Patch', size=(100, 2))],
        [sg.Text("\n\n")],
        [sg.Button('Patch has Finished', size=(100, 2))]
    ]
    return layout   




def view_start_simulation(gui): 
    
    layout = [
        [sg.Text('Setup Carla Autoware', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("")],
        [sg.Text("Scenario Patch for Carla Autoware.\n\nA new terminal that will require you to enter [sudo] password\n")],
        [sg.Button('Run Patch', size=(100, 2))],
        [sg.Text("\n\n")],
        [sg.Button('Patch has Finished', size=(100, 2))]
    ]
    return layout   




def view_metamorphic_test_state_page(gui):

    layout = [
        [sg.Text('Scenario', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("Step (1)")],
        [sg.Text("START SIMULATION: Carla Autoware Terminal\n")],
        # [sg.Text("In the 'Carla Autoware' terminal")],
        # [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/carla_autoware_docker_loaded.png')],
        # [sg.Text("ENTER COMMAND:\n\n./Documents/run-simulation.sh\n\n\n")],    
        [sg.Text("Step (2)")],
        [sg.Text("Wait for 'RVIS' Window to load.\n")],
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/rvis-launch.png')],
        [sg.Text("")],
        [sg.Text("If the RVIS loads with errors or does not load within 1 minute", font=("courier 10 pitch", 12))],
        [sg.Text("RESTART SIMULATION: Carla Autoware Terminal\n")],
        [sg.Button('(CONFIRM) RVIZ has loaded', size=(100, 2))],
    ]
    return layout   


def view_test_is_running(gui):

    layout = [
           [sg.Text('Scenario', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("\n\n\n\nScenario running...",justification='center')],

    ]
    return layout   



def view_next_metamorphic(gui):
    layout = [
        [sg.Text('Setup for Next Metamorphic Test', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("\n\n")],
        [sg.Text("The next metamorphic test for this scenario will be run.")],
        [sg.Text("\nBefore continuing you must:\n\nSTOP CARLA: Carla Terminal")],
        # [sg.Text("\n\nKEYPRESS: Control+C\n\n\n")],    
        # [sg.Text("Step (2)")],
        # [sg.Text("Wait for terminal to stop process.\n")],
        # [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/carla_autoware_docker_loaded.png')],
        # [sg.Text("")],
    
        [sg.Button('Continue', size=(100, 2))],
    ]
    return layout



def view_loading_next_scenario(gui):

    layout = [
        [sg.Text('Changing Scenario', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("\n\n\n\nLoading Next Scenario...",justification='center')],
        

    ]
    return layout   

def view_all_scenario_complete(gui):

    layout = [
           [sg.Text('Scenario Complete', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text("\n\n\nAll scenarios and tests complete.",justification='center')],
         [sg.Button('View Results', size=(100, 2))],

    ]
    return layout   


