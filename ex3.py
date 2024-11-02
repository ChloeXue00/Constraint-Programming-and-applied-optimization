from pickletools import optimize

from z3 import *
#create model
s= Model('model')

star = ['far','york','earhart']
Colonies= ['Tri','NewBerlin','Str','Vega']

supply=Int('Supply')
demand = Int('Demand')

s.add(supply[:]<=[35,40,50])
s.add(demand <= [20,30,30,45])


x= Model('model')
F =['corn','milk','']
N= ['vitaminA','']
x.add()

