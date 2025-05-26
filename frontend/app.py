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
        terminated_processes = data.get('terminated_processes', [])

        print("🔍 Received Data:")
        print("Processes:", num_processes)
        print("Resource Totals:", resource_totals)
        print("Max Needs:", max_needs)
        print("Allocations:", allocations)
        print("Terminated Processes:", terminated_processes)

        # Initialize system
        system = System(resource_totals)

        # Add processes and their allocations (skipping terminated ones)
        for i, (max_need, alloc) in enumerate(zip(max_needs, allocations)):
            if i not in terminated_processes:
                system.add_process(i, max_need, alloc)

        # Check safety using Banker's algorithm
        is_safe, safe_sequence = system.is_safe(terminated_processes)

        deadlocked = []
        termination_recommendation = None
        termination_pid = None

        if not is_safe:
            wfg = WFG(system)
            wfg.build_graph()
            deadlocked = wfg.detect_deadlock()
            termination_pid = wfg.recommend_process_to_terminate()
            if termination_pid is not None:
                process_index = next((i for i, p in enumerate(system.processes) if p.pid == termination_pid), None)
                if process_index is not None:
                    held_resources = system.processes[process_index].allocation
                    termination_recommendation = (
                        f"Terminate P{termination_pid} to break circular wait. "
                        f"This process holds resources: {held_resources}"
                    )
            else:
                termination_recommendation = "No further termination recommendation available. Deadlock may persist or system is unrecoverable."


        # Generate Resource Allocation Graph
        G = nx.DiGraph()

        for i in range(len(system.resources)):
            G.add_node(f"R{i}", shape='s', color='lightblue')

        for p in system.processes:
            node_color = 'red' if not is_safe and p.pid in deadlocked else 'lightgreen'
            G.add_node(f"P{p.pid}", shape='o', color=node_color)

        for p in system.processes:
            for r in range(len(p.allocation)):
                if p.allocation[r] > 0:
                    edge_color = 'darkred' if not is_safe and p.pid in deadlocked else 'green'
                    G.add_edge(f"R{r}", f"P{p.pid}", label='alloc', color=edge_color)

            for r in range(len(p.need)):
                if p.need[r] > 0:
                    edge_color = 'darkred' if not is_safe and p.pid in deadlocked else 'blue'
                    G.add_edge(f"P{p.pid}", f"R{r}", label='req', color=edge_color)

        pos = nx.spring_layout(G)
        plt.figure(figsize=(10, 8))

        node_colors = []
        for node in G.nodes():
            if node.startswith('R'):
                node_colors.append('lightblue')
            else:
                pid = int(node[1:])
                if not is_safe:
                    if deadlocked and pid in deadlocked:
                        node_colors.append('red' if pid == termination_pid else 'orange')
                    else:
                        node_colors.append('lightgreen')
                else:
                    node_colors.append('lightgreen')

        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        edge_labels = nx.get_edge_attributes(G, 'label')

        nx.draw(G, pos, with_labels=True, node_color=node_colors, 
               node_size=2000, edge_color=edge_colors, width=2, font_size=10)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        title = "Resource Allocation Graph (Safe State)" if is_safe else "Deadlock Detected"
        plt.title(title)
        plt.savefig(os.path.join(STATIC_FOLDER, "graph.png"))
        plt.close()

        return jsonify({
            "status": "safe" if is_safe else "deadlock",
            "message": "✅ System is in safe state" if is_safe else "⚠️ Deadlock detected",
            "deadlocked_processes": [f"P{pid}" for pid in deadlocked],
            "safe_sequence": [f"P{pid}" for pid in safe_sequence] if is_safe else [],
            "termination_recommendation": termination_recommendation,
            "graph_url": "/graph"
        })

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({
            "status": "error",
            "message": f"Error: {str(e)}"
        })

@app.route('/graph')
def get_graph():
    return send_from_directory(STATIC_FOLDER, "graph.png")

if __name__ == '__main__':
    app.run(debug=True)