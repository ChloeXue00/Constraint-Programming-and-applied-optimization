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
