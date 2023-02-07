import ortools
# Integer Linear Programming
from ortools.linear_solver import pywraplp
# Constraint Programming
from ortools.sat.python import cp_model
# Timer
import time
# Randomizer
import random as rd
# Math
from math import ceil
from math import factorial
def comb(x, y):
  return factorial(x)/(factorial(y) * factorial(x - y))
# Array
from array import *
# Numpy
import numpy as np
# Itertools
from itertools import combinations
# Data Reader
# filename = genData(n, m, d, c, k)
filename = 'data-N6-M2-d20-40-c15-45-K3.txt'
def readData(filename):
  with open(filename) as f:
    content = [[int(j) for j in i.split()] for i in f.read().splitlines()]
  N, d, M, c, K = content[0][0], content[1], content[2][0], content[3], content[4][0]
  p = [[content[5 + i][0] - 1, content[5 + i][1] - 1] for i in range(K)]
  print(f'N = {N}', f'd = {d}', f'M = {M}', f'c = {c}', f'K = {K}', f'p = {p}', sep = '\n')
  return N, d, M, c, K, p
N, d, M, c, K, p = readData(filename)
# Solution Printer
def printSolution():
  # Print the objective value
  print(f'The minimum number periods needed: {obj_value}, equivalent to: {ceil(obj_value / 4)} days.')
  print('------------------')
  # Print the solution matrix
  for i in range(obj_value):
    print(f'Period {i + 1}')
    for j in range(M):
      if solution_matrix[i][j] != -1:
        print(f'\tRoom {j + 1}: Course {solution_matrix[i][j] + 1}, attendants {d[solution_matrix[i][j]]}, capacity {c[j]}.')

# Constraint Programming
print('Constraint Programming')
print('------------------')


# Initianate a model
model = cp_model.CpModel()

# Define variables

# Variable x[i]
x = [model.NewIntVar(1, N, f'x[{i}]') for i in range(N)]

# Variable y[i][j]
y = [[model.NewIntVar(0, 1, f'y[{i}][{j}]') for j in range(M)] for i in range(N)]

# Define constraints

# Constraint 1: Pairs of conflicting courses may not be put in the same period 
for pair in p:
  model.Add(x[pair[0]] != x[pair[1]])

# Constraint 2: An course room may be assigned at most one course in a period
for i in range(N):
  model.Add(sum(y[i]) == 1)

# Constraint 3: Courses with same period may not share an course room
for j in range(M):
  for i1 in range(N - 1):
    for i2 in range(i1 + 1, N):
      b = model.NewBoolVar(f'b[{j}][{i1}][{i2}]')
      model.Add(y[i1][j] + y[i2][j] <= 1).OnlyEnforceIf(b)
      model.Add(x[i1] == x[i2]).OnlyEnforceIf(b)
      model.Add(x[i1] != x[i2]).OnlyEnforceIf(b.Not())

# Constraint 4: A course n_i must be put into a room m_j with adequate capacity c(j)
for i in range(N):
  model.Add(sum([y[i][j] * c[j] for j in range(M)]) >= d[i])

# Define objective
cp_obj = model.NewIntVar(1, N, 'obj')
model.AddMaxEquality(cp_obj, x)
model.Minimize(cp_obj)

# Instantiate a CP solver 
cp_solver = cp_model.CpSolver()
cp_solver.parameters.max_time_in_seconds = 40.0

# Solve and count used time
start_time = time.time()
status = cp_solver.Solve(model)
end_time = time.time()

# Print solution
if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
  obj_value = int(cp_solver.Value(cp_obj)) # Objective value
  solution_matrix = []
  for i in range(obj_value):
    solution_matrix.append([-1 for _ in range(M)])
  for i in range(N):
    for j in range(M):
      if cp_solver.Value(y[i][j]) == 1:
        solution_matrix[int(cp_solver.Value(x[i]) - 1)][j] = i
        break
  printSolution()
else:
  print('Not found solution.')
print('------------------')

print(f'Used time: {1000*(end_time - start_time)} milliseconds')