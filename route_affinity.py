# Route Affinity Scoring Implementation
# This module calculates route-based affinity scores between passengers.

def calculate_route_affinity(route_i, route_j):
    """
    Calculate the route affinity score between two passengers based on their routes.

    Args:
        route_i (list): Route of passenger i as a list of nodes.
        route_j (list): Route of passenger j as a list of nodes.

    Returns:
        float: Route affinity score.
    """
    def longest_common_prefix(seq1, seq2):
        lcp = []
        for a, b in zip(seq1, seq2):
            if a == b:
                lcp.append(a)
            else:
                break
        return lcp

    lcp = longest_common_prefix(route_i, route_j)
    if lcp == route_i or lcp == route_j:
        return len(lcp) / len(route_i)
    return 0.0
