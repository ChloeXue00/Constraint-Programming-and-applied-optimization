from typing import List, Tuple

class Node:
    name = None
    data = None

    # Constructor (init method)
    def __init__(self, name:[str, None]=None, data=None):
        self.name = name
        self.data = data
    
    def __str__(self) -> str:
        return "<{}, {}>".format(self.name, self.data)
    
    # Property Access
    def getName(self):
        return self.name
    
    def getData(self):
        return self.data
    
    def setName(self, name):
        self.name = name
    
    def setData(self, data):
        self.data = data

class Edge:
    start = None
    end = None
    weight = '-'
    isUniDirectional = False

    # Constructor (init method)
    def __init__(self, start:[Node, None]=None, end:[Node, None]=None, weight:['-', int, float]='-', isUniDirectional:bool=False):
        self.start = start
        self.end = end
        self.weight = weight
        self.isUniDirectional = isUniDirectional
    
    def __str__(self) -> str:
        if self.isUniDirectional:
            fmt_str = "{} --{}--> {}".format(self.start, self.weight, self.end)
        else:
            fmt_str = "{} --{}-- {}".format(self.start, self.weight, self.end)
        return fmt_str
    
    # Property Access
    def getStartNode(self):
        return self.start
    
    def getEndNode(self):
        return self.end
    
    def getWeight(self):
        return self.weight
    
    def getisUniDirectional(self):
        return self.isUniDirectional

    def setStartNode(self, start:[Node, None]=None):
        self.start = start
    
    def setEndNode(self, end:[Node, None]=None):
        self.end = end
    
    def setWeight(self, weight:['-', int, float]='-'):
        self.weight = weight
    
    def setIsUniDirectional(self, isUniDirectional:bool=False):
        self.isUniDirectional = isUniDirectional

    def flip(self):
        return Edge(self.end, self.start, self.weight, self.isUniDirectional)

class Graph:
    # Class attribute
    nodes = []
    edges = []

    # Constructor (init method)
    def __init__(self, nodes=[], edges=[]):
        self.nodes = nodes
        for edge in edges:
            self.edges.append(edge)
            if not edge.isUniDirectional:
                self.edges.append(edge.flip())
    
    def __str__(self):
        # Create a string to represent the graph
        graph_str = "Nodes:\n"
        for node in self.nodes:
            graph_str += f"{node}\n"
        
        graph_str += "\nEdges:\n"
        for edge in self.edges:
            graph_str += f"{edge}\n"
        
        return graph_str
    
    def get_edges_for(self, node:Node) -> list:
        return [edge for edge in self.edges if (edge.start == node) or (edge.end == node)]
    
    # TODO: Must do like this in future for shortest path and its heuristic...
    # from typing import Callable, List, Union
    # def shortest_path_between(self, start:Node, end:Node, shortest_path_algorithm:callable[Union[List[Node], List[Edge], Node, Node], Union[int, List[Node]]]):
    #     return shortest_path_algorithm(self.nodes, self.edges, start, end)
    
    def default_heuristic(self, end:Node, node:Node) -> float:
        # Replace this with an appropriate heuristic function (e.g., Manhattan, Euclidean, etc.)
        # return 0  # Here, we consider no heuristic information, i.e. dijkstra
        return abs(end.data["x"] - node.data["x"]) + abs(end.data["y"] - node.data["y"])  # Here, we consider Manhattan
    
    # Other methods
    def astar(self, start:Node, end:Node, heuristic:callable=default_heuristic) -> Tuple[int, List[Node]]:
        # Initialize data structures
        open_list = [(float(0), start)]   # Priority queue for nodes to explore
        closed_set = set()                # Set of visited nodes

        # g and f scores are stored as dictionary
        g_scores = {node: float('inf') for node in self.nodes}  # Cost from start to each node
        f_scores = {node: float('inf') for node in self.nodes}  # Estimated total cost from start to end through node
        g_scores[start] = 0                                # since distance covered from start to start is zero
        f_scores[start] = g_scores[start] + heuristic(self, end, start)
        
        parent_map = {}           # Parent pointers to reconstruct the path

        while open_list:
            open_list.sort(key=lambda x: x[0])  # Sort the open list by f_score
            _, current_node = open_list.pop(0)  # Get the node with the lowest f_score

            if current_node == end:
                # Reconstruct the path from end to start
                path = []
                while current_node:
                    path.insert(0, current_node)                   # Insert at the beginning to maintain order
                    current_node = parent_map.get(current_node)    # Move to the parent node
                return g_scores[end], path

            closed_set.add(current_node)

            # Explore neighbors of the current node
            for edge in self.edges:
                if edge.start == current_node and edge.end not in closed_set:
                    # Calculate the tentative g_score f_score for the neighbor
                    tentative_g_score = g_scores[current_node] + edge.weight
                    tentative_f_score = tentative_g_score + heuristic(self, end, edge.end)
                    
                    if tentative_f_score < f_scores[edge.end]:
                        # Update the parent and g_score and f_score for the neighbor
                        parent_map[edge.end] = current_node
                        g_scores[edge.end] = tentative_g_score
                        f_scores[edge.end] = tentative_f_score

                        # Add the neighbor to the open list for further exploration
                        open_list.append((tentative_f_score, edge.end))

# Usage:
if __name__ == "__main__":
    # Define nodes and edges
    node1 = Node("A")
    node2 = Node("B")
    node3 = Node("C")
    node4 = Node("D")

    edge1 = Edge(node1, node2, 1)
    edge2 = Edge(node2, node3, 2)
    edge3 = Edge(node1, node4, 3)
    edge4 = Edge(node1, node3, 5)
    edge5 = Edge(node4, node3, 1)

    nodes = [node1, node2, node3, node4]
    edges = [edge1, edge2, edge3, edge4, edge5]

    start_node = node1
    end_node = node3

    graph = Graph(nodes, edges)
    print(graph)
    
    # Find the shortest path using A* algorithm
    total_cost, path = graph.astar(start_node, end_node)

    if path:
        print("Shortest path:", [str(node) for node in path])
        print("Total cost:", total_cost)
    else:
        print("No path found.")
