from gurobipy import *

# model creation
m = Model("FIAT Investment Optimization")

# decision variable（million kr）
x_A = m.addVar(vtype=GRB.CONTINUOUS, name="Investment_A")
x_B = m.addVar(vtype=GRB.CONTINUOUS, name="Investment_B")
x_C = m.addVar(vtype=GRB.CONTINUOUS, name="Investment_C")
x_D = m.addVar(vtype=GRB.CONTINUOUS, name="Investment_D")
x_E = m.addVar(vtype=GRB.CONTINUOUS, name="Investment_E")

# 添加辅助变量来表示总投资
total_investment = m.addVar(vtype=GRB.CONTINUOUS, name="Total_Investment")

# constrains
# on total budget
m.addConstr(x_A + x_B + x_C + x_D + x_E <= 1000, "Total_Budget") #million kr

# lowest invest for public or gov
m.addConstr(x_B + x_C + x_D >= 0.4 * 1000, "Public_Government_Investment")

# constrain on total investment
m.addConstr(total_investment == x_A + x_B + x_C + x_D + x_E, "Total_Investment")

# average invest time <=5
m.addConstr((9 * x_A + 15 * x_B + 4 * x_C + 3 * x_D + 2 * x_E ) <= 5* total_investment, "Average_Duration")

# average risk <=1.5

m.addConstr((2 * x_A + 3 * x_B + 1 * x_C + 4 * x_D + 5 * x_E ) <= 1.5* total_investment, "Average_Risk")

# exclusive C,D
m.addConstr(x_C + x_D <= 1, "C_D_Mutual_Exclusion")

# only when x_A >1 can invest E
m.addConstr(x_E <= 1 * x_A, "Invest_E_if_A_over_1M")

# objective function：maximize the total revenue, gov has 30% tax
m.setObjective(0.045 * x_A + 0.054 * x_B + 0.051 * x_C * 0.7 + 0.044 * x_D * 0.7 + 0.061 * x_E, GRB.MAXIMIZE)


# solver
m.optimize()

# output
if m.status == GRB.OPTIMAL:
    print(f"Optimal investment in A: {x_A.X} million")
    print(f"Optimal investment in B: {x_B.X} million")
    print(f"Optimal investment in C: {x_C.X} million")
    print(f"Optimal investment in D: {x_D.X} million")
    print(f"Optimal investment in E: {x_E.X} million")
    print(f"Total Revenue: {m.objVal} million crowns")



