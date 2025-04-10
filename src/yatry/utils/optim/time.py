import numpy as np
from scipy.stats import norm
from yatry.utils.helpers.time import calc_time_conv_params
from scipy.optimize import golden


def optimize_dep_time(
    t_mins: list[float], t_maxs: list[float], m_range: float = 0.8
) -> float:
    """
    Optimizes the common departure time that best satisfies individual preferences.

    Given multiple passengers' preferred departure windows (`t_min` to `t_max`) and
    how strictly they prefer to stay within those windows (`m_range`), this function
    computes the optimal departure time that minimizes the overall inconvenience
    (negative log-likelihood) across all passengers, assuming each individual's
    time preference is modeled as a normal distribution.

    Args:
        t_mins (list[float]): List of earliest preferred departure times for each passenger.
        t_maxs (list[float]): List of latest preferred departure times for each passenger.
        m_ranges (float): Proportion (between 0 and 1) representing how much of each
            passenger's preference mass lies between `t_min` and `t_max`.
            If not provided, defaults to 0.8.

    Returns:
        float: The optimized common departure time that minimizes collective inconvenience.
    """
    mus, stds = [], []

    for t_min, t_max in zip(t_mins, t_maxs):
        mu, std = calc_time_conv_params(t_min=t_min, t_max=t_max, m_range=m_range)
        mus.append(mu)
        stds.append(std)

    mus = np.array(mus)
    stds = np.array(stds)
    brack_start = np.min(mus - 3 * stds)
    brack_end = np.min(mus + 3 * stds)

    def _time_objective_func(x: float) -> float:
        return float(-np.sum([norm.logpdf(x, mu, std) for mu, std in zip(mus, stds)]))

    return float(golden(func=_time_objective_func, brack=(brack_start, brack_end)))
