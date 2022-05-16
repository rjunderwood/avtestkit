##This is the main output result that a scenario has. 
from metric_calc.environment_perception import  CalcEnvironmentPerception
from metric_calc.higher_order_tracking import CalcHigherOrderTracking
from metric_calc.motion_planning import CalcMotionPlanning



class ScenarioResult:

    accelerationApplied = {};
    breakApplied = {};
    leftTurnApplied = {}; 
    rightTurnApplied = {}; 


    #Adds Step information and writes to file. 
    def add_step():

        #Ego Step Information

        #Object Step Information 

        #Ego Object Perception Step Information 
        
        return None
    

    

    def add_acceleration(self, time, amount):
        self.accelerationApplied[time] = amount

    def add_break(self, time, amount):
        self.breakApplied[time] = amount

    def add_left_turn(self,time, amount):
        self.leftTurnApplied[time] = amount
    
    def add_right_turn(self, time, amount):
        self.rightTurnApplied[time] = amount

    def get_record(self, time, data_set): 
        try:
            return self.data_set[time]
        except:
            return None
    
    def get_data(self, data_set): 
        try:
            return self.data_set
        except:
            return None

    def write_data_to_file():
        #Writes the output to the file in order to preserve memory.

        #Clear the memory holding the Scenario_result variables.


    


