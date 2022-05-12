from safety_metric import SafetyMetric

# Initialise the toolkit
class AssessmentToolkit:
    
    #Default Safety Metric 
    safety_metric = SafetyMetric()

    def __init__(self):
        print("__init__ AssessmentToolkit")
        pass

    
    def get_toolkit_status(self):
        print("Fine")

    
    def run_scenarios(self):
        print("run_scenarios")

    
    def run_metamorphic_test(self):
        print("run_metamorphic_test")
    

    def apply_safety_metric(self):
        print('apply_safety_metric');
        

