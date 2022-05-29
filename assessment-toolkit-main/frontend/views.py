

from cProfile import label
import PySimpleGUI as sg
import pathlib
import os



def view_container():
    layout = [[
        sg.Column(view_setup(), key='view_setup'),
        sg.Column(view_set_2d_nav(), key='view_set_2d_nav',visible=False),
        sg.Column(view_set_2d_pose_estimation(), key='view_set_2d_pose_estimation',visible=False),
        sg.Column(view_result(), key='view_result',visible=False)
        ]]
  
    return layout


def view_setup():

    layout = [
        [sg.Text('Test Runner', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text('Scenario: ')],
        [sg.Combo(values=("Default", "Follow Vehicle"), default_value='Follow Vehicle',readonly=True, k='scenario', auto_size_text=True, size=(100, 5))],
        [sg.Text('Metrics:')],
        [sg.Text('Speed:'), sg.Input(key='metric_speed'), sg.Text('km/ph')],
        [sg.Text('Distance:'), sg.Spin([i for i in range(1, 4)],initial_value=1, k='metric_distance'), sg.Text('sec')],
        [sg.Button('Start', size=(100, 2))]
    ]
    return layout


def view_set_2d_nav():

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


def view_set_2d_pose_estimation():

    layout = []
    if os.name == 'nt':
        layout = [
        
        [sg.Text('Set 2D Pose', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        #The Image that is shown depends on what scenario is ran #TODO when more scenarios are implemented
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'\img\scenarios\follow_vehicle\2d_pose.png',key='view_set_2d_pose_estimation_follow_vehicle')],
        [sg.Button('Next', size=(100, 2))]
        ]
    else:
        layout = [
        
        [sg.Text('Set 2D Pose', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        #The Image that is shown depends on what scenario is ran #TODO when more scenarios are implemented
        [sg.Image(str(pathlib.Path(__file__).parent.resolve())+r'/img/scenarios/follow_vehicle/2d_pose.png',key='view_set_2d_pose_estimation_follow_vehicle')],
        [sg.Button('Next', size=(100, 2))]
        ]

    return layout


def view_result():
    layout = [
        [sg.Text('Set Result', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
    ]
    return layout
