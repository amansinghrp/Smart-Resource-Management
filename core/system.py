from typing import List
from .process import Process
from .resource import Resource
from .banker import BankersAlgorithm

class System:
    def __init__(self, resource_totals:List[int]):
        """
        Simulates an OS managing processes and resources.
        
        Args:
            resource_totals: List of total instances per resource type.
                            Example: [5, 3] means 5 R0 and 3 R1.
        """
        
        self.resources = [Resource(rid, total) for rid, total in enumerate(resource_totals)] #create the resources
        self.processes = [] #create the processes in teh system -> initially no process
        self.available = resource_totals.copy()
        
    def add_process(self, max_needs:list[int]) ->int:
        """Register a new process; returns its PID"""
        pid = len(self.processes)
        self.processes.append(Process(pid, max_needs))
        return pid
    def request_resources(self, pid:int, request:List[int])->bool:
        """Attempt to allocate resources to a process"""
        process = self.processes[pid]
        
        # Step 1: Validate request <= process's max needs
        for i in range(len(request)):
            if(request[i] > process.max[i]):
                return False
            
        # Step 2: Check if resources are available
        for i in range(len(request)):
            if(request[i] > self.available[i]):
                process.status = 'waiting'
                return False
            
         # Step 3: Check safety with Banker's Algorithm
        banker = BankersAlgorithm(
            available=self.available.copy(),
            max_need=[p.max for p in self.processes],
            allocated=[p.allocation for p in self.processes]
        )
        
        if not banker.request_resources(pid, request):
            process.status = "waiting"
            return False
            
        # Step 4: ACTUALLY allocate resources if safe
        for j in range(len(request)):
            self.resources[j].allocate(request[j])
            process.allocation[j] += request[j]
            process.need[j] -= request[j]
            self.available[j] -= request[j]
            
        #finally the process is ready for excution
        process.status = "ready"
        return True
    
    def release_resources(self, pid: int):
        """Release all resources held by a process."""
        process = self.processes[pid]
        for j in range(len(process.allocation)):
            self.resources[j].release(process.allocation[j])
            self.available[j] += process.allocation[j]
            process.allocation[j] = 0
            process.need[j] = process.max[j]  # Reset need to max
        process.status = "terminated"
    
    def print_state(self):
        print("\n=== System State ===")
        for r in self.resources:
            print(r)
        for p in self.processes:
            print(p)