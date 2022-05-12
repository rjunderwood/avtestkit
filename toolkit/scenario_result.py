##This is the main output result that a scenario has. 
class ScenarioResult:

    accelerationApplied = {};
    breakApplied = {};
    leftTurnApplied = {}; 
    rightTurnApplied = {}; 

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


    


