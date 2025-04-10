import numpy as np
from scipy import stats


def create_time_convenience_func(
    t_min: float, t_max: float, m_range: float = 0.8
) -> tuple[float, float]:
    """
    Creates the time convenience function for a passenger, given the preferred
    earliest and latest times of departure (`t_min` and `t_max`). The output is a
    pdf with area `m_range` between `t_min` and `t_max`.

    Args:
        t_min (float): The earliest time of departure.
        t_max (float): The latest time of departure.
        m_range (float): How much of the area under the pdf should lie
            between `t_min` and `t_max`; `m_range > 0` always.

    Returns:
        tuple[float, float]: The mean and std of the normal distribution.
    """
    f_mean = (t_min + t_max) / 2
    f_std = float(-stats.norm.ppf((1 - m_range) / 2) * (t_max - t_min) / 2)

    return f_mean, f_std


def bhattacharyya_distance(u1: float, u2: float, std1: float, std2: float) -> float:
    return 0.25 * ((u1 - u2) ** 2 / (std1 + std2)) + 0.5 * np.log(
        (std1 + std2) / (2 * np.sqrt(std1 * std2))
    )


def bhattacharyya_coeff(u1: float, u2: float, std1: float, std2: float) -> float:
    return np.exp(-bhattacharyya_distance(u1=u1, u2=u2, std1=std1, std2=std2))


def time_affinity_score(
    t1_min: float, t2_min: float, t1_max: float, t2_max: float, m_range: float = 0.8
) -> float:
    u1, std1 = create_time_convenience_func(t_min=t1_min, t_max=t1_max, m_range=m_range)
    u2, std2 = create_time_convenience_func(t_min=t2_min, t_max=t2_max, m_range=m_range)
    return bhattacharyya_coeff(u1=u1, u2=u2, std1=std1, std2=std2)
