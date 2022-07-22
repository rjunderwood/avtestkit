
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
        window = self.make_window(sg.theme("Reddit"))
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

                print()
             
                
                if self.current_view == "view_scenario_starter_follow_vehicle":
                    self.change_view("view_start_autoware")
                
                   #Continue from Scenario Setup 
                if self.current_view == "view_setup_scenarios" or self.current_view == "view_setup_scenarios_none":

                    #Setup the scenario with the inputs
                    self.assessment_toolkit.setup_scenarios(event["data"])
                    print("#Continue from Scenario Setup")


            #User is saying that they have finished the 2D pose estimate
            elif(event["event_name"] == "start_scenario_run"):
                
                self.change_view("view_set_2d_nav")
                self.run_scenario_change+=1

            #Connect Carla Autoware View docker container has loaded
            elif(event["event_name"] == "carla_autoware_docker_container_loaded"):
                #Time to run the patch on docker and then move to the run scenario phase screen. 
                self.assessment_toolkit.run_ros_patch()

    




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

        available_views = [
            "view_setup_toolkit",
            "view_setup_scenarios",
            "view_setup_scenarios_none",
            "view_set_2d_pose_estimation",
            "view_setup",
            "view_set_2d_pose_estimation",
            "view_setup",
            "view_set_2d_nav",
            "view_result",
            "view_scenario_starter",
            "view_scenario_starter_follow_vehicle",
            "view_start_autoware"
        ]

        if target_view in available_views:
            
            for view in available_views:
                if(view == target_view):
                    self.window[view].update(visible=True)
                    self.current_view = target_view
                else:
                    self.window[view].update(visible=False)
            
            return True
          
       
    def set_view_result_data(self, result_data): 
        print('Loading results into the GUI...')
        



