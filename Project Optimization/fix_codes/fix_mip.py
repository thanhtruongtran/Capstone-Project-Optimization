import ortools
# Integer Linear Programming
from ortools.linear_solver import pywraplp
# Constraint Programming
from ortools.sat.python import cp_model
# Timer
import time
import sys
def input():
    [N,M] = [int(x) for x in sys.stdin.readline().split()]
    d = [int(x) for x in sys.stdin.readline().split()]
    c = [int(x) for x in sys.stdin.readline().split()]
    [K] = [int(x) for x in sys.stdin.readline().split()]
    p = []
    for i in range(K):
        p.append([int(x) for x in sys.stdin.readline().split()])
    return N,M,d,c,K,p

N, M, d, c, K, p = input()
d.insert(0,0)
c.insert(0,0)
# print(f'N = {N}', f'd = {d}', f'M = {M}', f'c = {c}', f'K = {K}', f'p = {p}', sep = '\n')

# Solution Printer
def printSolution():
  solution = []
  for i in range(1,obj_value+1):
    for j in range(M+1):
      if solution_matrix[i][j] != -1:
        solution.append([solution_matrix[i][j], i, j])
  solution = sorted(solution, key= lambda x: x[0])
  for i in solution:
    print(*i)
    
# Instantiate a MIP mip_solver
mip_solver = pywraplp.Solver.CreateSolver('SCIP')

# Infinity
INF = mip_solver.infinity()

# Define variables

# Variable x[i][j][k]
x = [[[mip_solver.IntVar(0, 1, f'x[{i}][{j}][{k}]') for i in range(N+1)] for j in range(M+1)] for k in range(N+1)]

# Variable y
y = mip_solver.IntVar(0, N , 'y')

# Define constraints

# Constraint 1: Pairs of conflicting courses may not be put in the same period
for i in range(K):
  u, v = p[i][0], p[i][1]
  for k in range(1,N+1):
    constraint = mip_solver.Constraint(0, 1)
    for j1 in range(1,M+1):
      for j2 in range(1,M+1):
        if j1 != j2:
          constraint.SetCoefficient(x[u][j1][k], 1)
          constraint.SetCoefficient(x[v][j2][k], 1)

# Constraint 2: An course room may be assigned at most one course in a period
for j in range(1,M+1):
  for k in range(1,N+1):
    constraint = mip_solver.Constraint(0, 1)
    for i in range(1,N+1):
      constraint.SetCoefficient(x[i][j][k], 1)

# Constraint 3: The number of periods (k.x[i,j,k] - y <= 0)
for i in range(1,N+1):
  for j in range(1,M+1):
    for k in range(1,N+1):
      constraint = mip_solver.Constraint(-INF, 0)
      constraint.SetCoefficient(y, -1)
      constraint.SetCoefficient(x[i][j][k], k)

# Constraint 4: A course may be conducted at most one time in an course room
for i in range(1,N+1):
  constraint = mip_solver.Constraint(1, 1)
  for j in range(1,M+1):
    for k in range(1,N+1):
      constraint.SetCoefficient(x[i][j][k], 1)

# Constraint 5: A course n_i must be put into a room m_j with capacity c(j)
for i in range(1,N+1):
  for j in range(1,M+1):
    constraint = mip_solver.Constraint(0, c[j])
    for k in range(1,N+1):
      constraint.SetCoefficient(x[i][j][k], d[i])

# Define objective
obj = mip_solver.Objective()
obj.SetCoefficient(y, 1)
obj.SetMinimization()

mip_solver.SetTimeLimit(30000)

# Solve and count elapsed time
start_time = time.time()
status = mip_solver.Solve()
end_time = time.time()



# Print solution
if status == mip_solver.OPTIMAL or status == mip_solver.FEASIBLE:
  obj_value = int(obj.Value())
  solution_matrix = []
  for i in range(obj_value+1):
    solution_matrix.append([-1 for _ in range(M+1)])
  for k in range(1,obj_value+1):
    for j in range(1,M+1):
      for i in range(1,N+1):
        if x[i][j][k].solution_value() == 1:
            solution_matrix[k][j] = i
  printSolution()
else:
  print('No solution found.')
