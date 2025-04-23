import numpy as np


def affinity_propagation_ride_sharing(
    convenience_matrix: np.ndarray,
    max_iterations: int = 200,
    damping_factor: float = 0.9,
    convergence_threshold: float = 1e-6,
) -> tuple[dict[int, list[int]], list[int]]:
    """
    Implements Affinity Propagation algorithm for ride-sharing scenarios.

    This function takes a convenience matrix where entry (i,j) represents how
    convenient it is for passenger i to share a ride with passenger j, and
    returns a clustering of passengers with designated drivers.

    Args:
        convenience_matrix: An `n x n` numpy array where entry (i,j) is the
            convenience score for passenger i to share a ride with passenger j.
        max_iterations: The maximum number of iterations to run the algorithm.
        damping_factor: Factor between 0.5 and 1.0 that dampens updates to
            avoid numerical oscillations.
        convergence_threshold: Minimum change in responsibility and
            availability matrices to declare convergence.

    Returns:
        A tuple containing:
            - A dictionary mapping driver IDs to lists of passenger IDs
            - A list of identified driver IDs (exemplars)
    """
    # Get the number of passengers
    n_passengers = convenience_matrix.shape[0]

    # Initialize the responsibility and availability matrices with zeros
    # Responsibility R(i,k): How good would passenger k be as a driver for passenger i
    R = np.zeros((n_passengers, n_passengers))

    # Availability A(i,k): How willing is passenger k to be a driver for passenger i
    A = np.zeros((n_passengers, n_passengers))

    # Use the convenience matrix as our similarity matrix
    S = convenience_matrix.copy()

    # Main loop - iteratively update responsibilities and availabilities
    for iteration in range(max_iterations):
        # Store old values to check for convergence
        old_R = R.copy()
        old_A = A.copy()

        # Step 1: Update responsibilities
        # R(i,k) = S(i,k) - max_{k' != k} {A(i,k') + S(i,k')}
        # This means: "How good is k as a driver for i compared to all other potential drivers?"
        for i in range(n_passengers):
            for k in range(n_passengers):
                # Find the maximum value excluding k
                AS = A[i, :] + S[i, :]  # Add availability and similarity for all k'
                AS[k] = -np.inf  # Exclude k itself
                max_val = np.max(AS)

                # Calculate new responsibility value
                r_new = S[i, k] - max_val

                # Apply damping to avoid oscillations
                # new_value = (1-damping) * new_calculation + damping * old_value
                R[i, k] = (1 - damping_factor) * r_new + damping_factor * R[i, k]

        # Step 2: Update availabilities
        # For i != k: A(i,k) = min(0, R(k,k) + sum_{i' != i,k} max(0, R(i',k)))
        # For i == k: A(k,k) = sum_{i' != k} max(0, R(i',k))
        # This means: "Given how other passengers view k as a driver,
        # how appropriate is it for i to choose k as their driver?"
        for i in range(n_passengers):
            for k in range(n_passengers):
                if i != k:
                    # Calculate sum of positive responsibilities to k from others (except i)
                    positive_r = np.maximum(
                        0, R[:, k]
                    )  # Get all positive responsibilities to k
                    positive_r[i] = 0  # Exclude i
                    positive_r[k] = 0  # Exclude k itself
                    sum_pos_r = np.sum(positive_r)

                    # Calculate new availability (capped at 0 for i!=k)
                    a_new = min(0, R[k, k] + sum_pos_r)
                else:
                    # Self-availability calculation
                    positive_r = np.maximum(
                        0, R[:, k]
                    )  # Get all positive responsibilities to k
                    positive_r[k] = 0  # Exclude k itself
                    sum_pos_r = np.sum(positive_r)

                    # Self-availability is not capped at 0
                    a_new = sum_pos_r

                # Apply damping
                A[i, k] = (1 - damping_factor) * a_new + damping_factor * A[i, k]

        # Check for convergence - if changes are small enough, we can stop
        if (
            np.sum(np.abs(R - old_R)) + np.sum(np.abs(A - old_A))
        ) < convergence_threshold:
            print(f"Converged after {iteration + 1} iterations")
            break

    # Step 3: Identify exemplars (drivers)
    # A point becomes an exemplar if (A(i,i) + R(i,i)) > 0
    # This means the point "agrees" to be an exemplar based on gathered evidence
    decision_matrix = A + R
    driver_indices = np.where(np.diag(decision_matrix) > 0)[0].tolist()

    # If no drivers found (can happen in edge cases), choose the point with max self-decision value
    if not driver_indices:
        print(
            "No drivers identified naturally, selecting based on highest decision value"
        )
        driver_indices = [np.argmax(np.diag(decision_matrix))]

    # Step 4: Assign passengers to drivers (forming carpools)
    carpools = {driver: [] for driver in driver_indices}  # type: ignore

    for passenger in range(n_passengers):
        # A passenger joins the carpool of the driver that maximizes A(passenger,driver) + R(passenger,driver)
        if passenger in driver_indices:  # type: ignore
            # Drivers are already assigned to their own carpool
            carpools[passenger].append(passenger)
        else:
            # Find the best driver for this passenger
            best_driver_idx = -1
            best_score = -np.inf

            for driver in driver_indices:  # type: ignore
                score = decision_matrix[passenger, driver]
                if score > best_score:
                    best_score = score
                    best_driver_idx = driver

            # Assign passenger to the best driver's carpool
            carpools[best_driver_idx].append(passenger)

    return carpools, driver_indices
