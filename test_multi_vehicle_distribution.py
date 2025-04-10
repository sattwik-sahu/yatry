from multi_vehicle_distribution import optimize_vehicle_distribution

# Example input
groups = [[1, 2, 3], [4, 5, 6]]
vehicle_capacity = 4
segment_fares = [10, 20, 30]

# Add debug prints to inspect intermediate values
print("Input Groups:", groups)
print("Vehicle Capacity:", vehicle_capacity)
print("Segment Fares:", segment_fares)

# Run the optimization
try:
    result = optimize_vehicle_distribution(groups, vehicle_capacity, segment_fares)
    print("Optimized Vehicle Assignments:", result)
except ValueError as e:
    print("Error:", e)
