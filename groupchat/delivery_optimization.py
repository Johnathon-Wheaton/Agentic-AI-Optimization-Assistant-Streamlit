# filename: delivery_optimization.py

import json
import numpy as np
from scipy.spatial import distance
from ortools.linear_solver import pywraplp

# Input Data
n_trucks = 3
truck_drive_time_limit = 8 * 60  # in minutes
truck_load_capacity = 2000  # in kg
truck_speed = 40 / 60  # km/min (40 km/hr)
starting_location = (5, 5)

customers = {
    1: {'coordinates': (10, 15), 'delivery_amount': 300, 'delivery_window': (9 * 60, 11 * 60), 'service_time': 15},
    2: {'coordinates': (15, 10), 'delivery_amount': 400, 'delivery_window': (8 * 60, 10 * 60), 'service_time': 15},
    3: {'coordinates': (8, 8), 'delivery_amount': 250, 'delivery_window': (10 * 60, 12 * 60), 'service_time': 15},
    4: {'coordinates': (12, 12), 'delivery_amount': 350, 'delivery_window': (11 * 60, 13 * 60), 'service_time': 15},
    5: {'coordinates': (5, 15), 'delivery_amount': 600, 'delivery_window': (9 * 60, 12 * 60), 'service_time': 15},
    6: {'coordinates': (15, 5), 'delivery_amount': 450, 'delivery_window': (8 * 60, 11 * 60), 'service_time': 15},
    7: {'coordinates': (9, 12), 'delivery_amount': 500, 'delivery_window': (10 * 60, 14 * 60), 'service_time': 15},
    8: {'coordinates': (11, 8), 'delivery_amount': 300, 'delivery_window': (9 * 60, 12 * 60), 'service_time': 15},
    9: {'coordinates': (7, 7), 'delivery_amount': 400, 'delivery_window': (11 * 60, 14 * 60), 'service_time': 15},
    10: {'coordinates': (14, 14), 'delivery_amount': 550, 'delivery_window': (10 * 60, 13 * 60), 'service_time': 15},
    11: {'coordinates': (6, 10), 'delivery_amount': 280, 'delivery_window': (8 * 60, 10 * 60), 'service_time': 15},
    12: {'coordinates': (13, 7), 'delivery_amount': 320, 'delivery_window': (9 * 60, 11 * 60), 'service_time': 15}
}

# Distance Calculation Matrix
customer_ids = list(customers.keys())
num_customers = len(customers)
distance_matrix = np.zeros((num_customers + 1, num_customers + 1))

# Calculate distances from the starting point and between each customer
for i, customer_id in enumerate(customer_ids):
    distance_matrix[0, i + 1] = distance.euclidean(starting_location, customers[customer_id]['coordinates'])
    for j, customer_id2 in enumerate(customer_ids):
        distance_matrix[i + 1, j + 1] = distance.euclidean(customers[customer_id]['coordinates'], customers[customer_id2]['coordinates'])
    distance_matrix[i + 1, 0] = distance_matrix[0, i + 1]  # Distance back to starting point

# Create the solver
solver = pywraplp.Solver.CreateSolver('SCIP')
if not solver:
    raise Exception("Unable to create the solver.")

# Decision variables
x = {}
for i in range(n_trucks):
    for j in range(num_customers + 1):
        x[i, j] = solver.IntVar(0, 1, f'x[{i},{j}]')  # Truck i delivers to customer j

# Auxiliary variables for total distance traveled between customers
d = {}
for i in range(n_trucks):
    for j in range(num_customers + 1):
        for k in range(num_customers + 1):
            if j != k:
                d[i, j, k] = solver.NumVar(0, solver.infinity(), f'd[{i},{j},{k}]')  # Distance for truck i from j to k

# Constraints to ensure proper routing
for i in range(n_trucks):
    for j in range(num_customers + 1):
        for k in range(num_customers + 1):
            if j != k:
                # The distance from j to k can only be counted if truck i travels from j to k
                solver.Add(d[i, j, k] == distance_matrix[j][k] * x[i, j] * x[i, k])

# Total distance is the sum of all traveled distances
total_distance = solver.Sum(d[i, j, k] for i in range(n_trucks) for j in range(num_customers + 1) for k in range(num_customers + 1) if j != k)

# Objective Function: Minimize the total distance traveled
solver.Minimize(total_distance)

# Constraints
# Each customer must be served exactly once
for j in range(1, num_customers + 1):
    solver.Add(solver.Sum(x[i, j] for i in range(n_trucks)) == 1)

# Capacity constraints
for i in range(n_trucks):
    total_weight = solver.Sum(customers[j]['delivery_amount'] * x[i, j] for j in range(1, num_customers + 1))
    solver.Add(total_weight <= truck_load_capacity)

# Delivery start time variables
delivery_start_time = {}
for i in range(n_trucks):
    for j in range(num_customers + 1):
        delivery_start_time[i, j] = solver.NumVar(0, truck_drive_time_limit, f'delivery_start_time[{i},{j}]')

# Ensure trucks leave the starting point in a timely manner
for i in range(n_trucks):
    for j in range(1, num_customers + 1):
        travel_time_to_customer = distance_matrix[0][j] * (1 / truck_speed)
        solver.Add(delivery_start_time[i, j] >= travel_time_to_customer)  # Must leave in time
        solver.Add(delivery_start_time[i, j] >= customers[j]['delivery_window'][0])  # Arrive within window

        for k in range(1, num_customers + 1):
            if j != k:
                travel_time_between_customers = distance_matrix[j][k] * (1 / truck_speed)
                solver.Add(delivery_start_time[i, k] >= delivery_start_time[i, j] + customers[j]['service_time'] + travel_time_between_customers)
                solver.Add(delivery_start_time[i, k] >= customers[k]['delivery_window'][0])  # Within window
                solver.Add(delivery_start_time[i, k] <= customers[k]['delivery_window'][1])  # Within window

    # Ensure trucks return to the starting location after all deliveries
    for k in range(1, num_customers + 1):
        return_travel_time = distance_matrix[k][0] * (1 / truck_speed)
        solver.Add(delivery_start_time[i, 0] >= delivery_start_time[i, k] + customers[k]['service_time'] + return_travel_time)

# Solve the problem
solver.Solve()

# Prepare results
solution = {'x': {}, 'objective_value': total_distance.solution_value()}
for i in range(n_trucks):
    for j in range(num_customers + 1):
        solution['x'][f'x[{i},{j}]'] = x[i, j].solution_value()

# Print the results in JSON format
print(json.dumps(solution, indent=4))