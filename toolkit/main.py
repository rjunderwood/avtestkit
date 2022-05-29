
# from scenario_runner.scenario_runner import ScenarioRunner
from assessment_toolkit import  AssessmentToolkit


# class Main:
    
#     def __init__(self) -> None:
#        None

#Starts the program and makes everything work.
def main():
    
    #Start Assessment Toolkit
    assessment_toolkit = AssessmentToolkit()    
    #Run Scenarios
    assessment_toolkit.run_scenarios()

    assessment_toolkit.get_toolkit_status()



main()


    

