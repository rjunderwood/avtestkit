
from cgitb import handler
import PySimpleGUI as sg
import base64
import subprocess
from .views import *
from .event_handler import parse_event

CWD = os.getcwd()

class FrontEndMain():

    assessment_toolkit = None
    window = None
    run_scenario_change = 0
    current_view = ""

    run_scenario_next_frame = False
    
    #This is a one off variable that controlls after the view_setup_toolkit has
    # had both the " 1. Launch Carla " & "2. Launch Carla Autoware"
    view_setup_toolkit_complete = False

    def __init__(self, assessment_toolkit):
        #Set the assessment toolkit
        self.assessment_toolkit = assessment_toolkit   
        

    def make_window(self,theme):
        sg.theme(theme)
  
        layout = view_container(self)

        directory = os.getcwd() 
        print("directory cwd :: " + directory)
        icon=base64.b64encode(open(directory+"/frontend/img/app-icon.png", 'rb').read())
        window = sg.Window(
            'Assessment Toolkit For Safe Self Driving Cars', 
            layout, 
            # grab_anywhere=True, 
            resizable=True, 
            margins=(0,0), 
            # use_custom_titlebar=True, 
            # min_size=(200,300),
            finalize=True, 
            keep_on_top=False,
            icon=icon
            )
       
        window.TKroot.minsize(400,900)
        # window.set_min_size(window.size)
        
        return window

    def get_current_scenario_name(self):
        return self.assessment_toolkit.get_current_scenario_name()

    def get_current_view(self):
        return self.current_view

    def refresh_window_data(self):
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


            if self.run_scenario_next_frame:
                self.run_scenario_next_frame = False
                self.assessment_toolkit.run_scenario()


                
            if(event["event_name"] =="close_window"):
                #Window Close Event if event_handler.run(window,event,values) RETURNS "close_window"
                break

            #Launch Carla.
            elif(event["event_name"] == "launch_carla"):
                self.assessment_toolkit.start_carla()

            #Launch Carla Autoware.
            elif(event["event_name"] == "launch_carla_autoware"):
                self.assessment_toolkit.start_carla_autoware()



                
            elif(event["event_name"] == "continue"):

              
                if self.current_view == "view_scenario_starter_follow_vehicle":
                    self.change_view("view_start_autoware")    

                if self.current_view == "view_scenario_starter_follow_vehicle_town3":
                    self.change_view("view_start_autoware")             
                
                if self.current_view == "view_scenario_starter_pedestrian_crossing":
                    self.change_view("view_start_autoware")

                if self.current_view == "view_scenario_starter_pedestrian_crossing_prior_vehicle_manouver":
                    self.change_view("view_start_autoware")

                if self.current_view == "view_scenario_starter_red_light":
                    self.change_view("view_start_autoware")

                if self.current_view == "view_scenario_starter_intersection_left_turn":
                    self.change_view("view_start_autoware")
                
                   #Continue from Scenario Setup 
                if self.current_view == "view_setup_scenarios":

                    #Setup the scenario with the inputs
                    self.assessment_toolkit.setup_scenarios(event["data"])
                    print("#Continue from Scenario Setup")


                if self.current_view == "view_setup_scenarios_none":
                    #Setup the scenario with the inputs
                    self.assessment_toolkit.setup_scenarios(event["data"])
                    print("#Continue from Scenario Setup")


                if self.current_view == 'view_next_metamorphic':
                    self.change_view("view_scenario_starter_"+ self.assessment_toolkit.get_current_scenario_name())
      
            elif(event["event_name"] == "start_scenario_run"):
                self.change_view("view_test_is_running")
                #On the next frame the run scenario needs to run. This needs to be done so that the system renders the next view_test_is_running before entering the run_scenario() while loop
                #
                self.run_scenario_next_frame = True
            
            
            



            #Connect Carla Autoware View docker container has loaded
            elif(event["event_name"] == "carla_autoware_docker_container_loaded"):
                # #Time to run the patch on docker and then move to the run scenario phase screen. 
                self.change_view("view_patch_autoware")


            #Run the patch on the docker container
            elif(event['event_name'] == 'run_patch'):
                
                self.assessment_toolkit.run_ros_patch()
                #Change view
                self.change_view("view_patch_autoware_finished")
            
            #Patch has finished. Redirect to the retamorphic text page
            elif(event['event_name'] == 'patch_has_finished'):

                self.change_view("view_metamorphic_test_state_page_"+self.get_current_scenario_name())


            elif(event['event_name'] == 'next_metamorphic_test'):
                #Go to next metamorphic test page
                self.change_view("view_metamorphic_test_state_page_"+self.get_current_scenario_name())

            
            elif(event['event_name'] == 'view_results'):
                #Open the results toolkit
                print(CWD)
                
                results_toolkit_file_location = self.get_results_toolkit_location()
                print(results_toolkit_file_location)
                subprocess.call('python3 results_toolkit.py', shell=True, cwd=results_toolkit_file_location)
                # not sure what the deal here is,  but seems to work after hardcoding the wd:
                #subprocess.call(['python results_toolkit.py'], cwd=results_toolkit_file_location)


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
            "view_result",
            "view_scenario_starter",
            "view_scenario_starter_follow_vehicle",
             "view_scenario_starter_follow_vehicle_town3",
            "view_scenario_starter_pedestrian_crossing",
            "view_scenario_starter_pedestrian_crossing_prior_vehicle_manouver",
            "view_scenario_starter_red_light",
            "view_scenario_starter_intersection_left_turn",
            "view_start_autoware",
            "view_patch_autoware",
            "view_patch_autoware_finished",
            "view_metamorphic_test_state_page_follow_vehicle",
            "view_metamorphic_test_state_page_follow_vehicle_town3",
            "view_metamorphic_test_state_page_pedestrian_crossing",
             "view_metamorphic_test_state_page_pedestrian_crossing_prior_vehicle_manouver",
            "view_metamorphic_test_state_page_red_light",
            "view_metamorphic_test_state_page_intersection_left_turn",
            "view_test_is_running",
            "view_next_metamorphic",
            "view_loading_next_scenario",
            "view_all_scenario_complete"
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
        



    def get_results_toolkit_location(self):
        base = CWD

        location_of_last_slash = 0
        for index,char in enumerate(base):
            if(char == '/'):
                location_of_last_slash = index
        start = location_of_last_slash
        stop = len(base) - 1
        # Remove charactes from index 5 to 10
        if len(base) > stop :
            base = base[0: start:] + base[stop + 1::]

        location = base + '/results_toolkit/'
        return location