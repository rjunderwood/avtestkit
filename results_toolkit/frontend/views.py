

from cProfile import label
import PySimpleGUI as sg
import pathlib
import os

font = ("courier 10 pitch", 16)
sg.set_options(font=font)

def view_container(gui):
    layout = [[
        #sg.Column(view_setup(gui), key='view_setup'),
        sg.Column(view_results_main_menu(gui), key='view_results_main_menu',visible=True),
        ]]
  
    return layout


def view_results_main_menu(gui):

    layout = [
        [sg.Text('Assessment Toolkit Results', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],

    ]
    return layout

