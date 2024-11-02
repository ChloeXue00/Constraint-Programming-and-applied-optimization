from z3 import *



from queue import PriorityQueue

class Node:
    def __init__(self, name, coordinates):
        self.name = name  # Node identifier, like 'Warehouse', 'Machine 1', 'Delivery'
        self.coordinates = coordinates  # Coordinates on the grid

class Edge:
    def __init__(self, start, end, weight):
        self.start = start  # Start node
        self.end = end  # End node
        self.weight = weight  # Distance between nodes

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # List of Node objects
        self.edges = edges  # List of Edge objects

    def get_neighbors(self, node):
        # Find all neighboring nodes for the given node
        neighbors = []
        for edge in self.edges:
            if edge.start == node:
                neighbors.append((edge.end, edge.weight))
            elif edge.end == node:
                neighbors.append((edge.start, edge.weight))
        return neighbors


# 
def heuristic(node, goal, node_coords):
    x1, y1 = node_coords[node]
    x2, y2 = node_coords[goal]
    return abs(x1 - x2) + abs(y1 - y2)

# 
def a_star(graph, start, goal, node_coords):
    pq = PriorityQueue()
    pq.put((0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal, node_coords)

    while not pq.empty():
        current = pq.get()[1]

        if current == goal:
            # 
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor, weight in graph[current]:
            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal, node_coords)
                pq.put((f_score[neighbor], neighbor))

    return None

# 
graph = {
    'node5': [('node5E', 25), ('node5W', 21), ('node5S', 17), ('node5N', 21)],
    'node5E': [('node5', 25), ('node2', 17)],
    'node5W': [('node5', 21), ('nodeBN', 17)],
    'node5N': [('node5', 21), ('node1W', 25)],
    'node5S': [('node5', 17), ('nodeBN', 21)],
    'nodeBN': [('node5S', 21), ('node5W', 17), ('nodeB', 17)],
    'node1W': [('node1', 20), ('node5N', 25)],
    'node1': [('node1W', 20), ('node1E', 18), ('node1S', 17)],
    'node1E': [('node1', 18), ('nodeDN', 28)],
    'node1S': [('node1', 17), ('node2E', 17)],
    'node2': [('node5E', 17), ('node2E', 20), ('node3', 72)],
    'node2E': [('node2', 20), ('node1S', 17)],
    'node3': [('node2', 72), ('node3N', 17)],
    'node3N': [('node3', 17), ('node3NE', 28)],
    'node3NE': [('node3N', 28), ('nodeD', 8)],
}

node_coords = {
    'node5': (28, 34), 'node5E': (53, 34), 'node5W': (7, 34), 'node5N': (28, 51), 'node5S': (28, 17),
    'nodeBN': (7, 17), 'node1W': (53, 51), 'node1': (73, 51), 'node1E': (91, 51), 'nodeDN': (119, 51),
    'node1S': (73, 34), 'node2': (53, 17), 'node2E': (73, 17), 'node3': (91, 17), 'node3N': (91, 34),
    'node3NE': (119, 34), 'nodeD': (127, 34)
}


node4W = Node("node4W", (7, 70))
node4 = Node("node4", (28, 70))
node1N = Node("node1N", (73, 70))
node6W = Node("node6W", (91, 70))
node6 = Node("node6", (119, 70))

node5NW = Node("node5NW", (7, 51))
node5N = Node("node5N", (28, 51))
node1W = Node("node1W", (53, 51))
node1 = Node("node1", (73, 51))
node1E = Node("node1E", (91, 51))
nodeDN = Node("nodeDN", (119, 51))

nodeW = Node("nodeW", (0, 34))
node5W = Node("node5W", (7, 34))
node5 = Node("node5", (28, 34))
node5E = Node("node5E", (53, 34))
node1S = Node("node1S", (73, 34))
node3N = Node("node3N", (91, 34))
node3NE = Node("node3NE", (119, 34))
nodeD = Node("nodeD", (127, 34))

nodeBN = Node("nodeBN", (7, 17))
node5S = Node("node5S", (28, 17))
node2 = Node("node2", (53, 17))
node2E = Node("node2E", (73, 17))
node3 = Node("node3", (91, 17))
node3E = Node("node3E", (119, 17))

nodeB = Node("nodeB", (7, 0))
nodeBE = Node("nodeBE", (28, 0))
node2S = Node("node2S", (53, 0))
node3S = Node("node3S", (91, 0))
node3SE = Node("node3SE", (119, 0))

machine_node = {"W":nodeW, 0:node1, 1:node2, 2:node3, 3:node4, 4:node5, 5:node6, "D":nodeD}

nodes = {
    "node4W":node4W, "node4":node4, "node1N":node1N, "node6W":node6W, "node6":node6,
    "node5NW":node5NW, "node5N":node5N, "node1W":node1W, "node1":node1, "node1E":node1E, "nodeDN":nodeDN,
    "nodeW":nodeW, "node5W":node5W, "node5":node5, "node5E":node5E, "node1S":node1S, "node3N":node3N, "node3NE":node3NE, "nodeD":nodeD,
    "nodeBN":nodeBN, "node5S":node5S, "node2":node2, "node2E":node2E, "node3":node3, "node3E":node3E,
    "nodeB":nodeB, "nodeBE":nodeBE, "node2S":node2S, "node3S":node3S, "node3SE":node3SE
    }
edges = {
    "edge_4W_4": Edge(node4W, node4, 21), "edge_4_1N": Edge(node4, node1N, 45), "edge_1N_6W": Edge(node1N, node6W, 18),
    "edge_6W_6": Edge(node6W, node6, 28),
    "edge_5NW_5N": Edge(node5NW, node5N, 21), "edge_5N_1W": Edge(node5N, node1W, 25),
    "edge_1W_1": Edge(node1W, node1, 20), "edge_1_1E": Edge(node1, node1E, 18), "edge_1E_DN": Edge(node1E, nodeDN, 28),
    "edge_W_5W": Edge(nodeW, node5W, 7), "edge_5W_5": Edge(node5W, node5, 21), "edge_5_5E": Edge(node5, node5E, 25),
    "edge_1S_3N": Edge(node1S, node3N, 18), "edge_3N_3NE": Edge(node3N, node3NE, 28),
    "edge_3NE_D": Edge(node3NE, nodeD, 8),
    "edge_BN_5S": Edge(nodeBN, node5S, 21), "edge_2_2E": Edge(node2, node2E, 20), "edge_3_3E": Edge(node3, node3E, 28),
    "edge_B_BE": Edge(nodeB, nodeBE, 21), "edge_BE_2S": Edge(nodeBE, node2S, 25),
    "edge_2S_3S": Edge(node2S, node3S, 38), "edge_3S_3SE": Edge(node3S, node3SE, 28),

    "edge_4W_5NW": Edge(node4W, node5NW, 19), "edge_1N_1": Edge(node1N, node1, 19),
    "edge_6W_1E": Edge(node6W, node1E, 19),
    "edge_5NW_5W": Edge(node5NW, node5W, 17), "edge_5N_5": Edge(node5N, node5, 17),
    "edge_1W_5E": Edge(node1W, node5E, 17), "edge_1_1S": Edge(node1, node1S, 17),
    "edge_1E_3N": Edge(node1E, node3N, 17), "edge_DN_3NE": Edge(nodeDN, node3NE, 17),
    "edge_5W_BN": Edge(node5W, nodeBN, 17), "edge_5E_2": Edge(node5E, node2, 17),
    "edge_1S_2E": Edge(node1S, node2E, 17), "edge_3N_3": Edge(node3N, node3, 17),
    "edge_3NE_3E": Edge(node3NE, node3E, 17),
    "edge_BN_B": Edge(nodeBN, nodeB, 17), "edge_5S_BE": Edge(node5S, nodeBE, 17), "edge_2_2S": Edge(node2, node2S, 17),
    "edge_3_3S": Edge(node3, node3S, 17), "edge_3E_3SE": Edge(node3E, node3SE, 17)
}
edge_weights = {"edge_4W_4": 21, "edge_4_1N": 45, "edge_1N_6W": 18, "edge_6W_6": 28,
                "edge_5NW_5N": 21, "edge_5N_1W": 25, "edge_1W_1": 20, "edge_1_1E": 18, "edge_1E_DN": 28,
                "edge_W_5W": 7, "edge_5W_5": 21, "edge_5_5E": 25, "edge_1S_3N": 18, "edge_3N_3NE": 28, "edge_3NE_D": 8,
                "edge_BN_5S": 21, "edge_2_2E": 20, "edge_3_3E": 28,
                "edge_B_BE": 21, "edge_BE_2S": 25, "edge_2S_3S": 38, "edge_3S_3SE": 28,

                "edge_4W_5NW": 19, "edge_5NW_5W": 17, "edge_5W_BN": 17, "edge_BN_B": 17,
                "edge_5N_5": 17, "edge_5S_BE": 17,
                "edge_1W_5E": 17, "edge_5E_2": 17, "edge_2_2S": 17,
                "edge_1N_1": 19, "edge_1_1S": 17, "edge_1S_2E": 17,
                "edge_6W_1E": 19, "edge_1E_3N": 17, "edge_3N_3": 17, "edge_3_3S": 17,
                "edge_DN_3NE": 17, "edge_3NE_3E": 17, "edge_3E_3SE": 17, }

node_names = [name for name, _ in nodes.items()]
node_list = [node for _, node in nodes.items()]

edge_names = [name for name, _ in edges.items()]
edge_list = [edge for _, edge in edges.items()]
weight = [weight for _ in edge_weights]
edge_vars = {edge_name: Bool(edge_name) for edge_name in edges_weights}
# 
# print("Edge variables created for Z3 solver:")
# for edge_name, var in edge_vars.items():
#     print(f"{edge_name}: {var}")

node_to_edges = {}
for edge_name, edge in edges.items():
    # 
    if edge.start not in node_to_edges:
        node_to_edges[edge.start] = []
    node_to_edges[edge.start].append(edge_name)

    # 
    if edge.end not in node_to_edges:
        node_to_edges[edge.end] = []
    node_to_edges[edge.end].append(edge_name)

# 
for node, edges in node_to_edges.items():
    print(f"{node}: {edges}")
solver = Solver()

# containt node5 
node5_edges = node_to_edges['node5']
solver.add(Sum([edge_vars[edge] for edge in node5_edges]) == 1)

# constraint node3 edge 
node3_edges = node_to_edges['node3']
solver.add(Sum([edge_vars[edge] for edge in node3_edges]) == 1)

# check solver 
if solver.check() == sat:
    model = solver.model()
    print("Solution found:")
    for edge_name in edge_vars:
        if model.eval(edge_vars[edge_name]):
            print(f"Edge {edge_name} is part of the path.")
else:
    print("No solution found.")



#
# # node5 to node3

def find_paths(graph, start, goal, node_coords, max_paths=10):
    solver = Solver()
    path_count = 0
    while path_count < max_paths:
        path = a_star(graph, start, goal, node_coords)
        if path is None:
            break
        # output path
        print(f"Path {path_count + 1}: {path}")
        total_weight = sum([graph[path[i]][j][1] for i in range(len(path) - 1) for j in range(len(graph[path[i]])) if graph[path[i]][j][0] == path[i + 1]])
        print(f"Total weight: {total_weight}")

        # add constraint to pass current found path 
        path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
        solver.add(Or([Not(And(edge_vars[edge])) for edge in path_edges]))
        path_count += 1

    if path_count == 0:
        print("No paths found.")

# search
find_paths(graph, 'node5', 'node3', node_coords)
