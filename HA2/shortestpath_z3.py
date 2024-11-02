from z3 import *

# Define Boolean variables for each node (A, B, C,..., I)
nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
node_vars = {node: Bool(node) for node in nodes}

# Define Boolean variables for each edge (a, b, c,..., l)
edges = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']
edge_vars = {edge: Bool(edge) for edge in edges}

# Define edge weights
weights = {
    'a': 2, 'b': 2, 'c': 3, 'd': 4, 'e': 2,
    'f': 1, 'g': 2, 'h': 3, 'i': 1, 'j': 1,
    'k': 1, 'l': 1
}

# Create a Z3 solver instance
solver = Optimize()

# Source (I) and destination (H) constraints
solver.add(edge_vars['a'] + edge_vars['b'] + edge_vars['c'] == 1)  # I's edges
solver.add(edge_vars['h'] + edge_vars['k'] + edge_vars['l'] + edge_vars['g'] == 1)  # H's edges

# Intermediate node constraints (2*A+a+d+e = 2) for A and similar for others
solver.add(2 * node_vars['A'] == edge_vars['a'] + edge_vars['d'] + edge_vars['e'])  # Node A
solver.add(2 * node_vars['B'] == edge_vars['b'] + edge_vars['e'] + edge_vars['f'])  # Node B
solver.add(2 * node_vars['C'] == edge_vars['c'] + edge_vars['f'] + edge_vars['g'])  # Node C
solver.add(2 * node_vars['D'] == edge_vars['d'] + edge_vars['h'])  # Node D
solver.add(2 * node_vars['E'] == edge_vars['e'] + edge_vars['i'] + edge_vars['j'])  # Node E
solver.add(2 * node_vars['F'] == edge_vars['f'] + edge_vars['g'] + edge_vars['j'] + edge_vars['l'])  # Node F
solver.add(2 * node_vars['G'] == edge_vars['h'] + edge_vars['i'] + edge_vars['k'])  # Node G
# solver.add(If(A, a + d + e == 2, a + d + e == 0))
# solver.add(If(B, b + f == 2, b  + f == 0))
# solver.add(If(C, c + g == 2, c  + g == 0))
# solver.add(If(D, d + h == 2, d  + h == 0))
# solver.add(If(H, h + k +l + g == 2, h + k +l + g == 0))
# solver.add(If(E, e + i == 2, e + i  == 0))
# solver.add(If(F, f + l == 2, f + l  == 0))
# solver.add(If(G, i + k == 2, i + k  == 0))

#
# node_vars = {
#     'A': Bool('A'), 'B': Bool('B'), 'C': Bool('C'),
#     'D': Bool('D'), 'E': Bool('E'), 'F': Bool('F'),
#     'G': Bool('G'), 'H': Bool('H'), 'I': Bool('I')
# }

# edge_vars = {
#     'a': Bool('a'), 'b': Bool('b'), 'c': Bool('c'),
#     'd': Bool('d'), 'e': Bool('e'), 'f': Bool('f'),
#     'g': Bool('g'), 'h': Bool('h'), 'i': Bool('i'),
#     'j': Bool('j'), 'k': Bool('k'), 'l': Bool('l')
# }




# Define the objective: Minimize the total weight of the edges
objective = Sum([If(edge_vars[edge], weights[edge], 0) for edge in edges])
solver.minimize(objective)

# Solve the problem
if solver.check() == sat:
    model = solver.model()
    print("Optimal Path:")
    for edge in edges:
        if model.eval(edge_vars[edge]):
            print(f"Edge {edge} is part of the optimal path.")
    print("Total path cost:", model.eval(objective))
else:
    print("No solution found.")
