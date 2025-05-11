class Resource:
    def __init__(self, rid: int, total: int):
        """
        Represents a system resource (e.g., CPU, printer).
        """
        self.rid = rid
        self.total = total
        self.allocated = 0
        self.available = total

    def allocate(self, instances: int) -> bool:
        """
        Attempt to allocate a specified number of instances of this resource.
        """
        if self.available >= instances:
            self.available -= instances
            self.allocated += instances
            return True
        return False

    def release(self, instances: int):
        """
        Release a specified number of instances of this resource.
        """
        self.allocated -= instances
        self.available += instances
        
    def __str__(self):
        return f'R{self.rid} (Total: {self.total}, Available: {self.available})'
