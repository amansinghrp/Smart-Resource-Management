from core.system import System

def simulate():
    # Initialize system with 2 resource types (5 R0, 3 R1)
    #means there are 2 resource types first with 5 instances and secodn with 3 instances
    system = System([5, 3])
    
    #add 2 processes in this system
    p0 = system.add_process([3, 1]) #max needs of p0 is 3<-r0 and 1<-r1
    p1 = system.add_process([2, 2]) #max needs of p1 is 2<-r0 and 2<-r1
    
    #p0 requests for resources
    print("\nP0 requests [2, 1]")
    if system.request_resources(p0, [2,1]):
        print("✓ Allocation successful!")
    else:
        print("✗ Allocation failed!")
    system.print_state()
    
    #p1 requests resources
    print("\nP1 requests [1, 3]")
    if system.request_resources(p1, [1, 3]):
        print("✓ Allocation successful!")
    else:
        print("✗ Allocation failed!")
    system.print_state()
    
if __name__ == "__main__":
    simulate()