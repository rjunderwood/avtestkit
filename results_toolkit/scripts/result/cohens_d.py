import numpy as np

def test_cohens_d(group1, group2):
    """
    Calculate Cohen's d for two groups of data.
    
    Parameters:
    group1 (array-like): First group of data.
    group2 (array-like): Second group of data.
    
    Returns:
    d (float): Cohen's d value.
    """
    # Calculate the means of the two groups
    mean1, mean2 = np.mean(group1), np.mean(group2)
    
    # Calculate the pooled standard deviation
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
    pooled_sd = np.sqrt(pooled_var)
    
    # Calculate Cohen's d
    d = (mean1 - mean2) / pooled_sd
    
    return d