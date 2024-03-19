import numpy as np
from transportation import *

# Non-discounted

C = np.array([  [11, 10**6,  8,  8],
                [ 7,     5,  6, 12],
                [4,     6,  8,  5]
            ], dtype=int)

S = np.array([100, 120, 60])
D = np.array([50, 40, 90, 70])

A1, C1 = init_vogel(C, S, D) 
A1, min_cost_1 = transportation_solver(A1, C1)

# Discounted 

C = np.array([  [11, 10**6,  8,  5],
                [ 7,     5,  6, 12],
                [4,     6,  8,  5]
            ], dtype=int)

S = np.array([100, 120, 60])
D = np.array([50, 40, 90, 70])

A2, C2 = init_vogel(C, S, D) 
A2, min_cost_2 = transportation_solver(A2, C2)

# Since we have a special case regarding a discount we have to recalculate the costs

min_cost_1 = min_cost_1 - (max(0, A1[0, 3] - 20) * 3)
min_cost_2 = min_cost_2 + (min(20, A2[0, 3]) * 3)

print(f'min1: {min_cost_1}, min2: {min_cost_2}')

