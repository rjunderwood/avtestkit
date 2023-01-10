import os 
from ..util import path_slash
from .result import Result

class Results():
    
    scenario_raw_data_paths = []
    results = []

    def __init__(self, scenario_raw_data_paths):
        self.scenario_raw_data_paths = scenario_raw_data_paths 
        self.process_scenario_raw_data()
    
    
    def process_scenario_raw_data(self):
        for scenario_raw_data_path in self.scenario_raw_data_paths:
            paths = self.construct_scenario_raw_data_paths(scenario_raw_data_path["path"])
            print("\nProcessing : " + scenario_raw_data_path["scenario_name"])
            result = Result(scenario_raw_data_path["scenario_name"], paths) 
            self.results.append(result)
    

    def construct_scenario_raw_data_paths(self, scenario_raw_data_path):
        #Get the directories in scenario_raw_data_path
        paths = {"source":"", "follow_ups":[]}
        for dir in os.listdir(scenario_raw_data_path):
            if dir == "S":
                paths["source"] = scenario_raw_data_path + dir + path_slash()
            elif "omit" in dir:
                #Need to not add certain omitted directories. This is for the pedestrian scenario "child" case specifically
                continue
            else:
                paths["follow_ups"].append({"follow_up_name": dir, "path":scenario_raw_data_path + dir + path_slash()})
        
        return paths
    
    def print_results(self):
        for result in self.results:
            print("\n\n" + result.get_scenario_name())
            print("S")
            self.print_collisions(result.source_data["result_frames"])
            for follow_up in result.follow_up_data:
                print(follow_up["follow_up_name"])
                self.print_collisions(follow_up["result_frames"])

    def print_collisions(self,result_frames):
        for test, frames in result_frames.items():
            had_collision = False
            for result_frame in frames:
                if result_frame.had_collision() and not had_collision:
                    had_collision = True
                    print(test + " :: Collision at time " + str(result_frame.get_time()) + "s")



   
