
from concurrent.futures import ProcessPoolExecutor
from tkinter import E
from unittest import result
from .result_data import ResultData
import pathlib
import os
import csv

class ProcessResult():

    #results an array of result_data

    result_data_list = []

    def __init__(self, file_name):

        
        file_path = self.get_file_path(file_name)
        try:
            with open(file_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')          
                for row in csv_reader:
                    self.result_data_list.append(ResultData(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        except Exception:
            print("Result File Not Found")
            print(Exception)

    def get_file_path(self, file_name):
        
        path_string = str(pathlib.Path(__file__).parent.resolve())
        construct_path_string = ""

        for char in path_string:
            if "AV-Tester" in construct_path_string:
                # add the \ 
                construct_path_string+=char
                construct_path_string+=file_name
                return construct_path_string
            construct_path_string+=char



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

    
    