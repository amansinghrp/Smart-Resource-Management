from .process import Process
from .resource import Resource
from .banker import Banker

class System:
    def __init__(self, resource_totals: list[int]):
        """
        Simulates an OS managing processes and resources.
        """
        self.resources = [Resource(rid, total) for rid, total in enumerate(resource_totals)]
        self.processes = []  # Initially no processes
        self.available = resource_totals.copy()

    def add_process(self, max_needs: list[int]) -> int:
        """Register a new process; returns its PID"""
        pid = len(self.processes)
        process = Process(pid, max_needs)
        self.processes.append(process)
        return pid

    def request_resources(self, pid: int, request: list[int]) -> bool:
        """Request resources for a process"""
        process = self.processes[pid]

        # Request resources
        process.request(request)

        # Step 1: Validate request <= process's max needs
        for i in range(len(request)):
            if request[i] > process.max[i]:
                return False

        # Step 2: Check if resources are available
        for i in range(len(request)):
            if request[i] > self.available[i]:
                process.status = 'waiting'
                return False

        # Step 3: Simulate resource allocation
        banker = Banker(self.available, [p.max for p in self.processes], [p.allocation for p in self.processes])

        if not banker.request_resources(pid, request):
            process.status = "waiting"
            return False

        # Step 4: Allocate resources
        for j in range(len(request)):
            self.resources[j].allocate(request[j])
            process.allocate(request[j])
            self.available[j] -= request[j]

        process.status = "ready"
        return True

    def release_resources(self, pid: int):
        """Release all resources held by a process"""
        process = self.processes[pid]
        for j in range(len(process.allocation)):
            self.resources[j].release(process.allocation[j])
            self.available[j] += process.allocation[j]
            process.allocation[j] = 0
            process.need[j] = process.max[j]  # Reset need to max
        process.status = "terminated"

    def print_state(self):
        """Print the current system state"""
        print("\n=== System State ===")
        for r in self.resources:
            print(r)
        for p in self.processes:
            print(p)
            