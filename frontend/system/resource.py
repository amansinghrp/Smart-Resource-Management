class Resource:
    def __init__(self, rid: int, total: int):
        self.rid = rid
        self.total = total
        self.allocated = 0
        self.available = total

    def allocate(self, instances: int) -> bool:
        if self.available >= instances:
            self.available -= instances
            self.allocated += instances
            return True
        return False

    def release(self, instances: int):
        self.allocated -= instances
        self.available += instances
