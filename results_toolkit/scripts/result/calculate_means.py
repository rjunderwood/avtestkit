

import statistics as stats

def calculate_means(source,follow_ups):
    source_mean = stats.mean(source)
    #flatten the 3d array to 2d array follow_ups
    follow_ups_mean = []
    for follow_up in follow_ups:
        follow_ups_mean.append(stats.mean(follow_up))

    return {"source_mean":source_mean,"follow_ups_mean":follow_ups_mean}
 
    