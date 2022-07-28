

from cProfile import label
from tkinter import scrolledtext
import PySimpleGUI as sg
import pathlib
import os
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

font = ("courier 10 pitch", 16)
sg.set_options(font=font)

def view_container(gui):

    layout = [[
    
        sg.Column(view_results_main_menu(gui), key='view_results_main_menu',visible=True),
        sg.Column(view_results_page(gui,'follow_vehicle'), key=('view_results_page_follow_vehicle'),visible=False, scrollable=True, vertical_scroll_only=True),
         sg.Column(view_results_page(gui,'pedestrian_crossing'), key=('view_results_page_pedestrian_crossing'),visible=False, scrollable=True, vertical_scroll_only=True)
        ]]
    


    #NOTE the following causes a weird bug making the view_results_page half the expected size. 
    #Add the available scenario results pages
    # result_data = gui.get_result_data()
    # available_scenarios = result_data.get_all_process_result_available_scenarios()
    # for scenario in available_scenarios:
    #     layout.append([sg.Column(view_results_page(gui,scenario), key=('view_results_page_'+scenario),visible=False, scrollable=True, vertical_scroll_only=True)])

    return layout


def view_results_main_menu(gui):
    
    headings = ["Scenario", "Parameters", "Failed Cases", "Total Cases"]

    scenario_summary = gui.get_result_data().get_all_process_results_summary()

    scenario_summary_table_data = []
    for scenario in scenario_summary:
        scenario_summary_table_data.append([scenario['scenario'],len(scenario['parameters']),scenario['failed_cases'],scenario['total_cases']])
    
    layout = [
        [sg.Text('Assessment Toolkit Results', size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text(' ', size=(100, 1))],
        [sg.Text('Summary of Results', size=(100, 1))],
        [sg.Text(' ', size=(100, 1))],

        [sg.Table(values=scenario_summary_table_data, headings=headings, max_col_width=25,
                    auto_size_columns=True,
                    # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                    
                    justification='center',
              
                    alternating_row_color='lightblue',
                    key='results_summary_table',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only=False,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='Results Summary Table')],

    ]
    
    return layout









def view_results_page(gui,scenario):
    
    scenario_result = gui.get_result_data().get_all_process_result_scenario(scenario)

 
    #Add the metamorphic tests of this scenario into the view
    #count the passes and fails. 
    test_fail = 0
    test_pass = 0
    for metamorphic_scenario in scenario_result:
        if(metamorphic_scenario.had_collision() or metamorphic_scenario.had_lane_invasion()):
            test_fail+=1
        else:
            test_pass+=1
  


    #Prepare the Failed Data table. 
    failed_data = gui.get_result_data().get_scenario_failed_data(scenario)

    headings = ["Parameter", "Value", "Failed Tests", "%"]
    summary_of_parameters_failed=[]
    for parameter in failed_data:
        value_counter=0
        for parameter_value in failed_data[parameter]:
            #Only add the name of parameter for the first one in the table
            if(value_counter == 0):
                summary_of_parameters_failed.append([parameter, parameter_value, failed_data[parameter][parameter_value]['total'],failed_data[parameter][parameter_value]['percentage']])
            else:
                summary_of_parameters_failed.append(['', parameter_value, failed_data[parameter][parameter_value]['total'],failed_data[parameter][parameter_value]['percentage']])
            value_counter+=1

    #Creat the summary of parameters of failed tests for this scenario 
    layout = [
        [sg.Text(scenario + " : results", size=(100, 1), justification='center', font=("Helvetica", 16), relief=sg.RELIEF_RIDGE)],
        [sg.Text('\n\n', size=(100, 1))],
        [sg.Text('Pass :: '+str(test_pass), size=(100, 1))],
        [sg.Text('Fail :: '+str(test_fail), size=(100, 1))],
        [sg.Table(values=summary_of_parameters_failed, headings=headings, max_col_width=25,
                    auto_size_columns=True,
                    # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                    
                    justification='center',
              
                    alternating_row_color='lightblue',
                    # key='results_summary_table',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only=False,
                    # enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='Results Summary Table')],
        [sg.Canvas(size=(1000,1000), key="-CANVAS-")]
    ]

    return layout


def create_plot():
    year = [2021,2020,2022,2020]
    unemployment_rate = [9,8,2,2.5]
    plt.plot(year, unemployment_rate, color='blue', marker='o')
    plt.title("Unemployment Rate vs Year", fontsize=14) 
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Unemployment Rate', fontsize=14)
    plt.grid(True)
    return plt.gcf()

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg