from gurobipy import *


# model
m=Model('model')


countries = ['Poland', 'Italy', 'US', 'Sweden']
cars = ['Panda', '500', 'Musa', 'Giulia']

#delivery fee to each country for each model
DI=[
    [800,0,3500,2000],
    [0,1000,2800,1600],
    [12000,0,0,2200],
    [0,0,5000,2500]
]

Dm=[#poland,Italy,US,Sweden
    [75000,35000,40000,2000], #panda
    [20000,40000,50000,50000], #500
    [10000,80000,0,1000],#musa
    [0,8000,3000,1000] #giulia
]

price = [
    [86000,106000,150000,112000],
    [92000,136000,170000,150000],
    [100000,150000,0,170000],
    [0,427000,550000,500000]
]


tax=[
    [0.3,0.3,0.325,0.3],   #panda
    [0.15,0.15,0.175,0.15],#500
    [0.2,0.2,0.225,0.2],   #Musa
    [0.3,0.3,0.325,0.3]    #Giulia
]
models = ['Panda','500','Musa','Giulia']


carprices=[106000,136000,150000,427000]
materials = [0.57, 0.6, 0.55, 0.45] #models
salaries_per_month = [20000, 11000, 20000, 26000]
manhours = [40,45,38,100]


cost=[[0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]]
#actual demand
# x = [[0, 0, 0, 0],
#      [0, 0, 0, 0],
#      [0, 0, 0, 0],
#      [0, 0, 0, 0]]

# define decision variables，x[i][j]
x = [[0 for _ in range(4)] for _ in range(4)]  # initialize variable matrix
profit_per_model_percountry=[[0 for _ in range(4)] for _ in range(4)]
profit_per_model=[0,0,0,0]
total_profit = 0
total_cost = 0
for i in range(4):
    for j in range(4):
        if Dm[i][j] > 0:
            # x[i][j] = m.addVar(countries, cars, name=f"deliveries,x{i+1}{j+1}", vtype=GRB.INTEGER,lb=Dm[i][j])
            x[i][j] = m.addVar(name=f"deliveries_x{i + 1}{j + 1}", vtype=GRB.INTEGER, lb=Dm[i][j])
            cost[i][j] = (carprices[i]*materials[i] + round(manhours[i]*salaries_per_month[i]/160) + DI[i][j])  # profit per model  每个车型利润= (价格-运费 -人工-材料)*数量
            profit_per_model_percountry[i][j] = (price[i][j] - cost[i][j])*(1-tax[i][j])
            profit_per_model[i]+= profit_per_model_percountry[i][j] * x[i][j]
            total_cost+= cost[i][j]





# constrains: different countries demand should be satisfied
m.addConstr(total_cost<=40000000000)

for i in range(4):
    for j in range(4):
        if Dm[i][j] > 0:
            m.addConstr(x[i][j] >= Dm[i][j], name=f"demand_{i}_{j}")

# target objective function: delivery fee/countries * demand/countries
m.setObjective(total_profit,GRB.MAXIMIZE)
#
m.optimize()

# output result
for i in range(4):
    for j in range(4):
        print(f"Deliveries of {cars[i]} to {countries[j]}: {x[i][j]}")


