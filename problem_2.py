import numpy as np
from transportation import *

C = np.array([  [5, 7, 9, 6],
                [6, 7, 10, 5],
                [7, 6, 8, 1]
            ], dtype=int)

S = np.array([120, 140, 100])
D = np.array([100, 60, 80, 120])

A, C = init_vogel(C, S, D) 
A, min_cost = transportation_solver(A, C)

print(f'min cost: {min_cost}')