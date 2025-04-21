# core/bankers.py
class BankersAlgorithm:
    def __init__(self, available: list[int], max_need: list[list[int]], allocated: list[list[int]]):
        """
        Initialize Banker's Algorithm with system state.
        
        Args:
            available: List of available instances per resource type (e.g., [3, 1, 2])
            max_need: 2D list of maximum needs per process (e.g., [[7,4,3], [3,2,2]])
            allocated: 2D list of currently allocated resources per process
        """
        self.available = available.copy()
        self.max = [row.copy() for row in max_need]
        self.allocation = [row.copy() for row in allocated]
        
        # Calculate need matrix (max - allocated)
        self.need = [
            [self.max[i][j] - self.allocation[i][j] 
             for j in range(len(available))]  # Per-resource
            for i in range(len(max_need))     # Per-process
        ]
            

    def is_safe(self) -> (bool, list[int]):
        """
        Check if system is in a safe state.
        
        Returns:
            (True, safe_sequence) if safe, (False, []) otherwise
        """
        work = self.available.copy()
        finish = [False] * len(self.max)
        safe_sequence = []
        
        # Try to find a complete safe sequence
        for _ in range(len(self.max)):  # Max N iterations (N = num processes)
            found = False
            for i in range(len(self.max)):
                if not finish[i] and all(self.need[i][j] <= work[j] for j in range(len(work))):
                    work = [work[j] + self.allocation[i][j] for j in range(len(work))]
                    finish[i] = True
                    safe_sequence.append(i)
                    found = True
                    break
            
            if not found:
                return (False, [])  # Deadlock detected → empty sequence
        
        return (True, safe_sequence)  # All processes finished

    def request_resources(self, pid: int, request: list[int]) -> bool:
        """
        Check if granting a request leads to a safe state.
        
        Args:
            pid: Process ID making the request
            request: List of requested resources per type
            
        Returns:
            True if request can be granted safely
        """
        # Step 1: Verify request <= need
        if any(request[j] > self.need[pid][j] for j in range(len(request))):
            return False
            
        # Step 2: Verify request <= available
        if any(request[j] > self.available[j] for j in range(len(request))):
            return False
            
        # Step 3: Tentatively allocate
        for j in range(len(request)):
            self.available[j] -= request[j]
            self.allocation[pid][j] += request[j]
            self.need[pid][j] -= request[j]
            
        # Step 4: Check safety
        is_safe, _ = self.is_safe()
        
        # Step 5: Rollback if unsafe
        if not is_safe:
            for j in range(len(request)):
                self.available[j] += request[j]
                self.allocation[pid][j] -= request[j]
                self.need[pid][j] += request[j]
        
        return is_safe