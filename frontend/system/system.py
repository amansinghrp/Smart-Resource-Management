from typing import List, Tuple
from .process import Process
from .resource import Resource
from .banker import Banker

class System:
    def __init__(self, resource_totals: List[int]):
        self.resources = [Resource(i, total) for i, total in enumerate(resource_totals)]
        self.processes: List[Process] = []
        self.available = resource_totals.copy()

    def add_process(self, pid: int, max_needs: List[int], allocation: List[int]):
        process = Process(pid, max_needs)
        process.allocate(allocation)
        for j in range(len(allocation)):
            self.resources[j].allocate(allocation[j])
            self.available[j] -= allocation[j]
        self.processes.append(process)

    def is_safe(self, terminated_processes: List[int] = []) -> Tuple[bool, List[int]]:
        # Filter out terminated processes
        filtered_max_need = []
        filtered_allocation = []
        filtered_available = self.available[:]
        active_process_ids = []

        for i, p in enumerate(self.processes):
            if p.pid in terminated_processes:
                # Add the terminated process's allocation back to available resources
                for j in range(len(p.allocation)):
                    filtered_available[j] += p.allocation[j]
                continue

            filtered_max_need.append(p.max)
            filtered_allocation.append(p.allocation)
            active_process_ids.append(p.pid)

        # Run Banker's algorithm on filtered data
        banker = Banker(
            available=filtered_available,
            max_need=filtered_max_need,
            allocated=filtered_allocation
        )
        is_safe, sequence = banker.is_safe_state()

        # Map the safe sequence indices back to actual PIDs
        actual_sequence = [active_process_ids[i] for i in sequence] if is_safe else []
        return is_safe, actual_sequence
