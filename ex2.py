from gurobipy import *

m = Model('model')


x=m.addVar(vtype=GRB.BINARY,name = 'x')
y=m.addVar(vtype=GRB.BINARY,name = 'y')
z=m.addVar(vtype=GRB.BINARY,name = 'z')

m.setObjective(x+y+2*z, GRB.MAXIMIZE)

#add constrains
c1 = m.addConstr(x+y >=1)
c2 = m.addConstr(x+2*y+3*z <=4)

#Solve the model
m.optimize()
vars = m.getVars()
for i in vars:
    print(i)

a = [2,1,2,4,55,6,3]


