import os

#Get the results data and read into memory. 
#Get the scenarios. Metamorphic tests to measure the data. 
from backend.util.results.process_results import ProcessResult

CWD = os.getcwd()

class ProcessAllResults():
    
    processed_results = []

    def __init__(self):
        pass

    def process_results(self):
        
        #Get the files 
        result_file_directory = CWD + "/backend/scenario/results/"
        for filename in os.listdir(result_file_directory):
            f = os.path.join(result_file_directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                
                scenario_info = self.process_file_name(filename)
                self.processed_results.append(ProcessResult(filename,scenario_info['scenario_name'],scenario_info['test_number']))
                #print(result_file.read())


    #returns the name of the scenario from the file name
    def process_file_name(self, filename):
        filename = filename.replace(".txt","")

        found_last_underscore = False
        end_char_tracker = ''
        for c in reversed(filename):
            if found_last_underscore == False:
                if c == '_':
                    found_last_underscore = True
                end_char_tracker = end_char_tracker+c

        scenario_name = filename.replace(end_char_tracker[::-1], "")
        test_number = end_char_tracker.replace("_", "")
        return {"scenario_name":scenario_name, "test_number":test_number}


    def get_all_process_result_data(self):
        return self.processed_results

    #Returns the ProcessResult objects for given *scenario
    def get_all_process_result_scenario(self, scenario_name):
        result = []
        for process_result in self.processed_results:
            if(process_result.get_scenario_name() == scenario_name):
                result.append(process_result)
        return result

    
    #Returns the names of the available scenarios that have processed results. 
    def get_all_process_result_available_scenarios(self):
        result = []
        for process_result in self.processed_results:
            if(process_result.get_scenario_name() not in result):
                result.append(process_result.get_scenario_name())
        return result


result_processor = ProcessAllResults()
result_processor.process_results()

for result in result_processor.get_all_process_result_available_scenarios():
    print(result)

