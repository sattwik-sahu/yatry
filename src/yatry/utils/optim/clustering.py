import numpy as np


def affinity_propagation_ride_sharing(
    affinity_matrix: np.ndarray,
    max_iterations: int = 200,
    damping_factor: float = 0.9,
    convergence_threshold: float = 1e-6,
) -> tuple[dict[int, list[int]], list[int]]:
    """
    Implements Affinity Propagation algorithm for ride-sharing passenger grouping.

    This function takes an affinity matrix where entry (i,j) represents how
    much passenger i would like to be grouped with passenger j, and
    returns clusters of passengers with designated cluster representatives.

    Args:
        affinity_matrix: An `n x n` numpy array where entry (i,j) is the
            affinity score for passenger i towards passenger j.
        max_iterations: The maximum number of iterations to run the algorithm.
        damping_factor: Factor between 0.5 and 1.0 that dampens updates to
            avoid numerical oscillations.
        convergence_threshold: Minimum change in responsibility and
            availability matrices to declare convergence.

    Returns:
        A tuple containing:
            - A dictionary mapping cluster representative IDs to lists of member passenger IDs
            - A list of identified cluster representative IDs (exemplars)
    """
    # Get the number of passengers
    n_passengers = affinity_matrix.shape[0]

    # Initialize the responsibility and availability matrices with zeros
    # Responsibility R(i,k): How suitable would passenger k be as a representative for passenger i
    R = np.zeros((n_passengers, n_passengers))

    # Availability A(i,k): How appropriate is it for passenger i to select passenger k as their representative
    A = np.zeros((n_passengers, n_passengers))

    # Use the affinity matrix as our similarity matrix
    S = affinity_matrix.copy()

    # Main loop - iteratively update responsibilities and availabilities
    for iteration in range(max_iterations):
        # Store old values to check for convergence
        old_R = R.copy()
        old_A = A.copy()

        # Step 1: Update responsibilities
        # R(i,k) = S(i,k) - max_{k' != k} {A(i,k') + S(i,k')}
        # This means: "How suitable is k as a representative for i compared to all other potential representatives?"
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
        # This means: "Given how other passengers view k as a representative,
        # how appropriate is it for i to choose k as their group representative?"
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

    # Step 3: Identify exemplars (cluster representatives)
    # A passenger becomes a representative if (A(i,i) + R(i,i)) > 0
    # This means the passenger "agrees" to be a representative based on gathered evidence
    decision_matrix = A + R
    # Convert NumPy array to explicit Python list of integers
    representative_indices = [
        int(idx) for idx in np.where(np.diag(decision_matrix) > 0)[0]
    ]

    # If no representatives found (can happen in edge cases), choose the passenger with max self-decision value
    if not representative_indices:
        print(
            "No cluster representatives identified naturally, selecting based on highest decision value"
        )
        representative_indices = [int(np.argmax(np.diag(decision_matrix)))]

    # Step 4: Assign passengers to their representatives (forming groups)
    passenger_groups: dict[int, list[int]] = {rep: [] for rep in representative_indices}

    for passenger in range(n_passengers):
        # A passenger joins the group of the representative that maximizes A(passenger,rep) + R(passenger,rep)
        if passenger in representative_indices:
            # Representatives are already assigned to their own group
            passenger_groups[passenger].append(passenger)
        else:
            # Find the best representative for this passenger
            best_rep_idx = -1
            best_score = -np.inf

            for rep in representative_indices:
                score = decision_matrix[passenger, rep]
                if score > best_score:
                    best_score = score
                    best_rep_idx = rep

            # Assign passenger to the best representative's group
            passenger_groups[best_rep_idx].append(passenger)

    return passenger_groups, representative_indices
