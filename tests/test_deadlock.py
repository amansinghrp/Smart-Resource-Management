from core.system import System
from core.wfg import WFG

# Initialize system
sys = System([3, 2])  # Example: 2 resource types

# Add processes
p0 = sys.add_process([2, 1])
p1 = sys.add_process([1, 2])
p2 = sys.add_process([3, 2])

# Request resources (simulate scenario that leads to waiting)
sys.request_resources(p0, [1, 0])
sys.request_resources(p1, [0, 1])
sys.request_resources(p2, [2, 1])

sys.request_resources(p1, [1, 1])  # This might cause p1 to wait

# Print current state
sys.print_state()

# Check WFG
wfg = WFG(sys)
wfg.build_graph()
wfg.print_graph()

deadlocked = wfg.detect_deadlock()
if deadlocked:
    print(f"\nDeadlock detected among: {[f'P{pid}' for pid in deadlocked]}")
else:
    print("\nNo deadlock detected.")
