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
        print(f'\tRoom {j + 1}: Course {solution_matrix[i][j] + 1}, attendant {d[solution_matrix[i][j]]}, capacity {c[j]}.')
# Mixed Integer Programming
print('Mixed Integer Programming')
print('------------------')

# Instantiate a MIP mip_solver
mip_solver = pywraplp.Solver.CreateSolver('SCIP')

# Infinity
INF = mip_solver.infinity()

# Define variables

# Variable x[i][j][k]
x = [[[mip_solver.IntVar(0, 1, f'x[{i}][{j}][{k}]') for i in range(N)] for j in range(M)] for k in range(N)]

# Variable y
y = mip_solver.IntVar(0, N - 1, 'y')

# Define constraints

# Constraint 1: Pairs of conflicting courses may not be put in the same period
for i in range(K):
  u, v = p[i][0], p[i][1]
  for k in range(N):
    constraint = mip_solver.Constraint(0, 1)
    for j1 in range(M):
      for j2 in range(M):
        if j1 != j2:
          constraint.SetCoefficient(x[u][j1][k], 1)
          constraint.SetCoefficient(x[v][j2][k], 1)

# Constraint 2: An course room may be assigned at most one course in a period
for j in range(M):
  for k in range(N):
    constraint = mip_solver.Constraint(0, 1)
    for i in range(N):
      constraint.SetCoefficient(x[i][j][k], 1)

# Constraint 3: The number of periods (k.x[i,j,k] - y <= 0)
for i in range(N):
  for j in range(M):
    for k in range(N):
      constraint = mip_solver.Constraint(-INF, 0)
      constraint.SetCoefficient(y, -1)
      constraint.SetCoefficient(x[i][j][k], k)

# Constraint 4: A course may be conducted at most one time in an course room
for i in range(N):
  constraint = mip_solver.Constraint(1, 1)
  for j in range(M):
    for k in range(N):
      constraint.SetCoefficient(x[i][j][k], 1)

# Constraint 5: A course n_i must be put into a room m_j with capacity c(j)
for i in range(N):
  for j in range(M):
    constraint = mip_solver.Constraint(0, c[j])
    for k in range(N):
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
  obj_value = int(obj.Value() + 1)
  solution_matrix = []
  for i in range(obj_value):
    solution_matrix.append([-1 for _ in range(M)])
  for k in range(obj_value):
    for j in range(M):
      for i in range(N):
        if x[i][j][k].solution_value() == 1:
          solution_matrix[k][j] = i
  printSolution()
else:
  print('Not found solution.')
print('------------------')

print(f'Used time: {1000*(end_time - start_time)} milliseconds')