# system.py

class Process:
    def __init__(self, pid, allocation):
        self.pid = pid
        self.allocation = allocation  # List of resources allocated
        self.request = [0] * len(allocation)  # Current requests, initially none

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
        # Basic deadlock detection (using Wait-For Graph idea)
        # Here, we'll simply assume deadlock when there are mutual requests
        # (this is very simple for visualization, can improve later)

        wait_for = {p.pid: set() for p in self.processes}
        held_by = {r.rid: None for r in self.resources}

        # Track which process holds which resource
        for p in self.processes:
            for rid, amount in enumerate(p.allocation):
                if amount > 0:
                    held_by[rid] = p.pid

        # Build wait-for relationships
        for p in self.processes:
            for rid, req_amount in enumerate(p.request):
                if req_amount > 0 and held_by[rid] is not None:
                    wait_for[p.pid].add(held_by[rid])

        # Detect cycle (naive way: DFS)
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
