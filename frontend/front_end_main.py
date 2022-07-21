
from cgitb import handler
import PySimpleGUI as sg

from .views import *
from .event_handler import parse_event


class FrontEndMain():

    assessment_toolkit = None
    window = None
    run_scenario_change = 0
    current_view = ""
    
    #This is a one off variable that controlls after the view_setup_toolkit has
    # had both the " 1. Launch Carla " & "2. Launch Carla Autoware"
    view_setup_toolkit_complete = False

    def __init__(self, assessment_toolkit):
        #Set the assessment toolkit
        self.assessment_toolkit = assessment_toolkit   
        

    def make_window(self,theme):
        sg.theme(theme)
  
        layout = view_container(self)
        window = sg.Window(
            'Assessment Toolkit For Safe Self Driving Cars', 
            layout, 
            grab_anywhere=True, 
            resizable=True, 
            margins=(0,0), 
            use_custom_titlebar=True, 
            finalize=True, 
            keep_on_top=True,
            
            )
        window.TKroot.minsize(400,500)
        # window.set_min_size(window.size)

        return window

    def get_current_scenario_name(self):
        return self.assessment_toolkit.get_current_scenario_name()


    def refresh_window_data():
        self.window.layout = view_container()
        self.change_view(self.current_view)


    def start(self):
        window = self.make_window(sg.theme())
        #Set the window to be accessed later. 
        self.window = window


        # This is an Event Loop 
        while True:       
            

            event = parse_event(self.window)
            

            #Setup Toolkit listener 
            self.handle_setup_toolkit()

            if(event["event_name"] =="close_window"):
                #Window Close Event if event_handler.run(window,event,values) RETURNS "close_window"
                break

            #Launch Carla.
            elif(event["event_name"] == "launch_carla"):
                self.assessment_toolkit.start_carla()

            #Launch Carla Autoware.
            elif(event["event_name"] == "launch_carla_autoware"):
                self.assessment_toolkit.start_carla_autoware()

            elif(event["event_name"] == "start_scenario_setup"):
                
                #Setup the scenario with the inputs
                self.assessment_toolkit.setup_scenario(event["data"])


                
            elif(event["event_name"] == "continue"):


                #Continue from Scenario Setup 
                if self.current_view == "view_setup_scenarios" or self.current_view == "view_setup_scenarios_none":

                    #Setup the scenario with the inputs
                    self.assessment_toolkit.setup_scenarios(event["data"])


            #User is saying that they have finished the 2D pose estimate
            elif(event["event_name"] == "start_scenario_run"):
                
                self.change_view("view_set_2d_nav")
                self.run_scenario_change+=1

            if(self.run_scenario_change > 0):
                print(self.run_scenario_change)
                self.run_scenario_change+=1
                
            if(self.run_scenario_change == 5):
                #Run the ready scenario
                self.assessment_toolkit.run_scenario()
                self.run_scenario_change = 0
        # End while
                

        window.close()
        exit(0)
    
    


    #Setup Toolkit listener 
    def handle_setup_toolkit(self):

        setup_controller = self.assessment_toolkit.get_setup_controller()
        if setup_controller['carla'] == True and setup_controller['carla_autoware'] == True:

            if self.view_setup_toolkit_complete == False:
                self.view_setup_toolkit_complete = True
                self.change_view("view_setup_scenarios")



    #Change the GUI view
    def change_view(self,target_view):
        print("gui: change_view : ", target_view)

        if(len(target_view) > 0):


            if(target_view == "view_setup_toolkit"):
                self.current_view = target_view
                self.window['view_setup_toolkit'].update(visible=True)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_setup_scenarios"):
                self.current_view = target_view                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=True)
                self.window['view_setup_scenarios_none'].update(visible=False) 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
                self.window['view_scenario_starter'].update(visible=False)                
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_setup_scenarios_none"):
                self.current_view = target_view                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=True) 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True





            elif(target_view == "view_set_2d_pose_estimation"):
                self.current_view = target_view               
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=True)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_setup"):
                self.current_view = target_view               
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=True)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_set_2d_nav"):
                self.current_view = target_view                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=True)
                self.window['view_result'].update(visible=False)  
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True    
            elif(target_view == "view_result"):
                self.current_view = target_view                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=True)        
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_scenario_starter"):
                self.current_view = target_view
                #REFRESH VIEW
                self.window.layout = view_container(self)                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)        
                self.window['view_scenario_starter'].update(visible=True)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=False)
                return True
            elif(target_view == "view_scenario_starter_follow_vehicle"):
                self.current_view = target_view
                #REFRESH VIEW
                self.window.layout = view_container(self)                
                self.window['view_setup_toolkit'].update(visible=False)
                self.window['view_setup_scenarios'].update(visible=False)
                self.window['view_setup_scenarios_none'].update(visible=False)                 
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)        
                self.window['view_scenario_starter'].update(visible=False)
                self.window['view_scenario_starter_follow_vehicle'].update(visible=True)
                return True
        
    def set_view_result_data(self, result_data): 
        print('Loading results into the GUI...')
        



