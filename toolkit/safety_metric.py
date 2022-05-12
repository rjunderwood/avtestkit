

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

    #p the ratio of true positive instances to the actual number of positive instances. This metric is suitable when false negatives are of high importance.
    ratio_object_recall_sensitivity = 0.1
    #r the ratio of true positive instances to the predicted number of positive instances. This metric is useful when false positive instances are important.
    ratio_object_precision_confidence = 0.1
    #F harmonic mean of precision p and recall r
    ratio_object_harmonic_mean = (2*ratio_object_precision_confidence*ratio_object_recall_sensitivity)/ratio_object_precision_confidence+ratio_object_recall_sensitivity

    

    


    