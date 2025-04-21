class Process:
    def __init__(self, pid, max_needs):
        self.pid = pid
        self.max = max_needs  # Maximum resource demand
        self.allocation = [0] * len(max_needs)
        self.need = max_needs.copy()
        self.status = 'new'

    def __str__(self):
        return (f"Process {self.pid} | Max: {self.max} | "
                f"Alloc: {self.allocation} | Need: {self.need} | Status: {self.status}")