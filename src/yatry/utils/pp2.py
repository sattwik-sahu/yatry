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
    # N_PASSENGERS = 200
    saving = []
    x_vals = []
    for N_PASSENGERS in range(500, 501):
        x_vals.append(N_PASSENGERS)

        passengers: list[Passenger] = create_random_passengers(
            n_passengers=N_PASSENGERS,
            time_range=(datetime.now(), datetime.now() + timedelta(hours=1)),
        )
        print(f"N_PASSENGERS : {N_PASSENGERS}")
        # pprint(passengers)

        # for passenger in passengers:
        #     print(passenger)
        #     print(BHOPAL._find_route(passenger.source, passenger.destination))
        #     BHOPAL.show()

        # Create the time affinity matrix
        tau: npt.NDArray[np.float64] = np.zeros(shape=(N_PASSENGERS, N_PASSENGERS))
        for i, p_i in enumerate(passengers):
            for j, p_j in enumerate(passengers):
                t1_min, t1_max = p_i.get_dep_time_range_num()
                t2_min, t2_max = p_j.get_dep_time_range_num()
                tau[i, j] = time_affinity_score(
                    t1_min=t1_min, t1_max=t1_max, t2_min=t2_min, t2_max=t2_max
                )
        # print(tau)

        # Create route affinity matrix
        rho: npt.NDArray[np.float64] = BHOPAL.get_passenger_route_affinity_matrix(
            passengers=passengers
        )
        # print(rho)

        # Create the affinity matrix
        affinity_matrix: npt.NDArray[np.float64] = rho * tau
        # print(affinity_matrix)
        plt.figure(figsize=(10, 8))
        sns.heatmap(affinity_matrix, cbar_kws={"label": "Affinity Score"})
        plt.title("Combined Route-Time Affinity Matrix")
        plt.xlabel("Passenger Index")
        plt.ylabel("Passenger Index")
        plt.tight_layout()
        plt.savefig("fig.pdf")
        plt.close()

        preference_val = np.percentile(affinity_matrix, 50)
        ap = AffinityPropagation(
            affinity="precomputed",
            damping=0.7,
            max_iter=500,
            preference=preference_val,
        )
        min_val = np.min(affinity_matrix)
        max_val = np.max(affinity_matrix)
        scaled_affinity = (affinity_matrix - min_val) / (max_val - min_val + 1e-10)
        cluster_passenger_inxs: np.ndarray = ap.fit_predict(X=scaled_affinity)
        # print(cluster_passenger_inxs)

        grouped_indices = defaultdict(list)

        for idx, val in enumerate(cluster_passenger_inxs):
            grouped_indices[val].append(idx)

        # Filter only those values that have more than one index (i.e., grouped)
        groups = {val: idxs for val, idxs in grouped_indices.items() if len(idxs) > 0}
        total_total_saving = 0
        for auto_number, (val, idxs) in enumerate(sorted(groups.items()), start=1):
            group = [passengers[idx] for idx in idxs]
            total_fare = 0
            sum_fare = 0
            total_saving = 0
            for passenger_ in group:
                original_fare = BHOPAL.get_fare_on_route(
                    BHOPAL._find_route(passenger_.source, passenger_.destination)
                )
                if original_fare > total_fare:
                    total_fare = original_fare
                sum_fare += original_fare

            # dep_time: float = optimize_passengers_dep_time(passengers=group)
            try:
                dep_time: float = optimize_passengers_dep_time(passengers=group)
            except Exception as e:
                print(f"[Warning] Optimization failed for group #{auto_number}: {e}")
                # Fallback: Use average of min departure times
                dep_time = float(
                    np.mean([p.get_dep_time_range_num()[0] for p in group])
                )

            # Calculate total fare for the group

            print(
                f"\n============================================= Auto #{auto_number} =============================================="
            )
            print(
                f"Optimized Departure Time: {datetime.fromtimestamp(dep_time).strftime('%H:%M %d %b %Y')}"
            )
            print(f"Total Passengers: {len(group)}; Total fare : {total_fare}")

            # Calculate new fare for each passenger
            for passenger_ in group:
                original_fare = BHOPAL.get_fare_on_route(
                    BHOPAL._find_route(passenger_.source, passenger_.destination)
                )

                new_fare = original_fare * total_fare / sum_fare
                print(
                    f"{passenger_.name} | From: {passenger_.source.value} → To: {passenger_.destination.value} | New Fare: ₹{new_fare:.2f} | Saved : ₹{(original_fare - new_fare):.2f}"
                )
                total_saving += original_fare - new_fare
            total_total_saving += total_saving
            print(f"Total Saving for this group : ₹{total_saving}")
        print("=" * 150)
        print(f"Total Saving: ₹{total_total_saving}")
        saving_pp = total_total_saving / N_PASSENGERS
        saving.append(saving_pp)

        # Plot the savings per passenger
    plt.figure(figsize=(10, 6))
    plt.plot(x_vals, saving, label="Avg Saving per Passenger")
    plt.xlabel("Number of Passengers")
    plt.ylabel("Average Saving per passenger (₹)")
    plt.title("Average Saving per Passenger vs Number of Passengers")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("savings_vs_passengers.png")


if __name__ == "__main__":
    main()
