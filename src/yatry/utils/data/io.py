import numpy as np
from yatry.utils.models import Passenger
from datetime import datetime


def create_random_passengers(
    n_passengers: int, time_range: tuple[datetime, datetime]
) -> list[Passenger]:
    """
    Returns a list of random passengers going to and from random places at
    random times.

    Args:
        n_passengers (int): The number of passengers to generate.
        time_range(tuple[datetime, datetime]): The `(start_time, end_time)`
            range of preferred departure times for the passengers.

    Returns:
        list[Passengers]:
            A list of random passengers.
    """
    pass
