from typing import List

class Banker:
    def __init__(self, available: List[int], max_need: List[List[int]], allocated: List[List[int]]):
        """
        Initializes the Banker's Algorithm for managing resource requests.
        
        Args:
            available: A list of available instances of each resource.
            max_need: A 2D list where each sublist represents the maximum resource need per process.
            allocated: A 2D list representing the resources allocated to each process.
        """
        self.available = available
        self.max_need = max_need
        self.allocated = allocated
        self.process_count = len(max_need)
        self.resource_count = len(available)
    
    def request_resources(self, pid: int, request: List[int]) -> bool:
        """
        Attempts to allocate requested resources to a process using the Banker's algorithm.
        
        Args:
            pid: Process ID requesting resources.
            request: List of requested resources by the process.
        
        Returns:
            bool: True if the request can be safely granted, False otherwise.
        """
        
        # Step 1: Check if the request is less than or equal to the process's maximum need
        for i in range(self.resource_count):
            if request[i] > self.max_need[pid][i]:
                return False
        
        # Step 2: Check if the request can be satisfied by the available resources
        for i in range(self.resource_count):
            if request[i] > self.available[i]:
                return False
        
        # Step 3: Pretend to allocate the requested resources
        # Temporarily modify available and allocation
        temp_available = self.available[:]
        temp_allocated = [row[:] for row in self.allocated]  # Create a deep copy
        temp_available = [temp_available[i] - request[i] for i in range(self.resource_count)]
        temp_allocated[pid] = [temp_allocated[pid][i] + request[i] for i in range(self.resource_count)]
        
        # Step 4: Check if the system is in a safe state after the allocation
        if not self.is_safe_state(temp_available, temp_allocated):
            return False
        
        # Step 5: If it's safe, actually allocate the resources
        self.available = temp_available
        self.allocated = temp_allocated
        
        return True
    
    def is_safe_state(self, available: List[int], allocated: List[List[int]]) -> bool:
        """
        Checks if the system is in a safe state by simulating resource allocation.
        
        Args:
            available: A list of available resources after allocation.
            allocated: A 2D list representing the current allocation of resources to processes.
        
        Returns:
            bool: True if the system is in a safe state, False otherwise.
        """
        
        work = available[:]
        finish = [False] * self.process_count
        
        while True:
            # Find a process that can finish
            progress_made = False
            for i in range(self.process_count):
                if not finish[i]:
                    # Check if the process's remaining need can be satisfied with available resources
                    can_finish = True
                    for j in range(self.resource_count):
                        if self.max_need[i][j] - allocated[i][j] > work[j]:
                            can_finish = False
                            break
                    
                    if can_finish:
                        # Pretend this process finishes and releases its resources
                        work = [work[j] + allocated[i][j] for j in range(self.resource_count)]
                        finish[i] = True
                        progress_made = True
                        break
            
            if not progress_made:
                break
        
        # If all processes can finish, the system is in a safe state
        return all(finish)
