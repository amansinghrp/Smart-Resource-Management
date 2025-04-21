def is_safe_state(allocation, maximum, available):
    p = len(allocation)  # number of processes
    r = len(available)   # number of resources

    # Step 1: Calculate the Need matrix
    need = [[maximum[i][j] - allocation[i][j] for j in range(r)] for i in range(p)]

    finished = [False] * p
    work = available[:]
    safe_seq = []

    while len(safe_seq) < p:
        allocated_in_this_round = False
        for i in range(p):
            if not finished[i] and all(need[i][j] <= work[j] for j in range(r)):
                for j in range(r):
                    work[j] += allocation[i][j]
                finished[i] = True
                safe_seq.append(i)
                allocated_in_this_round = True
        if not allocated_in_this_round:
            return False  # No safe sequence found

    return True