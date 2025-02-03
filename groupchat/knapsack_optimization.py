# filename: knapsack_optimization.py

import json
from pulp import LpProblem, LpMaximize, LpVariable, LpStatus, LpBinary, value, PULP_CBC_CMD  # Ensure PULP_CBC_CMD is imported

# Define input data
items = {
    "A": {"value": 10, "weight": 8},
    "B": {"value": 6, "weight": 4},
    "C": {"value": 6, "weight": 6}
}
weight_limit = 10

# Create the optimization problem
problem = LpProblem("Knapsack_Optimization", LpMaximize)

# Define decision variables
item_A_in_knapsack = LpVariable('item_A_in_knapsack', lowBound=0, upBound=1, cat=LpBinary)
item_B_in_knapsack = LpVariable('item_B_in_knapsack', lowBound=0, upBound=1, cat=LpBinary)
item_C_in_knapsack = LpVariable('item_C_in_knapsack', lowBound=0, upBound=1, cat=LpBinary)

# Objective function
problem += (10 * item_A_in_knapsack + 6 * item_B_in_knapsack + 6 * item_C_in_knapsack), "Total_Value"

# Constraints
problem += (8 * item_A_in_knapsack + 4 * item_B_in_knapsack + 6 * item_C_in_knapsack <= weight_limit), "Weight_Constraint"

# Create solver with correct options in a list format
solver = PULP_CBC_CMD(msg=True, timeLimit=600, options=["maxGap=0.01"])  # Setting options in the correct format

# Solve the problem with solver parameters
problem.solve(solver)

# Prepare output
output = {
    "status": LpStatus[problem.status],
    "total_value": value(problem.objective),
    "decision_variables": {
        "item_A_in_knapsack": item_A_in_knapsack.varValue,
        "item_B_in_knapsack": item_B_in_knapsack.varValue,
        "item_C_in_knapsack": item_C_in_knapsack.varValue
    }
}

# Print output in JSON format
print(json.dumps(output, indent=4))