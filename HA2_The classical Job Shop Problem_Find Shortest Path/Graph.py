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
    

# if __name__ == "__main__":
#     # Define nodes and edges
#     # node1 = Node("A")
#     # node2 = Node("B")
#     # node3 = Node("C")
#     # node4 = Node("D")
#     node1 = Node("A", (0, 0))
#     node2 = Node("B", (1, 0))


#     edge1 = Edge(node1, node2, 1)
   

#     nodes = [node1, node2, node3, node4]
#     edges = [edge1, edge2, edge3, edge4, edge5]

#     start_node = node1
#     end_node = node3

#     graph = Graph(nodes, edges)
#     print(graph)