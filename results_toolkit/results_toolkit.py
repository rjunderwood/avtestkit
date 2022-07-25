#from subprocess import call
import json
import time


## Frontend
#Import the front end
from frontend.front_end_main import FrontEndMain




class ResultsToolkit:

    current_scenario = None
    gui = None

    def __init__(self):
        #Start GUI
        gui = FrontEndMain(self)
        #Save GUI
        self.gui = gui
        #start the gui
        self.gui.start()
    


    

if __name__ == '__main__':
    
    assessment_toolkit = ResultsToolkit()

   


    


