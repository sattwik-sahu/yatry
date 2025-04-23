from yatry.utils.models import Passenger
from datetime import datetime, timedelta
import random
from yatry.utils.data.locations import Location
from pprint import pprint


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

    passengers = []
    start_time, end_time = time_range
    total_seconds = int((end_time - start_time).total_seconds())

    for i in range(n_passengers):
        origin, destination = Location.AASHIMA, Location.AASHIMA
        while not (
            Location.IISERB in (origin, destination) and origin is not destination
        ):
            origin, destination = random.sample(list(Location), 2)
        random_seconds = random.randint(0, total_seconds)
        duration = random.randint(900, min(5400, (total_seconds - random_seconds)))
        departure_time_start = start_time + timedelta(seconds=random_seconds)
        departure_time_end = departure_time_start + timedelta(seconds=duration)

        passenger = Passenger(
            name=i,
            source=origin,
            destination=destination,
            dep_time_range=(departure_time_start, departure_time_end),
        )
        passengers.append(passenger)

    return passengers


def main():
    pprint(
        create_random_passengers(
            n_passengers=5,
            time_range=(datetime.now(), datetime.now() + timedelta(days=1)),
        )
    )


if __name__ == "__main__":
    main()
