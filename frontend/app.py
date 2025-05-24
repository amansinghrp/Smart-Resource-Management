import matplotlib
matplotlib.use('Agg')

from flask import Flask, request, jsonify, render_template, send_from_directory
import matplotlib.pyplot as plt
import networkx as nx
import os
from system.system import System
from system.wfg import WFG

app = Flask(__name__)
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_deadlock():
    try:
        data = request.get_json()
        num_processes = data['num_processes']
        resource_totals = data['resource_totals']
        max_needs = data['maximum']
        allocations = data['allocation']

        print("🔍 Received Data:")
        print("Processes:", num_processes)
        print("Resource Totals:", resource_totals)
        print("Max Needs:", max_needs)
        print("Allocations:", allocations)

        system = System(resource_totals)

        for max_need in max_needs:
            system.add_process(max_need)

        for i, alloc in enumerate(allocations):
            system.processes[i].allocate(alloc)
            for j in range(len(alloc)):
                system.resources[j].allocate(alloc[j])
                system.available[j] -= alloc[j]

        is_safe, safe_sequence = system.is_safe()
        deadlocked = []


        wfg = WFG(system)
        wfg.build_graph()
        if not is_safe:
            deadlocked = wfg.detect_deadlock()
        else:
            print("✅ No deadlock detected.")
        # Generate Resource Allocation Graph (RAG)
        G = nx.DiGraph()

        # Add resource and process nodes
        for i in range(len(system.resources)):
            G.add_node(f"R{i}", shape='s', color='lightblue')

        for p in system.processes:
            G.add_node(f"P{p.pid}", shape='o', color='lightgreen')

        # Add allocation edges (R -> P)
        for p in system.processes:
            for r in range(len(p.allocation)):
                if p.allocation[r] > 0:
                    color = 'red' if (not is_safe and p.pid in deadlocked) else 'green'
                    G.add_edge(f"R{r}", f"P{p.pid}", label='alloc', color=color)

        # Add request edges (P -> R)
        for p in system.processes:
            for r in range(len(p.need)):
                if p.need[r] > 0:
                    G.add_edge(f"P{p.pid}", f"R{r}", label='req', color='blue')

        # Draw graph
        pos = nx.spring_layout(G)
        edge_labels = nx.get_edge_attributes(G, 'label')
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]

        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_color='lightgray', node_size=2000, edge_color=edge_colors, width=2, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title("Resource Allocation Graph" if is_safe else "Deadlock Detected in RAG")
        plt.savefig(os.path.join(STATIC_FOLDER, "graph.png"))
        plt.close()

        return jsonify({
            "message": "⚠️ Deadlock detected!" if not is_safe else "✅ No deadlock detected.",
            "deadlocked_processes": [f"P{pid}" for pid in deadlocked],
            "safe_sequence": [f"P{pid}" for pid in safe_sequence] if is_safe else [],
            "graph_url": "/graph"
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/graph')
def get_graph():
    return send_from_directory(STATIC_FOLDER, "graph.png")

if __name__ == '__main__':
    app.run(debug=True)
