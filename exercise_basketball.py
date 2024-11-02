from gurobipy import *
from nltk.misc.sort import quick

m = Model("team players")
# player = [x1,x2,x3,x4,x5,x6,x7]
Defense = [3,2,2,1,2,3,1]
p=[12, 10, 9, 8, 11, 12, 7]  # 示例得分数据
s = [10, 15, 12, 9, 8, 10, 13]  # 投篮得分
r = [11, 9, 13, 10, 12, 14, 8]
player = m.addVars(7,vtype=GRB.BINARY, name= "players")
#set constrain
m.addConstr(quicksum(player[i] for i in range(7)) <=5, name="total player" )
m.addConstr((p[j]*player[j]  for j in range(7)) >=10,name = "average passing score")
m.addConstr((s[j]*player[j]for j in range(7))  >=10 ,name = "average shots score")
m.addConstr((r[j]*player[j] for j in range(7)) >=10 ,name = "average rebound score")

m.addConstr( quicksum(player[0]+player[2]+player[4]+player[6]) >=3)
m.addConstr(quicksum(player[2]+player[4]+player[6]) >=2)
m.addConstr(quicksum(player[1]+player[3]+player[5])>=1)
m.addConstr(player[2]+player[5] <=1 )
m.addConstr(2*player[0] >= player[3]+player[4])
m.addConstr(player[1]+player[2]>=1)
m.addConstr(player[1]+player[6] >= 2*player[3])


#set objective function
m.setObjective((quicksum(p[i]*d[i])for i in range(7)) , GRB.MAXIMIZE)