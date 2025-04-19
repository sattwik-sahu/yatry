def Route(destination):
    des_list = ['I', 'S', 'C', 'B', 'G', 'A', 'D', 'L', 'N', 'U', 'M']
    des = des_list.index(destination)
    r = [[]]

    if des < 4:
        for i in range(1, des + 1):
            temp = []
            for j in range(1, i + 1):
                temp.append(j)
            r.append(temp)
    else:
        for i in range(4, des + 1):
            temp = []
            for j in range(4, i + 1):
                temp.append(j)
            r.append(temp)

    return r[-1]

def longest_common_prefix(route1, route2):
    lcp = []
    for a, b in zip(route1, route2):
        if a == b:
            lcp.append(a)
        else:
            break
    return lcp

def route_affinity_score(route_i, route_j):
    lcp = longest_common_prefix(route_i, route_j)
    if lcp == route_i or lcp == route_j:
        return len(lcp) / len(route_i)
    else:
        return 0.0

def compute_affinity_matrix(routes):
    n = len(routes)
    affinity_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            affinity_matrix[i][j] = route_affinity_score(routes[i], routes[j])
    return affinity_matrix

def print_matrix(matrix):
    for row in matrix:
        print("\t".join(f"{val:.2f}" for val in row))

def main():
    dest = input("Enter destinations (characters from I, S, C, B, G, A, D, L, N, U, M) separated by space: ").split()
    routes = [Route(ele) for ele in dest]
    affinity_matrix = compute_affinity_matrix(routes)
    print("\nAffinity Matrix (ρ_ij):")
    print_matrix(affinity_matrix)

if __name__ == "__main__":
    main()
