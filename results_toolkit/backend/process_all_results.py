import os

#Get the results data and read into memory. 
#Get the scenarios. Metamorphic tests to measure the data. 
from .process_results import ProcessResult

CWD = os.getcwd()

class ProcessAllResults():
    
    processed_results = []

    def __init__(self):
        pass

    def process_results(self):

        print("CWD")
        print(CWD)
        assessment_toolkit_cwd = CWD[:len(CWD) - 15] + "assessment_toolkit"

        #Get the files 
        result_file_directory = assessment_toolkit_cwd + "/backend/scenario/results/"
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
        print("processed_resultsprocessed_resultsprocessed_resultsprocessed_results   " + scenario_name)
        print(self.processed_results)
        for process_result in self.processed_results:
            if(process_result.get_scenario_name() == scenario_name):
                result.append(process_result)
        print("self.processed_results || " + str(result))
        return result

    
    #Returns the names of the available scenarios that have processed results. 
    def get_all_process_result_available_scenarios(self):
        result = []
        for process_result in self.processed_results:
            if(process_result.get_scenario_name() not in result):
                result.append(process_result.get_scenario_name())
        return result



    #Get a basoc summary of all the scenarios 
    def get_all_process_results_summary(self):
        
        scenario_names = self.get_all_process_result_available_scenarios()
        scenario_summary = []
        for scenario_name in scenario_names:
            scenario_data = self.get_all_process_result_scenario(scenario_name)
            parameters = scenario_data[0].get_metamorphic_test_data()
            total_cases = len(scenario_data)
            failed_cases = 0 
            #Test fails
            for scenario in scenario_data:
                print("scenario.had_collision()scenario.had_collision()scenario.had_collision() "+str(scenario.had_collision()))
                if(scenario.had_collision() or scenario.had_lane_invasion()):
                   
                    failed_cases+=1
            
            scenario_summary.append({
                'scenario':scenario_name,
                'parameters':parameters,
                'failed_cases':failed_cases,
                'total_cases':total_cases
            })
        
        return scenario_summary
              

    #Returns the failure data for a specific scenario | its parameters and values. 
    def get_scenario_failed_data(self, scenario_name):    
        
        print('get_scenario_failed_data()')
        scenario_tests = self.get_all_process_result_scenario(scenario_name)
        
        failed_data = {}
        print("LENGTH scenario_tests" + str(len(scenario_tests)))
        #Set the original parameters names for failed_data
        parameters = scenario_tests[0].get_metamorphic_test_data()
        for parameter in parameters:
            failed_data[parameter] = {}
        
   

        for scenario in scenario_tests:
            scenario.get_metamorphic_test_data()
            #Add the parameters and values for this test. 
            parameters = scenario.get_metamorphic_test_data()
            for parameter in parameters:
                value = parameters[parameter]
                
                #Value is not a key already for the parameter
                if value not in failed_data[parameter]:
                    #Add the value
                    failed_data[parameter][value] = {'total':0, 'percentage':0}

                if scenario.failed():
                    print("SCENARIO FAILED")
                    failed_data[parameter][value]['total']+=1


        #Calculate percentages
        for parameter in failed_data:
            total_fail = 0
            for parameter_value in failed_data[parameter]:
                total_fail+=failed_data[parameter][parameter_value]['total']

            for parameter_value in failed_data[parameter]:
                failed_data[parameter][parameter_value]['percentage'] = failed_data[parameter][parameter_value]['total'] / total_fail


        return failed_data
        