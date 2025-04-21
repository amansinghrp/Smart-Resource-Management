from typing import List
from process import Process
from resource import Resource

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
            
        # Step 3: Tentatively allocate
        for i in range(len(request)):
            self.resources[i].allocate(request[i])
            self.available[i] -= request[i]
            process.allocation[i] += request[i]
            process.need[i] -= request[i]
        
        #finally the process is ready for excution
        process.status = 'ready'
        return True
    
    def print_state(self):
        print("\n=== System State ===")
        for r in self.resources:
            print(r)
        for p in self.processes:
            print(p)