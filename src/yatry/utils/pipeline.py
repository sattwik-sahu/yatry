import numpy as np
from yatry.utils.data.locations import Location
from yatry.utils.helpers.route import get_longest_prefix
from yatry.utils.models import Passenger
from yatry.utils.models.map import Map
from yatry.utils.data.map import BHOPAL
from yatry.utils.data.io import create_random_passengers
from numpy import typing as npt
from datetime import datetime, timedelta
from yatry.utils.helpers.time import time_affinity_score
from yatry.utils.optim.clustering import affinity_propagation_ride_sharing
from yatry.utils.optim.assign import VehicleAssignmentModel
from yatry.utils.optim.time import optimize_passengers_dep_time
from pprint import pprint


def main():
    # Get the random passengers
    N_PASSENGERS: int = 10
    passengers: list[Passenger] = create_random_passengers(
        n_passengers=N_PASSENGERS,
        time_range=(datetime.now(), datetime.now() + timedelta(days=1)),
    )

    pprint(passengers)

    for passenger in passengers:
        print(passenger)
        print(BHOPAL._find_route(passenger.source, passenger.destination))
        BHOPAL.show()

    # Create the time affinity matrix
    # tau: npt.NDArray[np.float64] = np.zeros(shape=(N_PASSENGERS, N_PASSENGERS))
    # for i, p_i in enumerate(passengers):
    #     for j, p_j in enumerate(passengers):
    #         t1_min, t1_max = p_i.get_dep_time_range_num()
    #         t2_min, t2_max = p_j.get_dep_time_range_num()
    #         tau[i, j] = time_affinity_score(
    #             t1_min=t1_min, t1_max=t1_max, t2_min=t2_min, t2_max=t2_max
    #         )

    # # Create route affinity matrix
    # rho: npt.NDArray[np.float64] = BHOPAL.get_passenger_route_affinity_matrix(
    #     passengers=passengers
    # )

    # # Create the affinity matrix
    # affinity_matrix: npt.NDArray[np.float64] = rho * tau

    # # Cluster the passengers according to affinty
    # cluster_passenger_inxs, _ = affinity_propagation_ride_sharing(
    #     affinity_matrix=affinity_matrix
    # )
    # cluster_passengers = [
    #     [passengers[i] for i in passenger_inxs]
    #     for passenger_inxs in cluster_passenger_inxs.values()
    # ]

    # Vehicle wise assignment
    # vehicle_assignment = VehicleAssignmentModel()

    # Optimize departure time for each group of passengers
    # for i, group in enumerate(cluster_passengers):
    #     dep_time: float = optimize_passengers_dep_time(passengers=group)
    #     print(f"======= Group #{i + 1} ======")
    #     print(
    #         f"Time of Departure: {datetime.fromtimestamp(dep_time).strftime('%H:%M %d %b %Y')}"
    #     )
    #     print("Passengers:")
    #     for passenger_ in group:
    #         print(
    #             f"{passenger_.name} | From: {passenger_.source.value}; To: {passenger_.destination.value}"
    #         )


if __name__ == "__main__":
    print(BHOPAL._find_route(Location.IISERB, Location.BAIRAGARH))
    BHOPAL.show()
    print(BHOPAL._find_route(Location.IISERB, Location.BAIRAGARH))
    # main()
