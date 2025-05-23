import matplotlib.pyplot as plt
import networkx as nx
from process import Process
from system import System

# Initialize system with total resources
system = System([2, 1])  # R0 has 2, R1 has 1

# Create processes with their max needs
p0 = Process(0, [1, 1])
p1 = Process(1, [1, 1])

# Add processes to the system
system.add_process([1, 1])
system.add_process([1, 1])

# Simulate allocations and requests
p0.allocate([1, 0])  # P0 holds R0
p1.request([0, 1])   # P1 is requesting R1

# Create Resource Allocation Graph
G = nx.DiGraph()

# Add resource and process nodes
G.add_node("R0", shape="s", color='lightblue')
G.add_node("R1", shape="s", color='lightblue')
G.add_node("P0", shape="o", color='lightgreen')
G.add_node("P1", shape="o", color='lightgreen')

# Allocation edges: R -> P (R resources are allocated to P processes)
if p0.allocation[0] > 0:
    G.add_edge("R0", "P0", label="alloc", color='green')  # Green for allocation
if p1.allocation[0] > 0:
    G.add_edge("R0", "P1", label="alloc", color='green') 
if p0.allocation[1] > 0:
    G.add_edge("R1", "P0", label="alloc", color='green') 
if p1.allocation[1] > 0:
    G.add_edge("R1", "P1", label="alloc", color='green') 

# Request edges: P -> R (P processes request R resources)
if p0.requested[0] > 0:
    G.add_edge("P0", "R0", label="req", color='red')  # Red for requests
if p1.requested[0] > 0:
    G.add_edge("P1", "R0", label="req", color='red') 
if p0.requested[1] > 0:
    G.add_edge("P0", "R1", label="req", color='red') 
if p1.requested[1] > 0:
    G.add_edge("P1", "R1", label="req", color='red') 

# Draw graph
pos = nx.spring_layout(G)

edge_labels = nx.get_edge_attributes(G, 'label')
edge_colors = [G[u][v]['color'] for u, v in G.edges()]

nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightgray', font_size=12, edge_color=edge_colors, width=2)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.savefig('resource_allocation_graph.png', format='png')
