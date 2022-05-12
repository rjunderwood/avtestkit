

#https://www.frontiersin.org/articles/10.3389/ffutr.2021.759125/full
#3.1 Performance Metrics for Environment Perception


class SafetyMetric: 

    distance_stopped_from_pedestrian = None
    ego_position = None
    ego_velocity = None
    ego_acceleration = None
    estimate_object_velocity_threshold = None
    estimate_object_position_threshold = None 


    #Metrics of assessing the perception and motion planning


    def __init__(self, parameters):
        
        if(parameters == None):
            #Default Safety
            self.distance_stopped_from_pedestrian = 2 
            


    #Measuring the state of surrounding dynamic obstacles. 
    # State includes position, velocity, acceleration, and class/type.

    #Estimate velocit

    #estimate class of object 'car', 'truck', 'pedestrian'
    #estimate velocity
    #estimate position 
    #Perception of Environment State Metrics
    estimated_object_class = ''
    estimated_object_velocity_variance = 0.1 #Allow for a X% difference for the estimate
    estimated_object_position_variance = 0.1 #Allow for a X% difference for estimate

    


    