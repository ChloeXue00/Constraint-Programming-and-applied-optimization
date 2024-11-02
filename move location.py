from astropy.wcs.docstrings import ctype
from gurobipy import *

from task2 import budget

m= Model("model")

location_cost = [c1,c2,c3]  # cost on locations
m.addVars(location_cost,vtype=GRB.CONTINUOUS,name = "location_cost")
totalbudget= b0
m.addVar(totalbudget,vtype=GRB.CONTINUOUS)
man_cost = [c4,c5,c6]
m.addVar(man_cost,vtype=GRB.BATCH_COMPLETED,name = "man cost")
employee = [e1,e2,e3]
m.addVar(employee,vtype =GRB.BINARY)
m.addConstr(man_cost+ location_cost <= b0)
