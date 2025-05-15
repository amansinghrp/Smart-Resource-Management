from typing import Dict, List, Set
from .system import System

class WFG:
    def __init__(self, system: System):
        self.system = system
        self.graph: Dict[int, Set[int]] = {}  # wait-for graph

    def build_graph(self):
        print("\nWaiting Processes:")
        for p in self.system.processes:
            if p.status == "waiting":
                print(f"P{p.pid}")

        self.graph.clear()
        for p1 in self.system.processes:
            if p1.status == "waiting":
                # For each resource the process is waiting on
                for rid, needed in enumerate(p1.need):
                    if needed > 0:
                        # Check which process is holding this resource
                        for p2 in self.system.processes:
                            if p2.allocation[rid] > 0:
                                if p1.pid not in self.graph:
                                    self.graph[p1.pid] = set()
                                self.graph[p1.pid].add(p2.pid)

    def detect_deadlock(self) -> List[int]:
        visited = set()
        rec_stack = set()
        deadlocked_processes = []

        def dfs(pid: int) -> bool:
            visited.add(pid)
            rec_stack.add(pid)
            for neighbor in self.graph.get(pid, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True  # Found cycle
            rec_stack.remove(pid)
            return False

        for pid in self.graph:
            if pid not in visited:
                if dfs(pid):
                    # Collect all involved in cycle
                    deadlocked_processes = list(rec_stack)
                    break

        return deadlocked_processes

    def print_graph(self):
        print("\n=== Wait-For Graph ===")
        for pid in self.graph:
            print(f"P{pid} -> {[f'P{p}' for p in self.graph[pid]]}")
            