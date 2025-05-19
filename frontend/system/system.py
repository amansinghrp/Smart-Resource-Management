from typing import List
from .process import Process
from .resource import Resource
from .banker import Banker

class System:
    def __init__(self, resource_totals: List[int]):
        self.resources = [Resource(i, total) for i, total in enumerate(resource_totals)]
        self.processes: List[Process] = []
        self.available = resource_totals.copy()

    def add_process(self, max_needs: List[int]) -> int:
        pid = len(self.processes)
        process = Process(pid, max_needs)
        self.processes.append(process)
        return pid

    def is_safe(self) -> bool:
        banker = Banker(
            available=self.available[:],
            max_need=[p.max for p in self.processes],
            allocated=[p.allocation for p in self.processes]
        )
        return banker.is_safe_state(
            self.available[:],
            [p.allocation[:] for p in self.processes]
        )
