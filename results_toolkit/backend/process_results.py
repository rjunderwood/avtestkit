
from concurrent.futures import ProcessPoolExecutor
from tkinter import E
from unittest import result
from .result_data import ResultData
import pathlib
import os
import csv
import json
CWD = os.getcwd()

 
class ProcessResult():

    #results an array of result_data
    scenario_name=None
    scenario_metamorphic_test_number=None
    scenario_metamorphic_test_data=None
    result_data_list = []
    from_file = ""

    def __init__(self, file_name, scenario_name, scenario_metamorphic_test_number):
        print("ProcessResult ___init___ "+file_name)
        print(file_name)
        self.from_file = file_name
        assessment_toolkit_cwd = CWD[:len(CWD) - 15] + "assessment_toolkit"
        file_path = assessment_toolkit_cwd + "/backend/scenario/results/" + file_name
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')          
                csv_row_count = 0
                print("NUMBER OF CSV ROWS ")
               
                for row in csv_reader:
                    self.result_data_list.append(ResultData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
                    csv_row_count+=1 
                 
              
            csv_file.close()
        except Exception:
            print("Result File Not Found")
            print(Exception)


        self.scenario_name = scenario_name
        self.scenario_metamorphic_test_number = scenario_metamorphic_test_number
        self.import_metamorphic_data()


    def import_metamorphic_data(self):  

        assessment_toolkit_cwd = CWD[:len(CWD) - 15] + "assessment_toolkit"
        file_path = assessment_toolkit_cwd + "/backend/scenario/metamorphic_tests/" + self.scenario_name + ".json"
        file = open(file_path)  
        file_data = json.loads(file.read())   

        for index,metamorphic_test in enumerate(file_data):
            if index == int(self.scenario_metamorphic_test_number):
                self.scenario_metamorphic_test_data = metamorphic_test['parameters']


 

    def get_result_data(self):
        return self.result_data_list


    def failed(self):
        return self.had_collision() or self.had_lane_invasion()

    def had_collision(self):
        line_count = 0 
        
        for result_data in self.result_data_list:
            line_count+=1
  
            if(float(result_data.get_collision()) > 0):
                #print("RESULT COLLISION ::: " + str(line_count) + " " + result_data.get_collision() + self.scenario_name + str(self.scenario_metamorphic_test_number) + "  "+self.from_file)
                return True
      
        return False
    
    def had_lane_invasion(self):
        for result_data in self.get_result_data():
            if(float(result_data.get_lane_invasion()) > 0.0):
                return True
        return False

    def get_metamorphic_test_data(self):
        return self.scenario_metamorphic_test_data
    
    def get_scenario_name(self):
        return self.scenario_name