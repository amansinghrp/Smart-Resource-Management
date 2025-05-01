# visualization/rag.py

import networkx as nx
import matplotlib.pyplot as plt

def draw(system_state):
    G = nx.DiGraph()

    deadlocked = system_state["deadlocked"]

    # Add process nodes
    for p in system_state["processes"]:
        color = 'red' if p['pid'] in deadlocked else 'blue'
        G.add_node(f"P{p['pid']}", color=color, shape='o')

    # Add resource nodes
    for r in system_state["resources"]:
        G.add_node(f"R{r['rid']}", color='green', shape='s')

    # Add allocation edges (Resource -> Process)
    for p in system_state["processes"]:
        for rid, count in enumerate(p["alloc"]):
            if count > 0:
                G.add_edge(f"R{rid}", f"P{p['pid']}", color='black', style='solid')

    # Add request edges (Process -> Resource)
    for req in system_state["requests"]:
        G.add_edge(f"P{req['pid']}", f"R{req['rid']}", color='red', style='dashed')

    pos = nx.spring_layout(G, seed=42)

    # Draw process nodes
    process_nodes = [n for n in G.nodes if n.startswith('P')]
    resource_nodes = [n for n in G.nodes if n.startswith('R')]

    process_colors = [G.nodes[n]['color'] for n in process_nodes]
    resource_colors = [G.nodes[n]['color'] for n in resource_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=process_nodes, node_color=process_colors, node_shape='o', label="Process")
    nx.draw_networkx_nodes(G, pos, nodelist=resource_nodes, node_color=resource_colors, node_shape='s', label="Resource")

    # Draw edges
    edge_colors = [G[u][v]['color'] for u,v in G.edges]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)

    # Draw labels
    nx.draw_networkx_labels(G, pos)

    # Setup legend
    blue_patch = plt.Line2D([0], [0], marker='o', color='w', label='Process', markerfacecolor='blue', markersize=10)
    green_patch = plt.Line2D([0], [0], marker='s', color='w', label='Resource', markerfacecolor='green', markersize=10)
    red_patch = plt.Line2D([0], [0], marker='o', color='w', label='Deadlocked Process', markerfacecolor='red', markersize=10)

    plt.legend(handles=[blue_patch, green_patch, red_patch])
    plt.title("Resource Allocation Graph (RAG)")
    plt.axis('off')
    plt.savefig('rag_visualization.png')

