from flask import Flask, request, jsonify, render_template, send_from_directory
import networkx as nx
import matplotlib
matplotlib.use('Agg')  # Use Anti-Grain Geometry backend (non-GUI)
import matplotlib.pyplot as plt
import os
from system.system import System
from system.wfg import WFG

app = Flask(__name__)
STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
@app.route('/check', methods=['POST'])
def check_deadlock():
    try:
        data = request.get_json()
        resource_totals = data['resource_totals']
        max_needs = data['maximum']
        allocations = data['allocation']

        system = System(resource_totals)

        # Add processes
        for max_need in max_needs:
            system.add_process(max_need)

        # Apply allocations
        for i, alloc in enumerate(allocations):
            system.processes[i].allocate(alloc)
            for j in range(len(alloc)):
                system.resources[j].allocate(alloc[j])
                system.available[j] -= alloc[j]

        # ✅ Mark processes as waiting if they still need any resources
        for p in system.processes:
            for i in range(len(p.need)):
                if p.need[i] > 0:
                    p.status = "waiting"
                    break

        # Build WFG and detect deadlock
        wfg = WFG(system)
        wfg.build_graph()
        deadlocked = wfg.detect_deadlock()

        # Generate graph image
        G = nx.DiGraph()
        for pid, waits_for in wfg.graph.items():
            for target_pid in waits_for:
                G.add_edge(f"P{pid}", f"P{target_pid}")

        plt.figure(figsize=(6, 4))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='lightcoral', edge_color='gray', node_size=2000, font_size=10)
        plt.title("Wait-For Graph")
        plt.savefig(os.path.join(STATIC_FOLDER, "graph.png"))
        plt.close()

        return jsonify({
            "message": "⚠️ Deadlock detected!" if deadlocked else "✅ No deadlock detected.",
            "deadlocked_processes": [f"P{pid}" for pid in deadlocked],
            "graph_url": "/graph"
        })

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/graph')
def get_graph():
    return send_from_directory(STATIC_FOLDER, 'graph.png')

# ✅ This block ensures the app runs when you execute `python3 app.py`
if __name__ == '__main__':
    app.run(debug=True)
