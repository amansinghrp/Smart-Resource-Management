def is_safe(process, resources, maximum_needed, allocated, p, r):
    # Calculate the needed matrix
    needed = [[maximum_needed[i][j] - allocated[i][j] for j in range(r)] for i in range(p)]

    finished_process = [False] * p
    safe_seq = []

    # Make a copy of available resources
    temp_avail = resources.copy()

    finished = 0
    while finished < p:
        current_process_finished = False
        for i in range(p):
            if not finished_process[i]:
                if all(needed[i][j] <= temp_avail[j] for j in range(r)):
                    # Allocate the released resources
                    for k in range(r):
                        temp_avail[k] += allocated[i][k]
                    finished += 1
                    safe_seq.append(i)
                    finished_process[i] = True
                    current_process_finished = True
        if not current_process_finished:
            print("No safe sequence")
            return

    print("System is in Safe sequence")
    print("->".join(map(str, safe_seq)) + "->end")


def main():
    print("Enter number of process and Total Resources Available")
    p, r = map(int, input().split())

    print("Enter Process Ids")
    process = list(map(int, input().split()))

    print("Enter number of Each resource")
    resources = list(map(int, input().split()))

    maximum_needed = []
    print("Enter the Maximum of each process needed")
    for i in range(p):
        print(f"P{i} ", end="")
        maximum_needed.append(list(map(int, input().split())))

    allocated = []
    print("Enter Allocated Resources")
    for i in range(p):
        print(f"P{i} ", end="")
        allocated.append(list(map(int, input().split())))

    is_safe(process, resources, maximum_needed, allocated, p, r)


if __name__ == "__main__":
    main()
