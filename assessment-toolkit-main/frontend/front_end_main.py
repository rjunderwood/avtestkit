

from cgitb import handler
import PySimpleGUI as sg

from .views import *
from .event_handler import parse_event




class FrontEndMain():

    assessment_toolkit = None
    window = None

    def __init__(self, assessment_toolkit):
        #Set the assessment toolkit
        self.assessment_toolkit = assessment_toolkit   
        

    def make_window(self,theme):
        sg.theme(theme)
        layout = view_container()
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
        window.set_min_size(window.size)
        return window


    def start(self):
        window = self.make_window(sg.theme())
        #Set the window to be accessed later. 
        self.window = window


        # This is an Event Loop 
        while True:
            event = parse_event(self.window)
            if(event["event_name"] =="close_window"):
                #Window Close Event if event_handler.run(window,event,values) RETURNS "close_window"
                break
            elif(event["event_name"] == "start"):
                print(event)
                #Setup the scenario with the inputs
                self.assessment_toolkit.setup_scenario(event["data"])
                #Show the next view
                self.change_view("view_set_2d_pose_estimation")

            #User is saying that they have finished the 2D pose estimate
            elif(event["event_name"] == "next"):
                #Run the ready scenario
                self.assessment_toolkit.run_scenario()
                #Show the next view ( Now simulation is running the user needs to start the ego movement with 2d nav goal RVIS)
                self.change_view("view_set_2d_nav")
            
            else:
                # print(event)
                pass

                

        window.close()
        exit(0)
    
    





    #Change the GUI view
    def change_view(self,target_view):
        print("gui: change_view : ", target_view)

        if(len(target_view) > 0):

            if(target_view == "view_set_2d_pose_estimation"):
                #Set view_set_2d_pose_estimation & other views false
                self.window['view_set_2d_pose_estimation'].update(visible=True)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
            elif(target_view == "view_setup"):
                #Set view_set_2d_pose_estimation & other views false
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=True)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=False)
            elif(target_view == "view_setup"):
                #Set view_set_2d_pose_estimation & other views false
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=True)
                self.window['view_result'].update(visible=False)      
            elif(target_view == "view_result"):
                #Set view_set_2d_pose_estimation & other views false
                self.window['view_set_2d_pose_estimation'].update(visible=False)
                self.window['view_setup'].update(visible=False)
                self.window['view_set_2d_nav'].update(visible=False)
                self.window['view_result'].update(visible=True)        
        
