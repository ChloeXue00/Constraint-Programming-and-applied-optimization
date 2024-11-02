from gurobipy import *
from sympy.physics.units import hours

#constr: each line working time limited 10x+15y+5z<=100
#constra
#objective function ,maximize the quantity of foam c=c1+c2+c3,maximize c
m=Model("model")

hours_per_component= m.addVars(4, 3, name="hours", vtype=GRB.CONTINUOUS, lb=0)  #hours
production_rate = [
    [10,15,5],
    [15,10,5],
    [20,5,10],
    [10,15,20]
]
capacity=[100,150,80,200]
production_result=[
    [0,0,0],
    [0,0,0],
    [0,0,0],
    [0,0,0]
]
production_per_component=[0,0,0]
hours_per_line=[0,0,0,0] #hours on each line


# constrain
for i in range(4):  # constrains on each line
    m.addConstr(sum(hours_per_component[i, j] for j in range(3)) <= capacity[i],
                name=f"capacity_limit_line_{i}")

# objective function for total production
total_production = 0  # total production
for j in range(3):  # count on evert component
    production_per_component[j] = sum(production_rate[i][j] * hours_per_component[i, j] for i in range(4))
    total_production += production_per_component[j]


m.setObjective(total_production,GRB.MAXIMIZE)

m.optimize()



for j in range(3):
    print(f"Total production of component {j+1}: {production_per_component[j].getValue()}")

# hours on each component, on each line
for i in range(4):
    for j in range(3):
        print(f"Hours used on line {i+1} for component {j+1}: {hours_per_component[i, j].x}")