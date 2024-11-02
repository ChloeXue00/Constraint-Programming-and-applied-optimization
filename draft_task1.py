from gurobipy import *

# Create a new model
m = Model("Fiat-Chrysler Production")

# Define decision variables (number of cars to produce for each model)
x1 = m.addVar(vtype=GRB.INTEGER, name="Panda")
x2 = m.addVar(vtype=GRB.INTEGER, name="500")
x3 = m.addVar(vtype=GRB.INTEGER, name="Musa")
x4 = m.addVar(vtype=GRB.INTEGER, name="Giulia")

# Data from the table
price = [106, 136, 150, 427]  # in thousand Kr
material_cost_pct = [0.57, 0.60, 0.55, 0.45]  # percentage
# salary_per_month = [20000, 11000, 20000, 26000]  #  Kr/month
salary_per_month = [20, 11, 20, 26]  #  thousand Kr/month
manhour = [40, 45, 38, 100]  # hours per car
tax = [0.30, 0.15, 0.20, 0.30]  # tax percentage
min_prod = [120000, 100000, 80000, 15000]  # minimum production requirement
budget = 40000  # in million Kr
# budget = 30000  # in million Kr, decrease budget


# Compute material cost, labor cost, and net income for each car
material_cost = [price[i] * material_cost_pct[i] for i in range(4)]
labor_cost = [(salary_per_month[i] * manhour[i]) / 160 for i in range(4)]
net_income = [price[i] - material_cost[i] - labor_cost[i] for i in range(4)]
profit = [net_income[i] * (1 - tax[i]) for i in range(4)]

# Set objective: Maximize total profit
m.setObjective(profit[0] * x1 + profit[1] * x2 + profit[2] * x3 + profit[3] * x4, GRB.MAXIMIZE)

# Budget constraint: Material cost + labor cost <= budget
m.addConstr(material_cost[0] * x1 + material_cost[1] * x2 + material_cost[2] * x3 + material_cost[3] * x4 +
            labor_cost[0] * x1 + labor_cost[1] * x2 + labor_cost[2] * x3 + labor_cost[3] * x4 <= budget * 1000)

# Minimum production constraints
m.addConstr(x1 >= min_prod[0])
m.addConstr(x2 >= min_prod[1])
m.addConstr(x3 >= min_prod[2])
m.addConstr(x4 >= min_prod[3])

# Combined production constraint for Panda and Musa
m.addConstr(x1 + x3 <= 300000)

# Optimize model
m.optimize()

# Print the results
if m.status == GRB.OPTIMAL:

    print(f"Panda: {x1.X} cars")
    print(f"500: {x2.X} cars")
    print(f"Musa: {x3.X} cars")
    print(f"Giulia: {x4.X} cars")
    print(f"Optimal total profit: {m.objVal}")
