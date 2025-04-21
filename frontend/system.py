from typing import List
from process import Process
from resource import Resource
from banker import is_safe_state  # Importing the function from banker.py

class System:
    def __init__(self, processes, resources, allocation, maximum, available):
        self.processes = [Process(i, maximum[i]) for i in range(processes)]
        self.resources = [Resource(i, available[i]) for i in range(resources)]
        self.allocation = allocation
        self.maximum = maximum
        self.available = available


    def add_process(self, max_needs: List[int]) -> int:
        """Register a new process; returns its PID"""
        pid = len(self.processes)
        self.processes.append(Process(pid, max_needs))
        return pid

    def request_resources(self, pid: int, request: List[int]) -> bool:
        """Attempt to allocate resources to a process"""
        process = self.processes[pid]

        # Step 1: Validate request <= process's max needs
        for i in range(len(request)):
            if request[i] > process.max[i]:
                return False

        # Step 2: Check if resources are available
        for i in range(len(request)):
            if request[i] > self.available[i]:
                process.status = 'waiting'
                return False

        # Step 3: Tentatively allocate
        for i in range(len(request)):
            self.resources[i].allocate(request[i])
            self.available[i] -= request[i]
            process.allocation[i] += request[i]
            process.need[i] -= request[i]

        process.status = 'ready'
        return True

    def print_state(self):
        print("\n=== System State ===")
        for r in self.resources:
            print(r)
        for p in self.processes:
            print(p)

    def is_safe(self):
        return is_safe_state(self.allocation, self.maximum, self.available)