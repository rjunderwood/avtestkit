
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


    def __init__(self, file_name, scenario_name, scenario_metamorphic_test_number):
        
        print(file_name)
        file_path = CWD + "/backend/scenario/results/" + file_name
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')          
                for row in csv_reader:
                    self.result_data_list.append(ResultData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        except Exception:
            print("Result File Not Found")
            print(Exception)


        self.scenario_name = scenario_name
        self.scenario_metamorphic_test_number = scenario_metamorphic_test_number
        self.import_metamorphic_data()


    def import_metamorphic_data(self):  

        file_path = CWD + "/backend/scenario/metamorphic_tests/" + self.scenario_name + ".json"
        file = open(file_path)  
        file_data = json.loads(file.read())   

        for index,metamorphic_test in enumerate(file_data):
            if index == int(self.scenario_metamorphic_test_number):
                self.scenario_metamorphic_test_data = metamorphic_test['parameters']


 

    def get_result_data(self):
        return self.result_data_list


    def had_collision(self):
        
        for result_data in self.get_result_data():
            if(float(result_data.get_collision()) > 0.0):
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