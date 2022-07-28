
#TODO when not in development change from .mock_follow_vehicle => .follow_vehicle

#Can only be imported on the system with carla. 
from .follow_vehicle import ScenarioFollowVehicle
from .pedestrian_crossing import ScenarioPedestrianCrossing
#Import a mock scenario 
#from .mock_follow_vehicle import ScenarioFollowVehicle

class Scenario: 
    

    #A Object on the specific scenario eg. FollowVehicle
    scenario_runner = None
    scenario_name = None
    scenario_data = None


    def __init__(self, scenario_name, scenario_params):
        self.scenario_name = scenario_name
        #Set the Scenario 
        if(scenario_name == 'follow_vehicle'):
            self.scenario_runner = ScenarioFollowVehicle()
        if(scenario_name == 'pedestrian_crossing'):
            self.scenario_runner = ScenarioPedestrianCrossing()
        
        #TODO scenario_params (These are the metrics that were entered by the user of the GUI)


    def run(self):
        

        #Run the scenario
        self.scenario_runner.run()


    
    def get_scenario_name(self):
        return self.scenario_name


    #Checks to see if scenario is finished. This gets called from the assessment_toolkit.py
    def is_scenario_finished(self):
        return self.scenario_runner.is_scenario_finished()

    #Checks to see if the metamorphic test on the scenario is running. This gets called from the assessment_toolkit.py
    def is_metamorphic_test_running(self):
        return self.scenario_runner.is_metamorphic_test_running()



    




