from math import ceil
import time
import sys

#READ INPUT

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
print(f'N = {N}', f'd = {d}', f'M = {M}', f'c = {c}', f'K = {K}', f'p = {p}', sep = '\n')

def printSolution():
  solution = []
  for i in range(1,obj_value+1):
    for j in range(M+1):
      if solution_matrix[i][j] != -1:
        solution.append([solution_matrix[i][j], i,j])
  solution = sorted(solution, key= lambda x: x[0])
  for i in solution:
    print(*i)

#GREEDY ALGORITHM
print('Heuristic 1')

# List of (capacity, room) are sorted by capacity in ascending order 
sorted_c = sorted([(c[i], i) for i in range(M+1)])

# Conflicts
conflicts = {} # conflicts[i] = list of courses that cannot be administered in the same period as course i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

def heuristic_1():
  result = [[-1] * (M+1)] # initiate with first period 
                      # Result[i, k] = course exam administered in period i+1 and room k+1
  for exam in range(1,N+1): #sequentially assign a period and a room to each course
    nextCourse = False
    for period in range(1,len(result) + 1): #consider existing periods first
      if period == len(result):
        #if this exam cannot be held in any existing period, create a new period
        result.append([-1] * (M+1)) # new period with M rooms
      not_ThisPeriod = False
      if exam in conflicts:
        for otherCourse in result[period-1]:
          if otherCourse in conflicts[exam]:
            not_ThisPeriod = True
            break
        if not_ThisPeriod == True:
          continue 
      for room  in range(1,M+1): #consider smaller rooms first to save bigger ones for other courses
        capacity = sorted_c[room][0]
        roomIndex = sorted_c[room][1]
        if result[period-1][roomIndex] == -1 and capacity >= d[exam]:
          result[period-1][roomIndex] = exam
          nextCourse = True
          break
      if nextCourse == True:
        break
  return len(result), result

start_time = time.time()
obj_value, solution_matrix = heuristic_1()
end_time = time.time()
print(obj_value)
print(solution_matrix)

# Result
printSolution()
print('------------------')

print(f'Used time: {1000*(end_time - start_time)} milliseconds')