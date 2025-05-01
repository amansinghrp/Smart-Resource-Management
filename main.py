# main.py

from system import System
import rag

def main():
    system = System([1, 1])  # 2 resources R0 and R1
    p0 = system.add_process([1, 1])  # Process 0 allocated 1 unit of R0 and R1
    p1 = system.add_process([1, 1])  # Process 1 allocated 1 unit of R0 and R1

    system.request_resources(p0, [1, 0])  # P0 requests 1 R0 (already holds)
    system.request_resources(p1, [0, 1])  # P1 requests 1 R1 (already holds)
    system.request_resources(p0, [0, 1])  # P0 requests R1 (held by P1) → waiting
    system.request_resources(p1, [1, 0])  # P1 requests R0 (held by P0) → waiting → Deadlock

    rag.draw(system.get_rag_data())

if __name__ == "__main__":
    main()
