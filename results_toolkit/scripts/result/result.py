from tqdm import tqdm
from .result_frame import ResultFrame
import os
import threading
from collections import deque
import json
from ..util import path_slash
from ..plots.graph_label import GraphLabel
from ..plots.box_plot import create_box_plot
from ..plots.bar_plot import plot_stacked_bar, plot_bar
from .mann_whitney_u_test import test_mann_whitney
from .cohens_d import test_cohens_d
from .calculate_means import calculate_means
from .calculate_std_devs import calculate_std_devs
import queue
import csv
CWD = os.getcwd()


class Result():

    scenario_name = None
    raw_data_paths = {}
    source_data = []
    follow_up_data = []
    total_processed = 0
    total_to_process = 0
    progress_bar = None

    def __init__(self, scenario_name, raw_data_paths):
        self.scenario_name = scenario_name
        self.raw_data_paths = raw_data_paths
        # self.total_to_process = len(self.raw_data_paths["follow_ups"]) + 1
        print("\nImporting Raw Data...\n")
        self.progress_bar = tqdm(total=len(self.raw_data_paths["follow_ups"]) + 1)

        self.process_source()
        self.process_follow_ups()

    def start_progress_bar(self):
        self.progress_bar = tqdm(total=100)
    
    def get_scenario_name(self):
        return self.scenario_name

    def process_source(self):
        source_raw_data_path = self.raw_data_paths["source"]
        source_processed_data = self.process_test_data(source_raw_data_path)
        self.source_data = deque([{"result_frames": source_processed_data["result_frames"], "test_config":source_processed_data["test_config"]}])
        self.source_data = self.source_data[0]

    def process_follow_ups(self):
        raw_data_follow_ups = self.raw_data_paths["follow_ups"]
        self.follow_up_data = deque()
        for raw_data_follow_up in raw_data_follow_ups:
            follow_up_name = raw_data_follow_up["follow_up_name"]
            follow_up_raw_data_path = raw_data_follow_up["path"]
            follow_up_processed_data = self.process_test_data(
                follow_up_raw_data_path)
            follow_up_data_ = deque([{"follow_up_name": follow_up_name,
                                    "result_frames": follow_up_processed_data["result_frames"], "test_config": follow_up_processed_data["test_config"]}])
            self.follow_up_data.append(follow_up_data_[0])
            
    def get_scenario_test_labels(self):
        labels = ["S: "+self.source_data["test_config"]["plot_label"]]
        
        for follow_up in self.follow_up_data:
            labels.append(follow_up["follow_up_name"] + ": " + follow_up["test_config"]["plot_label"])
        
        if(len(labels) == 1):
            return []
        return labels

    def process_test_data(self, path):
        result_frames = {}
        test_config_queue = queue.Queue()
        for file in os.listdir(path):
            if file.endswith(".txt"):
                result_frames[file] = []
          

        def process_file(file, test_config_queue):
            if file.endswith(".txt"):
                # open the file
                with open(path + file, "r") as f:
                    # read the file
                    lines = f.readlines()
                    # Each line is a result frame
                    for line in lines:
                        # create a result frame object
                        result_frame = ResultFrame(*line.split(","))
                        # append the result frame to the list
                        result_frames[file].append(result_frame)

            elif file.endswith(".json"):
                # open the file
                with open(path + file, "r") as f:
                 
                    # read the file
                    test_config = json.loads(f.read())
                    test_config_queue.put(test_config)
                    
        # create a thread for each file
        threads = [threading.Thread(target=process_file, args=(file,test_config_queue))
                   for file in os.listdir(path)]
        # start the threads
        for thread in threads:
            thread.start()
        # wait for the threads to finish
        for thread in threads:
            thread.join()
        test_config = test_config_queue.get()

        self.progress_bar.update(1)
        if(self.progress_bar.n >= self.progress_bar.total):
            self.progress_bar.close()
        

        return {"result_frames": result_frames, "test_config": test_config}


        #If crash is true, then we want to get the speeds of the crash scenarios
    def test_contains_crash(self,frames):
        for frame in frames:
            if(frame.had_collision()):
                return True
        return False

    ## functions for graph data
    def get_scenario_stopping_distances(self,crash=False):
        stopping_distances = []
        source_frames = self.source_data["result_frames"]
        follow_up_frames = []
        for follow_up in self.follow_up_data:
            follow_up_frames.append(follow_up["result_frames"])
        

        # Last Stopping Distance is for the Pedestrian turn left prior vehicle maneuver, scenario D. 
        def last_stopping_distance(frames):
            velocity = []
            distance = []
            for frame in frames:
                distance.append(float(frame.get_dist_to_actor()))
                velocity_ = float(frame.get_mag_vel())
                velocity.append(velocity_)

            # Set a flag to track whether we are in a 0 cycle
            in_zero_cycle = False

            # Set a variable to store the index of the first 0 in the cycle
            first_zero_index = None

            for i, x in enumerate(velocity):
                if x == 0:
                    if not in_zero_cycle:
                        # We have entered a new 0 cycle
                        in_zero_cycle = True
                        first_zero_index = i
                else:
                    if in_zero_cycle:
                        # We have exited a 0 cycle
                        in_zero_cycle = False

            # Return the distance of the frame at the index of the first 0 in the last 0 cycle
            if first_zero_index is not None:
                return distance[first_zero_index]
            else:
                return None
        
        source_stopping_distance_list = []
        for test, frames in source_frames.items():
            recorded_test_frames=0
            if(not self.test_contains_crash(frames)):
                if self.scenario_name == 'D':
                    source_stopping_distance_list.append(last_stopping_distance(frames))
                else:
                    for frame in frames:
                        velocity = float(frame.get_mag_vel())
                        distance = float(frame.get_dist_to_actor())
                        if(velocity == 0.0):
                            if(recorded_test_frames < 1):
                                recorded_test_frames += 1
                                source_stopping_distance_list.append(distance)
        stopping_distances.append(source_stopping_distance_list)
        

        
        follow_up_num = 0
        for follow_up in follow_up_frames:
            follow_up_stopping_distance_list = []
            for test, frames in follow_up.items():
                recorded_test_frames =0
                if(not self.test_contains_crash(frames)):
                    if self.scenario_name == 'D':
                        follow_up_stopping_distance_list.append(last_stopping_distance(frames))
                    else:
                        for frame in frames:
                            velocity = float(frame.get_mag_vel())
                            distance = float(frame.get_dist_to_actor())
                            if(velocity == 0.0):
                                if(recorded_test_frames < 1):
                                    recorded_test_frames += 1   
                                    follow_up_stopping_distance_list.append(distance)
              
            stopping_distances.append(follow_up_stopping_distance_list)
            follow_up_num += 1

        
        #source stopping distance is the first element in the list
        #follow up stopping distances are the rest of the elements in the list
        source_distance = stopping_distances[0]
        follow_up_distances = stopping_distances[1:]
        mann_whitney_results = []
        cohens_d_results = []
        p_values = []
        for follow_up_distance in follow_up_distances:
            mann_whitney = test_mann_whitney(source_distance,follow_up_distance)
            cohens_d = test_cohens_d(source_distance,follow_up_distance)
            cohens_d_results.append(cohens_d)
            p_values.append(mann_whitney['p_value'])
            mann_whitney_results.append(mann_whitney['result'])
        
        
        #Means 
        means = calculate_means(source_distance,follow_up_distances)
        #Standard Deviations
        std_devs = calculate_std_devs(source_distance,follow_up_distances)

        return {"stopping_distances":stopping_distances, "mann_whitney_results":mann_whitney_results, "cohens_d_results":cohens_d_results, "p_values":p_values, "means":means, "std_devs":std_devs}


    def get_test_stopping_distances(self,result_frames):
        stopping_distances = []
        #Only get one stopping distance frame per test
        for test, frames in result_frames.items():
            stopping_distance_list = []
            for frame in frames:
                distance = float(frame.get_dist_to_actor())
                velocity = float(frame.get_mag_vel())
                if(velocity == 0.0 or distance == 0.0):
                    if(len(stopping_distance_list) < 1):
                        stopping_distance_list.append(distance)
                    # stopping_distance_list.append(distance)
            if(self.test_contains_crash(frames)):
                stopping_distances.append([])
                continue
            stopping_distances.append(stopping_distance_list)
        return stopping_distances
    
    def get_scenario_collision_data(self):
        collisions = []
        passes = []

        source_frames = self.source_data["result_frames"]
        source_passes = 0
        source_collisions = 0
        for test, frames in source_frames.items():
            collision = False
            for frame in frames:
                if(frame.had_collision() and not collision):
                    collision = True
            if(collision):
                source_collisions += 1
            else:
                source_passes += 1
        collisions.append(source_collisions)
        passes.append(source_passes)



        for follow_up in self.follow_up_data:
            follow_up_frames = follow_up["result_frames"]
            follow_up_passes = 0
            follow_up_collisions = 0
            for test, frames in follow_up_frames.items():
                collision = False
                for frame in frames:
                    if(frame.had_collision() and not collision):
                        collision = True
                if(collision):
                    follow_up_collisions += 1
                else:
                    follow_up_passes += 1
            collisions.append(follow_up_collisions)
            passes.append(follow_up_passes)


        #Get the highest number of passes[] and collisions[] sum 
        upper_limit = 0
        for i in range(len(collisions)):
            try:
                if(collisions[i] + passes[i] > upper_limit):
                    upper_limit = collisions[i] + passes[i]
            except:
                pass
          

        
        
        return {"collisions": collisions, "passes": passes, "upper_limit": upper_limit}

    def save_stopping_distance_statistics(self,save_path,means,std_devs,p_values, cohen_d_results):
        with open(save_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["F#","Smean", "Ssd", "Fmean", "Fsd", "Pvalue", "CohenD"])
            for i in range(len(means['follow_ups_mean'])):
                writer.writerow(["F"+str(i+1),means['source_mean'], std_devs['source_std_dev'], means['follow_ups_mean'][i], std_devs['follow_ups_std_dev'][i], p_values[i], cohen_d_results[i]])
            
            

    def plot_stopping_distances(self):

        print("\nPlotting Stopping Distances...\n")
        self.start_progress_bar()
        # Plot the stopping distances of the source and follow up tests
        test_labels = self.get_scenario_test_labels()
        scenario_stopping_distance_data_and_statistics = self.get_scenario_stopping_distances()
        #Save the means, std devs, and p values to a csv file
        save_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}processed{path_slash()}stopping_distance{path_slash()}{self.scenario_name}{path_slash()}statistics.csv"
        self.save_stopping_distance_statistics(save_path,scenario_stopping_distance_data_and_statistics["means"],scenario_stopping_distance_data_and_statistics["std_devs"],scenario_stopping_distance_data_and_statistics["p_values"], scenario_stopping_distance_data_and_statistics["cohens_d_results"])


        scenario_stopping_distance_data =  scenario_stopping_distance_data_and_statistics["stopping_distances"] 
        

        save_plot_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}processed{path_slash()}stopping_distance{path_slash()}{self.scenario_name}{path_slash()}combined.png"
        violations = scenario_stopping_distance_data_and_statistics["mann_whitney_results"]
        create_box_plot(scenario_stopping_distance_data, save_plot_path,GraphLabel('','Scenario','Stopping Distance (m)','',test_labels), violations)
        self.progress_bar.update(33)
    
        # Plot the stopping distances of the source tests only
        test_labels = []
        for i in range(len(self.source_data["result_frames"])):
            test_labels.append(f"{i+1}")
        #test labels is array of 1 to length of self.source_data["result_frames"].keys()

        source_stopping_distances = self.get_test_stopping_distances(self.source_data["result_frames"])
        remove_indexes=[]
        for i, source_stopping_distance_element in enumerate(source_stopping_distances):
            if len(source_stopping_distance_element) == 0:
                remove_indexes.append(i)
        for remove_index in sorted(remove_indexes, reverse=True):
            del source_stopping_distances[remove_index]
            del test_labels[remove_index]

        save_plot_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}processed{path_slash()}stopping_distance{path_slash()}{self.scenario_name}{path_slash()}S.png"
        #flatten 3d array to 2d array source_stopping_distances
        source_stopping_distances = [item for sublist in source_stopping_distances for item in sublist]
        #get the highest value in the array

        if(len(source_stopping_distances) > 0):
            upper_limit = max(source_stopping_distances)
            value = {"upper_limit": upper_limit+5, "values": source_stopping_distances}
            plot_bar(values=value, filesave=save_plot_path,graphlabel=GraphLabel('','Run','Stopping Distance (m)','',test_labels))
        self.progress_bar.update(33)

        # Plot the stopping distances of the follow up tests only
        for follow_up in self.follow_up_data:
            test_labels = []
            for i in range(len(follow_up["result_frames"])):
                test_labels.append(f"{i+1}")
            #test labels is array of 1 to length of follow_up["result_frames"].keys()

            follow_up_stopping_distances = self.get_test_stopping_distances(follow_up["result_frames"])
            remove_indexes=[]
            for i, follow_up_stopping_distance_element in enumerate(follow_up_stopping_distances):
                if len(follow_up_stopping_distance_element) == 0:
                    remove_indexes.append(i)
            for remove_index in sorted(remove_indexes, reverse=True):
                del follow_up_stopping_distances[remove_index]
                del test_labels[remove_index]

            follow_up_name = follow_up["follow_up_name"]
            save_plot_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}processed{path_slash()}stopping_distance{path_slash()}{self.scenario_name}{path_slash()}{follow_up_name}.png"
            #flatten 3d array to 2d array follow_up_stopping_distances
            follow_up_stopping_distances = [item for sublist in follow_up_stopping_distances for item in sublist]      
            #get the highest value in the array
     
            if(len(follow_up_stopping_distances) > 0):
                upper_limit = max(follow_up_stopping_distances)
                value = {"upper_limit": upper_limit+5, "values": follow_up_stopping_distances}
                plot_bar(values=value, filesave=save_plot_path,graphlabel=GraphLabel('','Run','Stopping Distance (m)','',test_labels))
        self.progress_bar.update(34)
        self.progress_bar.close()

    def plot_pass_crash(self):

        print("\nPlotting Pass Crash...\n")
        self.start_progress_bar()
        #Plot a stacked bar plot for the passes and crashes of the source and follow up tests 
        test_labels = self.get_scenario_test_labels()
        scenario_pass_crash_data = self.get_scenario_collision_data()
        save_plot_path = f"{os.path.split(CWD)[0]}{path_slash()}data{path_slash()}processed{path_slash()}pass_crash{path_slash()}{self.scenario_name}{path_slash()}combined.png"
       
        graphlabel = GraphLabel(title='',xlabel='Scenario',ylabel='Runs',legend='legend',xlabels=test_labels)
        plot_stacked_bar(values=scenario_pass_crash_data,graphlabel=graphlabel,legend=('pass', 'collision'),filesave=save_plot_path)
        self.progress_bar.update(100)
        self.progress_bar.close()
    



         
