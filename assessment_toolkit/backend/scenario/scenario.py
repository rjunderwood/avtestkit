
#Can only be imported on the system with carla. 
from .follow_vehicle import ScenarioFollowVehicle
from .follow_vehicle_town3 import ScenarioFollowVehicleTown3
from .pedestrian_crossing import ScenarioPedestrianCrossing
from .red_light import ScenarioRedLight


class Scenario: 
    

    #A Object on the specific scenario eg. FollowVehicle
    scenario_runner = None
    scenario_name = None
    scenario_data = None


    def __init__(self, scenario_name, scenario_params):
        self.scenario_name = scenario_name

        print("SCenario __ini__"+ str(self.scenario_runner))
        #Set the Scenario 
        if(scenario_name == 'follow_vehicle'):
            self.scenario_runner = ScenarioFollowVehicle()
        if(scenario_name == 'follow_vehicle_town3'):
            print("Added Vehicle TOWN 3 "+scenario_name)
            self.scenario_runner = ScenarioFollowVehicleTown3()
        if(scenario_name == 'pedestrian_crossing'):
            self.scenario_runner = ScenarioPedestrianCrossing()
        if(scenario_name == 'red_light'):
            self.scenario_runner = ScenarioRedLight()
        print("SCenario __ini__"+ str(self.scenario_runner))
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



    




