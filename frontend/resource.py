class Resource:
    def __init__(self, rid, total):
        self.rid = rid
        self.total = total
        self.allocated = 0

    def allocate(self, amount):
        self.allocated += amount

    def release(self, amount):
        self.allocated -= amount

    def __str__(self):
        return f"Resource {self.rid} | Total: {self.total} | Allocated: {self.allocated}"