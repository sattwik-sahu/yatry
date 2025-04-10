# Time Affinity Scoring Implementation
# This module calculates time-based affinity scores between passengers.

import numpy as np

def calculate_time_affinity(dist_i, dist_j):
    """
    Calculate the time affinity score between two passengers based on their time preferences.

    Args:
        dist_i (callable): Probability distribution function for passenger i.
        dist_j (callable): Probability distribution function for passenger j.

    Returns:
        float: Time affinity score.
    """
    def bhattacharyya_coefficient(p, q):
        return np.sum(np.sqrt(p * q))

    def hellinger_distance(p, q):
        return 1 - bhattacharyya_coefficient(p, q)

    return hellinger_distance(dist_i, dist_j)
