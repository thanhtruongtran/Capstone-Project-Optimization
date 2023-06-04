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
N = 6 
M = 2
d = [27, 25, 33, 23, 29, 26]
c = [40, 41]
K = 3
p = [[6, 4], [2, 3], [1, 6]]

# Backtracking 

end = 1000000
conflict = [[] for _ in range(N+1)]

for k in p:
  u, v = k[0], k[1]
  conflict[u].append(v)
  conflict[v].append(u)

# assign period
period = [-1] * (N+1)

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
  if u == N+1:
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
dfs(1, 1)
end_time = time.process_time()

# Solution
if end != 1000000:
  print(f'Objective value: {end + 1}')
else:
  print('No found solution.')
print('------------------')
print(f'Used time: {1000*(end_time - start_time)} milliseconds')