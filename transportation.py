import numpy as np

def init_vogel(C, S, D):

    m, n = np.shape(C)

    A = np.zeros((m, n), dtype=int)

    print('\n------------------- INIT --------------------\n')

    non_filled_rows = [i for i in range(m)]
    non_filled_colls = [i for i in range(n)]

    counter = 0
    while(len(non_filled_rows) > 0 and len(non_filled_colls) > 0):
        counter += 1

        is_pivot_row = True
        pivot_idx = -1

        print(f'len non filled rows: {len(non_filled_rows)}')

        if len(non_filled_rows) < 2:
            is_pivot_row = True
            pivot_idx = non_filled_rows.pop()
        elif len(non_filled_colls) < 2:
            is_pivot_row = False
            pivot_idx = non_filled_colls.pop()

        else:
            row_diffs = np.column_stack((non_filled_rows, [np.diff(np.sort(C[i, non_filled_colls])[:2]) for i in non_filled_rows]))
            col_diffs = np.column_stack((non_filled_colls, [np.diff(np.sort(C[non_filled_rows, j])[:2]) for j in non_filled_colls]))
            max_row_diff = max(row_diffs, key=lambda x: x[1])
            max_col_diff = max(col_diffs, key=lambda x: x[1])

            print(f'col_diffs: {col_diffs.tolist()}')

            if max_col_diff[1] > max_row_diff[1]:
                is_pivot_row = False
                pivot_idx = max_col_diff[0]
                non_filled_colls.remove(pivot_idx)
            else:
                is_pivot_row = True
                pivot_idx = max_row_diff[0]
                non_filled_rows.remove(pivot_idx)
        

        if is_pivot_row:
            idxs_cost_sorted = np.array(sorted(list(zip(non_filled_colls, C[pivot_idx, non_filled_colls].tolist())), key=lambda x: (x[1], -x[0])))[:, 0].tolist()

            while(S[pivot_idx] - sum(A[pivot_idx]) > 0 and len(idxs_cost_sorted) > 0):
                idx = idxs_cost_sorted.pop(0)

                A[pivot_idx, idx] = min(S[pivot_idx] - sum(A[pivot_idx]), D[idx] - sum(A[:,idx]) if D[idx] - sum(A[:,idx]) > 0 else 0)

        else:
            idxs_cost_sorted = np.array(sorted(list(zip(non_filled_rows, C[non_filled_rows, pivot_idx].tolist())), key=lambda x: (x[1], -x[0])))[:, 0].tolist()

            while(D[pivot_idx] - sum(A[:, pivot_idx]) > 0 and len(idxs_cost_sorted) > 0):
                idx = idxs_cost_sorted.pop(0)

                A[idx, pivot_idx] = min(S[idx] - sum(A[idx]) if S[idx] - sum(A[idx]) > 0 else 0, D[pivot_idx] - sum(A[:, pivot_idx]))


        # remove maxed out demand or supply
        for i, x in enumerate(D):
            if x - np.sum(A[:, i]) == 0 and i in non_filled_colls:
                non_filled_colls.remove(i)
                print(f'Col {i} deleted')
        
        for i, x in enumerate(S):
            if x - np.sum(A[i]) == 0 and i in non_filled_rows:
                non_filled_rows.remove(i)
                print(f'Row {i} deleted')

        
        print(f'pivot idx: {pivot_idx}')
        print(f'is pivot row: {is_pivot_row}')
        print(f'A: \n{A}\n')


    if sum(S) > sum(D):
        C = np.column_stack((C, np.zeros(m, dtype=int)))
        D = np.append(D, sum(S) - sum(D))
        A = np.column_stack((A, np.zeros(m, dtype=int)))

        m, n = np.shape(C)

        for i in range(m):
            A[i, -1] = S[i] - sum(A[i])


    print(f'C:\n{C} \n A:\n{A}')

    return A, C


def transportation_solver(A, C):
    m, n = np.shape(C)

    print('\n---------------ALGORITM START----------------\n')
    counter = 1
    while(True):
        print('ITERATION: ', counter, '\n')
        counter += 1

        idxs_zeros = []

        for i in range(m):
            for j in range(n):
                if A[i, j] != 0:
                    idxs_zeros.append((i ,j))

        v = np.full(m, None)
        w = np.full(n, None)

        first = True
        c = 0
        while idxs_zeros:
            c += 1
            if c > (m*n)**2:
                return A, np.sum(np.multiply(A, C))
            i, j = idxs_zeros.pop(0)
            if first:
                v[i] = 0
                first = False

            if v[i] is not None:
                w[j] = C[i, j] - v[i]
            elif w[j] is not None:
                v[i] = C[i, j] - w[j]
            else:
                idxs_zeros.append((i, j))

            # print('v: ', v)
            # print('w: ', w)
            # print('zeros: ', idxs_zeros)


        v = np.array(v, dtype=int)
        w = np.array(w, dtype=int)

        print(f'v: {v}, w: {w}')
                    
        C_slack = np.zeros((m, n))

        for i in range(m):
            for j in range(n):
                C_slack[i, j] = C[i, j] - v[i] - w[j]


        index_min = np.unravel_index(C_slack.argmin(), C_slack.shape)

        print(f'C slack: \n{C_slack}')

        if C_slack[index_min] >= 0 or counter > 3:
            # Optimal found 
            break

        row, col = index_min

        # Find the loop
        points = []

        for a in range(n):
            if a == col or A[row, a] == 0:
                continue
            for b in range(m):
                if A[b, a] > 0 and A[b, col] > 0:
                    points = [(row, col), (row, a), (b, a), (b, col)]
                    break

        change = min(A[points[1]], A[points[3]]) 

        A[points[0]] += change
        A[points[1]] -= change
        A[points[2]] += change
        A[points[3]] -= change

        print(f'points: {points}')
        print(f'change: {change}')
        print(f'C_hat: \n{C_slack}')
        print(f'A:\n{A}')
        print(f'min: {np.sum(np.multiply(A, C))}')

        print("\n- - - - - - - - - - - - - - - - - - - - - - -\n")

    min_cost = np.sum(np.multiply(A, C))
    print(f'A:\n{A}')
    print(f'min cost: {min_cost}')

    return A, min_cost
