import numpy as np
from scipy.stats import shapiro
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from sklearn.preprocessing import StandardScaler

def test_turkeys_range(source_data, follow_up_data):
    # Normalize the data
    scaler = StandardScaler()
    print(len(source_data))

    print(len(follow_up_data))
    if len(source_data) > len(follow_up_data):
        source_data = source_data[:len(follow_up_data)]
    
    if(len(source_data) < len(follow_up_data)):
        follow_up_data = follow_up_data[:len(source_data)]


    source_data_normalized = scaler.fit_transform(np.array(source_data).reshape(-1, 1))
    follow_up_data_normalized = scaler.transform(np.array(follow_up_data).reshape(-1, 1))
    
    
    # Check if the data is normally distributed
    _, p_value = shapiro(source_data_normalized)
    if p_value < 0.05:
        return False
    _, p_value = shapiro(follow_up_data_normalized)
    if p_value < 0.05:
        return False
    
    # Perform Tukey's range test
    data = np.concatenate([source_data_normalized, follow_up_data_normalized])
    groups = ['source'] * len(source_data) + ['followup'] * len(follow_up_data)
    tukey = pairwise_tukeyhsd(data, groups)
    
    # Check if there is a statistically significant difference
    match = False
    for i, group in enumerate(tukey.groupsunique):
        if group[0] == 'source' and group[1] == 'followup':
            if tukey.pvalues[i] > tukey.q_crit:
                match = True
                break
    return match