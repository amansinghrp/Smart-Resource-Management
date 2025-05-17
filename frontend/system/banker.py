from typing import List

class Banker:
    def __init__(self, available: List[int], max_need: List[List[int]], allocated: List[List[int]]):
        self.available = available
        self.max_need = max_need
        self.allocated = allocated
        self.process_count = len(max_need)
        self.resource_count = len(available)

    def is_safe_state(self, available: List[int], allocated: List[List[int]]) -> bool:
        work = available[:]
        finish = [False] * self.process_count
        need = [
            [self.max_need[i][j] - allocated[i][j] for j in range(self.resource_count)]
            for i in range(self.process_count)
        ]

        while True:
            progress = False
            for i in range(self.process_count):
                if not finish[i] and all(need[i][j] <= work[j] for j in range(self.resource_count)):
                    for j in range(self.resource_count):
                        work[j] += allocated[i][j]
                    finish[i] = True
                    progress = True
            if not progress:
                break

        return all(finish)
