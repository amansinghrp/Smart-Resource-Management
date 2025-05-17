import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for Matplotlib
import matplotlib.pyplot as plt
import networkx as nx

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

        print(f"Received request with {num_processes} processes")
        print(f"Total resources: {resource_totals}")
        print(f"Max needs: {max_needs}")
        print(f"Allocations: {allocations}")

        system = System(resource_totals)

        for max_need in max_needs:
            system.add_process(max_need)

        for i, alloc in enumerate(allocations):
            system.processes[i].allocate(alloc)
            for j in range(len(alloc)):
                # Update system resources allocation
                system.resources[j].allocate(alloc[j])
                system.available[j] -= alloc[j]

        print(f"System available after allocations: {system.available}")
        for p in system.processes:
            print(f"Process {p.pid} allocation: {p.allocation}, need: {p.need}, status: {p.status}")

        is_safe = system.is_safe()
        deadlocked = []

        if not is_safe:
            print("System is NOT in safe state, building Wait-For Graph...")
            wfg = WFG(system)
            wfg.build_graph()

            print("Wait-For Graph adjacency list:")
            for pid, neighbors in wfg.graph.items():
                print(f"P{pid} -> {[f'P{n}' for n in neighbors]}")

            deadlocked = wfg.detect_deadlock()
            print(f"Deadlocked processes detected: {deadlocked}")

            # Build graph visualization
            G = nx.DiGraph()
            for pid, targets in wfg.graph.items():
                for target in targets:
                    G.add_edge(f"P{pid}", f"P{target}")

            plt.figure(figsize=(6, 4))
            pos = nx.spring_layout(G)
            nx.draw(G, pos, with_labels=True, node_color='salmon', edge_color='gray', node_size=2000)
            plt.title("Wait-For Graph")
            plt.savefig(os.path.join(STATIC_FOLDER, "graph.png"))
            plt.close()
        else:
            print("System is in safe state. No deadlock.")

        return jsonify({
            "message": "⚠️ Deadlock detected!" if not is_safe else "✅ No deadlock detected.",
            "deadlocked_processes": [f"P{pid}" for pid in deadlocked],
            "graph_url": "/graph" if not is_safe else None
        })

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"message": f"Error: {str(e)}"})


@app.route('/graph')
def get_graph():
    return send_from_directory(STATIC_FOLDER, "graph.png")


if __name__ == '__main__':
    app.run(debug=True)
