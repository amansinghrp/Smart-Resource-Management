class Resource:
    def __init__(self, rid:int, total:int):
        """
            Represents a system resource (e.g., CPU, printer).
        
            Args:
                rid: Resource ID (unique identifier)
                total: Total available instances of this resource
        """
        
        self.rid = rid
        self.total = total
        self.allocated = 0
        self.available = total
        
    def allocate(self, instances:int)->bool:
        if(self.available >= instances):
            self.available -= instances
            self.allocated += instances
            return True
        return False
    
    def release(self, instances:int):
        self.allocated -= instances
        self.available += instances
    
    def __str__(self):
        return f'R{self.rid} (Total: {self.total}, Available: {self.available})'