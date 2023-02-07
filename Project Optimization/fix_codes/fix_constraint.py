import ortools
import sys
# Integer Linear Programming
from ortools.linear_solver import pywraplp
# Constraint Programming
from ortools.sat.python import cp_model
# Timer
import time

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
        solution.append([solution_matrix[i][j], cp_solver.Value(x[i]),j])
  solution = sorted(solution, key= lambda x: x[0])
  for i in solution:
    print(*i)
# Constraint Programming

# Initianate a model
model = cp_model.CpModel()

# Define variables

# Variable x[i]
x = [model.NewIntVar(1, N, f'x[{i}]') for i in range(N+1)]

# Variable y[i][j]
y = [[model.NewIntVar(0, 1, f'y[{i}][{j}]') for j in range(M+1)] for i in range(N+1)]

# Define constraints

# Constraint 1: Pairs of conflicting courses may not be put in the same period 
for pair in p:
  model.Add(x[pair[0]] != x[pair[1]])

# Constraint 2: An course room may be assigned at most one course in a period
for i in range(1,N+1):
  model.Add(sum(y[i]) == 1)

# Constraint 3: Courses with same period may not share an course room
for j in range(1,M+1):
  for i1 in range(1,N):
    for i2 in range(i1 + 1, N+1):
      b = model.NewBoolVar(f'b[{j}][{i1}][{i2}]')
      model.Add(y[i1][j] + y[i2][j] <= 1).OnlyEnforceIf(b)
      model.Add(x[i1] == x[i2]).OnlyEnforceIf(b)
      model.Add(x[i1] != x[i2]).OnlyEnforceIf(b.Not())

# Constraint 4: A course n_i must be put into a room m_j with adequate capacity c(j)
for i in range(1,N+1):
  model.Add(sum([y[i][j] * c[j] for j in range(M+1)]) >= d[i])

# Define objective
cp_obj = model.NewIntVar(1, N, 'obj')
model.AddMaxEquality(cp_obj, x)
model.Minimize(cp_obj)

# Instantiate a CP solver 
cp_solver = cp_model.CpSolver()
cp_solver.parameters.max_time_in_seconds = 40.0

# Solve and count used time
start_time = time.process_time()
status = cp_solver.Solve(model)
end_time = time.process_time()

# Print solution
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
  obj_value = int(cp_solver.Value(cp_obj)) # Objective value
  solution_matrix = []
  for i in range(obj_value+1):
    solution_matrix.append([-1 for _ in range(M+1)])
  for i in range(1, N+1):
    for j in range(1, M+1):
      if cp_solver.Value(y[i][j]) == 1:
        solution_matrix[int(cp_solver.Value(x[i]))][j] = i
        break
  printSolution()
else:
  print('Not found solution.')