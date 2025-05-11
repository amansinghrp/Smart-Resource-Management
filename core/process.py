class Process:
    def __init__(self, pid: int, max_resources: list[int]):
        """
        Initializes a process with its unique process ID and maximum resources it needs.
        """
        self.pid = pid
        self.max = max_resources.copy()  # Max resources needed by the process
        self.allocation = [0] * len(max_resources)  # Initially no resources allocated
        self.need = self.max.copy()  # Initially the need is the same as max resources
        self.requested = [0] * len(max_resources)  # Initially no resources requested
        self.status = "ready"  # status: ready/waiting/terminated

    def allocate(self, resources: list[int]):
        """
        Allocates resources to this process.
        """
        for i in range(len(resources)):
            self.allocation[i] += resources[i]
            self.need[i] -= resources[i]

    def request(self, resources: list[int]):
        """
        Request resources for the process.
        """
        self.requested = resources.copy()
        
    def __str__(self):
        """For printing the process"""
        return f"P{self.pid} | Alloc: {self.allocation} | Need: {self.need} | Req: {self.requested}"
