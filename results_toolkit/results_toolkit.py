
from scripts.result.results import Results
from scripts.util import path_slash
import os
CWD = os.getcwd()


def process_raw_data(target_scenarios):
    raw_data_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}raw{path_slash()}"
    raw_data_scenario_directory_paths = []
    for scenario in target_scenarios:
        raw_data_scenario_directory_paths.append({"scenario_name": scenario, "path": f"{raw_data_path}{scenario}{path_slash()}"})
    return Results(raw_data_scenario_directory_paths)


if __name__ == "__main__":
    target_scenarios = ["D"]
    results = process_raw_data(target_scenarios)
    for result in results.results:
        #Plotting 
        result.plot_stopping_distances()
        result.plot_pass_crash()
     
