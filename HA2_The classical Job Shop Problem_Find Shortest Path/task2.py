from read_job_scheduling_data import *
from floor_layout import *
from Graph import *
from typing import List, Tuple
import heapq
import math

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

    def heuristic(self, node1, node2):
        # Manhattan distance as heuristic
        # print("here")
        # print(node1.name)
        # print(node1.coordinates)
        # print(node2)
        # x1, y1 = node1.coordinates['x'], node1.coordinates['y']
        # x2, y2 = node2.coordinates['x'], node2.coordinates['y']
        x1, y1 = node1.coordinates[0], node1.coordinates[1]
        x2, y2 = node2.coordinates[0], node2.coordinates[1]
        # x1, y1 = node1.coordinates
        # x2, y2 = node2.coordinates
        return abs(float(x1) - float(x2)) + abs(float(y1) - float(y2))

    def astar(self, start, goal):
        open_list = [(0, start)]  # Priority queue of nodes to explore (f-score, node)
        came_from = {}  # To reconstruct the path
        g_score = {node: float('inf') for node in self.nodes}
        g_score[start] = 0
        f_score = {node: float('inf') for node in self.nodes}
        f_score[start] = g_score[start] + self.heuristic(start, goal)

        while open_list:
            # Get the node with the lowest f-score
            open_list.sort(key=lambda x: x[0])
            current = open_list.pop(0)[1]

            if current == goal:
                # Reconstruct the path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                # print("here291:",path)
                return f_score[goal],path

            neighbors = self.get_neighbors(current)
            for neighbor, weight in neighbors:
                tentative_g_score = g_score[current] + weight
                if tentative_g_score < g_score[neighbor]:
                    # This path is better
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    open_list.append((f_score[neighbor], neighbor))
        # print("here303")
        return None, float('inf')  # No path found
    
#floor layout
from Graph import Node, Edge, Graph


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
    "edge_4W_4":Edge(node4W, node4, 21), "edge_4_1N":Edge(node4, node1N, 45), "edge_1N_6W":Edge(node1N, node6W, 18), "edge_6W_6":Edge(node6W, node6, 28),
    "edge_5NW_5N":Edge(node5NW, node5N, 21), "edge_5N_1W":Edge(node5N, node1W, 25), "edge_1W_1":Edge(node1W, node1, 20), "edge_1_1E":Edge(node1, node1E, 18), "edge_1E_DN":Edge(node1E, nodeDN, 28),
    "edge_W_5W":Edge(nodeW, node5W, 7), "edge_5W_5":Edge(node5W, node5, 21), "edge_5_5E":Edge(node5, node5E, 25), "edge_1S_3N":Edge(node1S, node3N, 18), "edge_3N_3NE":Edge(node3N, node3NE, 28), "edge_3NE_D":Edge(node3NE, nodeD, 8),
    "edge_BN_5S":Edge(nodeBN, node5S, 21), "edge_2_2E":Edge(node2, node2E, 20), "edge_3_3E":Edge(node3, node3E, 28), 
    "edge_B_BE":Edge(nodeB, nodeBE, 21), "edge_BE_2S":Edge(nodeBE, node2S, 25), "edge_2S_3S":Edge(node2S, node3S, 38), "edge_3S_3SE":Edge(node3S, node3SE, 28), 
    
    "edge_4W_5NW":Edge(node4W, node5NW, 19), "edge_1N_1":Edge(node1N, node1, 19), "edge_6W_1E":Edge(node6W, node1E, 19), 
    "edge_5NW_5W":Edge(node5NW, node5W, 17), "edge_5N_5":Edge(node5N, node5, 17), "edge_1W_5E":Edge(node1W, node5E, 17), "edge_1_1S":Edge(node1, node1S, 17), "edge_1E_3N":Edge(node1E, node3N, 17), "edge_DN_3NE":Edge(nodeDN, node3NE, 17), 
    "edge_5W_BN":Edge(node5W, nodeBN, 17), "edge_5E_2":Edge(node5E, node2, 17), "edge_1S_2E":Edge(node1S, node2E, 17), "edge_3N_3":Edge(node3N, node3, 17), "edge_3NE_3E":Edge(node3NE, node3E, 17), 
    "edge_BN_B":Edge(nodeBN, nodeB, 17), "edge_5S_BE":Edge(node5S, nodeBE, 17), "edge_2_2S":Edge(node2, node2S, 17), "edge_3_3S":Edge(node3, node3S, 17), "edge_3E_3SE":Edge(node3E, node3SE, 17)
    }

node_names = [name for name, _ in nodes.items()]
node_list = [node for _, node in nodes.items()]

edge_names = [name for name, _ in edges.items()]
edge_list = [edge for _, edge in edges.items()]

shop_floor = Graph(node_list, edge_list)


def read_job_scheduling_data(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Extract n and m values from the first line
            if not lines:
                raise ValueError("File is empty")
            try:
                n, m = map(int, lines[0].split())
            except ValueError:
                raise ValueError("First line should contain two integers representing n and m")
            # Extract n and m values from the first line
            # n, m = map(int, lines[0].split())

            # Initialize lists for times and machines
            times = []
            machines = []

            # Read the remaining lines and extract times and machines data
            for line in lines[1:]:
                data = list(map(int, line.split()))
                if len(data) % 2 != 0:
                    raise ValueError("Each job line must have an even number of integers")
                machine_process_pairs = [(data[i], data[i + 1]) for i in range(0, len(data), 2)]
                machines.append([pair[0] for pair in machine_process_pairs])
                times.append([pair[1] for pair in machine_process_pairs])

            return n, m, times, machines
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except ValueError as ve:
        print(f"Error: {ve}")
        return None



# print(shop_floor)
def task2():
    speed = 5.0                   

    file_path = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft06.txt'       
    # Read job scheduling data from the specified file
    n, m, times, machines = read_job_scheduling_data(file_path)
    for job in machines:
        job.insert(0, "W")
        job.insert(len(job), "D")
    print(machines)
    
    # For all the jobs in the list find shortest path between machines
    machine_pairs_list = []
    distances_list = []
    paths_list = []
    time_required_list = []
    for machine_sequence in machines:
        machine_pairs = [(machine_sequence[i], machine_sequence[i+1]) for i in range(0, len(machine_sequence) - 1)]
        distances = []
        paths = []
        for start, end in machine_pairs:
            dist, path = shop_floor.astar(machine_node[start], machine_node[end])
            distances.append(dist)
            # print("here29",path)
            paths.append([node.name for node in path])
        distances_list.append(distances)
        time_required_list.append([d/speed for d in distances])
        paths_list.append(paths)
        machine_pairs_list.append(machine_pairs)
    
    # print the data to stdout
    for i in range(len(distances_list)):
        print("---------- ----------")
        print("machine_pairs_list[{}] = {}".format(i, machine_pairs_list[i]))
        print("time_required_list[{}] = {}".format(i, time_required_list[i]))
        print("paths_list[{}] = {}".format(i, paths_list[i]))
        print("distances_list[{}] = {}".format(i, distances_list[i]))
    print("---------- ----------")
    print(">>>> NOTE: in above output, machine number indexing starts from 0. <<<<")


def calculate_all_shortest_paths():
    # get all nodes in plant
    node_names = list(machine_node.keys())  
    
    #  store shortest path and dist
    all_pairs_shortest_paths = []
    
    for i in range(len(node_names)):
        for j in range(i + 1, len(node_names)):
            start_node = machine_node[node_names[i]]
            end_node = machine_node[node_names[j]]
            
            # shortest path from start_node to end_node 
            dist, path = shop_floor.astar(start_node, end_node)
            
            # record paths if find one
            if path:
                all_pairs_shortest_paths.append({
                    "start": start_node.name,
                    "end": end_node.name,
                    "distance": dist,
                    "path": [node.name for node in path]
                })
    
    #  shortest path for each pair
    print("Shortest paths between all pairs of points in the plant:")
    for entry in all_pairs_shortest_paths:
        print(f"From {entry['start']} to {entry['end']}:")
        print(f"  Distance: {entry['distance']}")
        print(f"  Path: {' -> '.join(entry['path'])}")
        print("-" * 40)

# calculate all path
calculate_all_shortest_paths()


#job scheduling
file_name = 'C:\\Users\\xuefx\\PycharmProjects\\coppc\\ft06.txt'

file_path = file_name
n, m, times, machines = read_job_scheduling_data(file_path)

# print the data to stdout
print("n = {}".format(n))       # jobs (row count)
print("m = {}".format(n))       # machines (column count)
print("machines = {}".format(machines))
print("times = {}".format(times))

# task2()