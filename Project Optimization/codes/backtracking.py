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

# Backtracking 

end = 1000000
conflict = [[] for _ in range(N)]

for k in p:
  u, v = k[0], k[1]
  conflict[u].append(v)
  conflict[v].append(u)

# assign period
period = [-1] * N

# room
room = []
for _ in range(N):
  room.append([-1] * M)

def isPlaceable(u, slot):
  if period[u] >= 0:
    return False
  for v in conflict[u]:
    if period[v] == slot:
      return False
  return True

def dfs(u, slot):
  global end
  if u == N:
    end = min(end, slot)
    return
  if slot > end:
    return
  for j in range(M):
    if room[slot][j] == -1:
      for i in range(N):
        if isPlaceable(i, slot) and d[i] <= c[j]:
          period[i], room[slot][j] = slot, i
          dfs(u + 1, slot)
          period[i], room[slot][j] = -1, -1
  dfs(u, slot + 1)
  return

# Solve
start_time = time.process_time()
dfs(0, 0)
end_time = time.process_time()

# Solution
if end != 1000000:
  print(f'Objective value: {end + 1}')
else:
  print('No found solution.')
print('------------------')
print(f'Used time: {1000*(end_time - start_time)} milliseconds')