from scipy.stats import mannwhitneyu

def test_mann_whitney(source, follow_up, alpha=0.05):
    """
    Perform the Mann-Whitney U-test.
    
    Parameters:
    source (list): First group of data
    follow_up (list): Second group of data
    alpha (float): Significance level (default: 0.05)
    
    Returns:
    bool: True if the difference is statistically significant, False otherwise
    """
    # Perform the Mann-Whitney U-test
    try: 
        statistic, p_value = mannwhitneyu(source, follow_up)
        
        
        
        # Check if the p-value is less than the significance level
        return {"result":p_value < alpha, "p_value":p_value}
    except:
        return False
