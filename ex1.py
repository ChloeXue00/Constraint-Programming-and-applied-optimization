from pickletools import optimize

# from boto.sdb.db.model import Model

# from pickletools import optimize

# S=Model('model')
#create model
from z3 import *
from gurobipy import *

s= Optimize()
# add variables
x = Int("x")
y = Int("y")
z = Int("z")

obj = Int("obj")
#add constrains
s.add(x+2*y+3*z <=4)
s.add(x+y >=1)

s.add(x<=1,y<=1,z<=1)
s.add(obj == x+y+2*z)
s.maximize(obj)


s.check()
print(s.model())

