import numpy as np
from yatry.utils.data.locations import Location
from yatry.utils.helpers.route import get_valid_shared_route
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
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.cluster import AffinityPropagation
from collections import defaultdict


def main():
    # Get the random passengers
    N_PASSENGERS: int = 200
    passengers: list[Passenger] = create_random_passengers(
        n_passengers=N_PASSENGERS,
        time_range=(datetime.now(), datetime.now() + timedelta(hours=1)),
    )

    pprint(passengers)

    for passenger in passengers:
        print(passenger)
        print(BHOPAL._find_route(passenger.source, passenger.destination))
        BHOPAL.show()

    # Create the time affinity matrix
    tau: npt.NDArray[np.float64] = np.zeros(shape=(N_PASSENGERS, N_PASSENGERS))
    for i, p_i in enumerate(passengers):
        for j, p_j in enumerate(passengers):
            t1_min, t1_max = p_i.get_dep_time_range_num()
            t2_min, t2_max = p_j.get_dep_time_range_num()
            tau[i, j] = time_affinity_score(
                t1_min=t1_min, t1_max=t1_max, t2_min=t2_min, t2_max=t2_max
            )
    print(tau)

    # Create route affinity matrix
    rho: npt.NDArray[np.float64] = BHOPAL.get_passenger_route_affinity_matrix(
        passengers=passengers
    )
    print(rho)

    # Create the affinity matrix
    affinity_matrix: npt.NDArray[np.float64] = rho * tau
    print(affinity_matrix)
    # Cluster the passengers according to affinty
    sns.heatmap(affinity_matrix)
    plt.savefig("fig.png")
    # cluster_passenger_inxs, _ = affinity_propagation_ride_sharing(
    #     affinity_matrix=1 - affinity_matrix, convergence_threshold=1e-12
    # )
    preference_val = np.percentile(affinity_matrix, 50)
    ap = AffinityPropagation(
        affinity="precomputed",
        # random_state=42,
        damping=0.7,
        max_iter=500,
        # convergence_iter=15,
        preference=preference_val,
    )
    min_val = np.min(affinity_matrix)
    max_val = np.max(affinity_matrix)
    scaled_affinity = (affinity_matrix - min_val) / (max_val - min_val + 1e-10)
    cluster_passenger_inxs: np.ndarray = ap.fit_predict(X=scaled_affinity)
    print(cluster_passenger_inxs)

    grouped_indices = defaultdict(list)

    for idx, val in enumerate(cluster_passenger_inxs):
        grouped_indices[val].append(idx)

    # Filter only those values that have more than one index (i.e., grouped)
    groups = {val: idxs for val, idxs in grouped_indices.items() if len(idxs) > 0}

    # # Optional: pretty print
    # for auto_number, (val, idxs) in enumerate(sorted(groups.items()), start=1):
    #     print(f"\nAuto:{auto_number}")
    #     for idx in idxs:
    #         p = passengers[idx]
    #         print(f"  Passenger {idx}: {p.source.value} → {p.destination.value}")

    for auto_number, (val, idxs) in enumerate(sorted(groups.items()), start=1):
        group = [passengers[idx] for idx in idxs]

        dep_time: float = optimize_passengers_dep_time(passengers=group)

        print(f"\n======= Auto #{auto_number} =======")
        print(
            f"Optimized Departure Time: {datetime.fromtimestamp(dep_time).strftime('%H:%M %d %b %Y')}"
        )
        print(f"Total Passengers: {len(group)}")

        for passenger_ in group:
            print(
                f"{passenger_.name} | From: {passenger_.source.value} → To: {passenger_.destination.value}"
            )

    # Optimize departure time for each group of passengers
    # for i in np.unique_values(cluster_passenger_inxs):
    #     group = [
    #         passenger_
    #         for passenger_, j in zip(passengers, cluster_passenger_inxs)
    #         if j == i
    #     ]

    #     dep_time: float = optimize_passengers_dep_time(passengers=group)
    #     print(f"======= Group #{i + 1} ======")
    #     print(
    #         f"Time of Departure: {datetime.fromtimestamp(dep_time).strftime('%H:%M %d %b %Y')}"
    #     )
    #     print(f"Passengers: {len(group)}")
    #     for passenger_ in group:
    #         print(
    #             f"{passenger_.name} | From: {passenger_.source.value}; To: {passenger_.destination.value}"
    #         )


if __name__ == "__main__":
    # print(BHOPAL._find_route(Location.IISERB, Location.BAIRAGARH))
    # BHOPAL.show()
    # print(BHOPAL._find_route(Location.IISERB, Location.BAIRAGARH))
    # BHOPAL.show()
    main()
