

#https://www.frontiersin.org/articles/10.3389/ffutr.2021.759125/full
#3.1 Performance Metrics for Environment Perception


class SafetyMetric: 

    distance_stopped_from_pedestrian = None
    ego_position = None
    ego_velocity = None
    ego_acceleration = None

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
    #Jaccard Distance
    ratio_object_jaccard_distance = 0.1
    #Multiple Object Detection Accuracy
    object_intersection_over_union = 0.1
    #Multiple-Object-Tracking Accuracy
    object_mota = 0.1
    #Multiple Object-Tracking Precision
    object_motp = 0.1
    #Lane Offset 
    ego_lane_offset_variance = 0.1

    ##########
    #Higher Order Tracking Accuracy
    ###########

    #Association Score
    object_association_score = 0.1
    #Detection accuracy 
    object_detection_score = 0.1
    #Association accuracy
    object_detection_accuracy = 0.1
    #Higher Order Tracking Accuracy score
    object_higher_order_accuracy_score = 0.1
    

    #######
    #Motion Planning Metrics 
    ######

    #TTC Time to Collision how
    #don't let below X time for safety
    object_time_to_collision = 10
    object_exposed_time_to_collision = 1
    object_post_encroachment_time = 1

    #total near collision 
    total_near_collisions = 10 
    #Space required to stop this is more of a ratio as the safe long distance is dynamically changing based on velocity between ego and object
    #Towards eachother and not towards eachother longitudinal distance
    safe_longitudinal_distance = 0.5
    safe_lateral_distance = 10
    total_longitudinal_distance_violations = 1
    total_lateral_distance_violations = 1
    #Time that longitudinal distance is not met is the longitudinal threshold 









    
    

    


    