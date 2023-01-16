

import statistics as stats

def calculate_std_devs(source,follow_ups):
    source_std_dev = stats.stdev(source)
    follow_ups_std_dev = []
    for follow_up in follow_ups:
        follow_ups_std_dev.append(stats.stdev(follow_up))
   

    return {"source_std_dev":source_std_dev,"follow_ups_std_dev":follow_ups_std_dev}