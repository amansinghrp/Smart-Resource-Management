from typing import Dict, Set, List
from .system import System

class WFG:
    def __init__(self, system: System):
        self.system = system
        self.graph: Dict[int, Set[int]] = {}

    def build_graph(self):
        self.graph.clear()
        for p1 in self.system.processes:
            p1.status = "ready"  # Reset status
            for rid, needed in enumerate(p1.need):
                if needed > 0 and needed > self.system.available[rid]:
                    p1.status = "waiting"
                    for p2 in self.system.processes:
                        if p2.allocation[rid] > 0:
                            self.graph.setdefault(p1.pid, set()).add(p2.pid)

    def detect_deadlock(self) -> List[int]:
        visited = set()
        rec_stack = set()
        deadlocked = []

        def dfs(pid):
            visited.add(pid)
            rec_stack.add(pid)
            for neighbor in self.graph.get(pid, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(pid)
            return False

        for pid in self.graph:
            if pid not in visited and dfs(pid):
                deadlocked = list(rec_stack)
                break

        return deadlocked
