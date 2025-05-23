from typing import List

class Process:
    def __init__(self, pid: int, max_resources: List[int]):
        self.pid = pid
        self.max = max_resources.copy()
        self.allocation = [0] * len(max_resources)
        self.need = self.max.copy()
        self.status = "ready"
        self.requested = [0] * len(max_resources)  # Track current requests

    def allocate(self, resources: List[int]):
        for i in range(len(resources)):
            self.allocation[i] += resources[i]
            self.need[i] -= resources[i]

    def request(self, resources: List[int]):
        self.requested = resources.copy()

    def __str__(self):
        return f"P{self.pid} | Max: {self.max} | Alloc: {self.allocation} | Need: {self.need} | Requested: {self.requested}"
