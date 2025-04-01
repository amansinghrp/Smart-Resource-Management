class Process:
    def __init__(self, pid:int, max_resources:list[int]):
        """
            initialise a process with its unique process ID 
            and maximum resources it needs in the form a list
            
            Args:
                pid: Process ID (e.g., 1, 2, 3...)
                max_resources: List defining max needed instances 
                per resource type
        """
        
        self.pid = pid
        self.max = max_resources.copy() #make sure that changes dont reflect
        self.allocation = [0] * len(max_resources)
        self.need = max_resources.copy() #initially the need is same as maximum resources
        self.status = "ready" #status: ready/waiting/terminated
        
    def __str__(self):
        """For printing the process"""
        return f"P{self.pid} | Alloc: {self.allocation} | Need: {self.need}"
        