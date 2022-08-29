#from subprocess import call
import json
import time


## Frontend
#Import the front end
# from .frontend.front_end_main import FrontEndMain
# from .backend.process_all_results import ProcessAllResults

from backend.process_all_results import ProcessAllResults
from frontend.front_end_main import FrontEndMain

class ResultsToolkit:

    current_scenario = None
    gui = None
    processed_results = ProcessAllResults()

    def __init__(self):
  
        self.main()
        print("START")
        #Start GUI
        gui = FrontEndMain(self, self.processed_results)
        
        #Save GUI
        self.gui = gui
        #start the gui
        self.gui.start()
       

        # for result in result_processor.get_all_process_result_available_scenarios():
        #     print(result)
     


    def main(self):
        
        self.processed_results.process_results()

        scenario_names = self.processed_results.get_all_process_result_available_scenarios()
   
        for scenario in scenario_names: 
            print(scenario)



    

if __name__ == '__main__':
    
    assessment_toolkit = ResultsToolkit()

   


    


