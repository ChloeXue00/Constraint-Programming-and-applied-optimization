#last year revenues W
#possible location l, l[i] with fixed cost F[i]
#variable cost C1 based on retailer size, per 100m^2 assume per m^2 variable cost c[i]
#retailer size:  [L1,U1]
#each retailer revenues R1  per
#center count <=k
# set of locations of retail centers and their size to maximum revenue R[i]
from gurobipy import *

m=Model('model')

I = range(5)  # assume 5 possible retailer location
F = [10000, 20000, 15000, 18000, 25000]  # every location costs
C = [500, 700, 600, 650, 550]  # every 100 square meters cost
R = [2000, 2200, 2100, 2300, 2400]  # every 100 square meters revenue
L = [10, 15, 12, 20, 18]  # every retailer lowest size
U = [30, 35, 28, 40, 32]  # every retailer max size
W = 100000  # Fiat , last year upper limit
K = 3  # max retailer
# decision variable
x = m.addVars(I, vtype=GRB.BINARY, name="open")  # x_i , binary, if open a store
s = m.addVars(I, vtype=GRB.CONTINUOUS, name="size")  # s_i retailer size (every 100 square meters)


# objective function：max(total revenue- cost)
m.setObjective(quicksum(R[i] * s[i] - F[i] * x[i] - C[i] * s[i] for i in I), GRB.MAXIMIZE)

# budget constrain：fixed cost + variable cost <= W
m.addConstr(quicksum(F[i] * x[i] + C[i] * s[i] for i in I) <= W, "budget")

# retailer constrain ：total number retailer <= K
m.addConstr(quicksum(x[i] for i in I) <= K, "store_limit")

# constrain on retailer size：L_i * x_i <= s_i <= U_i * x_i
for i in I:
    m.addConstr(s[i] >= L[i] * x[i], f"min_size_{i}")
    m.addConstr(s[i] <= U[i] * x[i], f"max_size_{i}")

# solver
m.optimize()

# results
for i in I:
    if x[i].x > 0.5:  # if retailer is open
        print(f"Location {i}: Open, Size = {s[i].x * 100} m², Revenue = {R[i] * s[i].x}, Cost = {F[i] + C[i] * s[i].x}")
