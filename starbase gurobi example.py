from operator import index

from gurobipy import *

starbase =['Farpoint', 'Yorktown','Earhart']
spacecolonies=['Triacus','NewBerlin','Strnad','Vega']
demand =[20,30,30,45]
supply=[35,40,45]
transCost=[[6,9,10,8],[9,5,16,14],[12,7,13,9]]

#set model
m= Model('facility')

#set decision variables
x= m.addVars(starbase,spacecolonies,vtype=GRB.BINARY,name='x')

#constrains
m.addConstrs(
    sum(x[i,j] for j in spacecolonies) <= supply[index]
    for index, i in enumerate(starbase)
)

m.addConstrs(
    sum(x[i,j] for i in starbase) >= demand[index]
    for index, j in enumerate(spacecolonies)
)
#set objective function
m.setObjective(
    sum(
        x[i,j]*transCost[index_i][index_j]
        for index_i, i in enumerate(starbase)
        for index_j, j in enumerate(spacecolonies)
    )
)

m.optimize()
