import numpy as np
from scipy import stats


def calc_time_conv_params(
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
    z = float(stats.norm.ppf((1 + m_range) / 2))
    f_std = (t_max - t_min) / (2 * z)

    return f_mean, f_std


def bhattacharyya_distance(u1: float, u2: float, std1: float, std2: float) -> float:
    """
    Computes the Bhattacharyya distance between two normal distributions.

    This distance measures the similarity between two probability distributions.
    A smaller distance implies greater overlap and hence greater similarity.

    Args:
        u1 (float): Mean of the first distribution.
        u2 (float): Mean of the second distribution.
        std1 (float): Standard deviation of the first distribution.
        std2 (float): Standard deviation of the second distribution.

    Returns:
        float: The Bhattacharyya distance between the two distributions.
    """
    return 0.25 * ((u1 - u2) ** 2 / (std1 + std2)) + 0.5 * np.log(
        (std1 + std2) / (2 * np.sqrt(std1 * std2))
    )


def bhattacharyya_coeff(u1: float, u2: float, std1: float, std2: float) -> float:
    """
    Computes the Bhattacharyya coefficient between two normal distributions.

    This coefficient measures the amount of overlap between two distributions.
    It lies in the range [0, 1], where 1 indicates complete overlap (identical
    distributions), and 0 indicates no overlap.

    Args:
        u1 (float): Mean of the first distribution.
        u2 (float): Mean of the second distribution.
        std1 (float): Standard deviation of the first distribution.
        std2 (float): Standard deviation of the second distribution.

    Returns:
        float: The Bhattacharyya coefficient between the two distributions.
    """
    return np.exp(-bhattacharyya_distance(u1=u1, u2=u2, std1=std1, std2=std2))


def time_affinity_score(
    t1_min: float, t2_min: float, t1_max: float, t2_max: float, m_range: float = 0.8
) -> float:
    """
    Computes a time affinity score between two passengers based on their
    preferred departure time windows.

    Each passenger's time preference is modeled as a normal distribution.
    The affinity score is the how much area of the first passenger's time
    convenience distribution lies between the preferred time range of the
    second passenger.

    Args:
        t1_min (float): Earliest preferred departure time of the first passenger.
        t2_min (float): Earliest preferred departure time of the second passenger.
        t1_max (float): Latest preferred departure time of the first passenger.
        t2_max (float): Latest preferred departure time of the second passenger.
        m_range (float, optional): Proportion of total probability mass that should
            lie within the preferred departure window. Defaults to 0.8.

    Returns:
        float: A value in [0, 1] indicating the time affinity between the two passengers.
    """
    u1, std1 = calc_time_conv_params(t_min=t1_min, t_max=t1_max, m_range=m_range)
    # u2, std2 = calc_time_conv_params(t_min=t2_min, t_max=t2_max, m_range=m_range)
    return min(
        1,
        (
            float(stats.norm.cdf(t2_min, u1, std1))
            - float(stats.norm.cdf(t2_max, u1, std1))
        )
        / m_range,
    )
