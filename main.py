import networkx as nx
import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, allocation):
        self.pid = pid
        self.allocation = allocation
        self.request = [0] * len(allocation)

class Resource:
    def __init__(self, rid, total):
        self.rid = rid
        self.total = total

class System:
    def __init__(self, total_resources):
        self.resources = [Resource(rid, total) for rid, total in enumerate(total_resources)]
        self.processes = []
        self.next_pid = 0

    def add_process(self, allocation):
        p = Process(self.next_pid, allocation)
        self.processes.append(p)
        self.next_pid += 1
        return p

    def request_resources(self, process, request):
        for rid, amount in enumerate(request):
            if amount > 0:
                process.request[rid] += amount

    def detect_requests(self):
        requests = []
        for p in self.processes:
            for rid, req in enumerate(p.request):
                if req > 0:
                    requests.append({"pid": p.pid, "rid": rid})
        return requests

    def detect_deadlock(self):
        wait_for = {p.pid: set() for p in self.processes}
        held_by = {r.rid: None for r in self.resources}

        for p in self.processes:
            for rid, amount in enumerate(p.allocation):
                if amount > 0:
                    held_by[rid] = p.pid

        for p in self.processes:
            for rid, req_amount in enumerate(p.request):
                if req_amount > 0 and held_by[rid] is not None:
                    wait_for[p.pid].add(held_by[rid])

        visited = set()
        stack = set()

        def dfs(pid):
            if pid in stack:
                return True
            if pid in visited:
                return False
            visited.add(pid)
            stack.add(pid)
            for neighbor in wait_for[pid]:
                if dfs(neighbor):
                    return True
            stack.remove(pid)
            return False

        deadlocked_pids = []
        for pid in wait_for:
            if dfs(pid):
                deadlocked_pids.append(pid)

        return deadlocked_pids

    def get_rag_data(self):
        return {
            "processes": [{"pid": p.pid, "alloc": p.allocation} for p in self.processes],
            "resources": [{"rid": r.rid, "instances": r.total} for r in self.resources],
            "requests": self.detect_requests(),
            "deadlocked": self.detect_deadlock()
        }

def draw(system_state):
    G = nx.DiGraph()
    deadlocked = system_state["deadlocked"]

    for p in system_state["processes"]:
        color = 'red' if p['pid'] in deadlocked else 'blue'
        G.add_node(f"P{p['pid']}", color=color, shape='o')

    for r in system_state["resources"]:
        G.add_node(f"R{r['rid']}", color='green', shape='s')

    for p in system_state["processes"]:
        for rid, count in enumerate(p["alloc"]):
            if count > 0:
                G.add_edge(f"R{rid}", f"P{p['pid']}", color='black', style='solid')

    for req in system_state["requests"]:
        G.add_edge(f"P{req['pid']}", f"R{req['rid']}", color='red', style='dashed')

    pos = nx.spring_layout(G, seed=42)

    process_nodes = [n for n in G.nodes if n.startswith('P')]
    resource_nodes = [n for n in G.nodes if n.startswith('R')]

    process_colors = [G.nodes[n]['color'] for n in process_nodes]
    resource_colors = [G.nodes[n]['color'] for n in resource_nodes]

    nx.draw_networkx_nodes(G, pos, nodelist=process_nodes, node_color=process_colors, node_shape='o')
    nx.draw_networkx_nodes(G, pos, nodelist=resource_nodes, node_color=resource_colors, node_shape='s')

    edge_colors = [G[u][v]['color'] for u,v in G.edges]
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors)
    nx.draw_networkx_labels(G, pos)

    import matplotlib.pyplot as plt
    blue_patch = plt.Line2D([0], [0], marker='o', color='w', label='Process', markerfacecolor='blue', markersize=10)
    green_patch = plt.Line2D([0], [0], marker='s', color='w', label='Resource', markerfacecolor='green', markersize=10)
    red_patch = plt.Line2D([0], [0], marker='o', color='w', label='Deadlocked Process', markerfacecolor='red', markersize=10)

    plt.legend(handles=[blue_patch, green_patch, red_patch])
    plt.title("Resource Allocation Graph (RAG)")
    plt.axis('off')
    plt.savefig('rag_visualization.png')
    plt.show()

def main():
    system = System([1, 1])  # 2 resources R0 and R1
    p0 = system.add_process([1, 1])  # Process 0 allocated 1 unit of R0 and R1
    p1 = system.add_process([1, 1])  # Process 1 allocated 1 unit of R0 and R1

    system.request_resources(p0, [1, 0])  # P0 requests R0
    system.request_resources(p1, [0, 1])  # P1 requests R1
    system.request_resources(p0, [0, 1])  # P0 requests R1 → held by P1
    system.request_resources(p1, [1, 0])  # P1 requests R0 → held by P0

    draw(system.get_rag_data())

if __name__ == "__main__":
    main()