def compute_makespan(schedule, p):
    _, m = p.shape
    n = len(schedule)
    c = [[0]*m for i in range(n)]
    for i in range(n):
        for j in range(m):
            if i == 0 and j == 0:
                c[i][j] = p[schedule[i]][j]
            elif i == 0:
                c[i][j] = c[i][j-1] + p[schedule[i]][j]
            elif j == 0:
                c[i][j] = c[i-1][j] + p[schedule[i]][j]
            else:
                c[i][j] = max(c[i][j-1], c[i-1][j]) + p[schedule[i]][j]
    return c[n-1][m-1]

def sum_and_order(tasks_val, machines_val, tasks):
    tab = []
    tab1 = []
    for i in range(0, tasks_val):
        tab.append(0)
        tab1.append(0)
    for j in range(0, tasks_val):
        for k in range(0, machines_val):
            tab[j] += tasks[j][k]
    place = 0
    iter = 0
    while(iter != tasks_val):
        max_time = 0
        for i in range(0, tasks_val):
            if(max_time < tab[i]):
                max_time = tab[i]
                place = i
        tab[place] = 1
        tab1[iter] = place
        iter = iter + 1
    return tab1


def insert(sequence, position, value):
    new_seq = sequence[:]
    new_seq.insert(position, value)
    return new_seq


def neh(tasks, machines_val, tasks_val):
    order = sum_and_order(tasks_val, machines_val, tasks)
    current_seq = [order[0]]
    for i in range(1, tasks_val):
        min_cmax = float("inf")
        for j in range(0, i + 1):
            tmp = insert(current_seq, j, order[i])
            cmax_tmp = compute_makespan([x-1 for x in tmp], tasks)
            if min_cmax > cmax_tmp:
                best_seq = tmp
                min_cmax = cmax_tmp
        current_seq = best_seq
    return current_seq, compute_makespan([x-1 for x in current_seq] , tasks)





def modif_NEH(data_Trans, nbr_machines, nbr_tasks):
    seq, _ = neh(data_Trans, nbr_machines, nbr_tasks)
    seq = [x+1 for x in seq]
    return seq,_
