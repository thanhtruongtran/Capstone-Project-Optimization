from math import ceil
import time

#READ INPUT

def readData(filename):
    with open(filename) as f:
        content = [[int(j) for j in i.split()] for i in f.read().splitlines()]
    N, d, M, c, K = content[0][0], content[1], content[2][0], content[3], content[4][0]
    p = [[content[5 + i][0] - 1, content[5 + i][1] - 1] for i in range(K)]
    print(f'N = {N}', f'd = {d}', f'M = {M}', f'c = {c}', f'K = {K}', f'p = {p}', sep = '\n')
    print('------------------')
    return N, d, M, c, K, p
filename = 'data-N6-M2-d20-40-c15-45-K3.txt'
N, d, M, c, K, p = readData(filename)

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

#GREEDY ALGORITHM
print('Heuristic 1')

# List of (capacity, room) are sorted by capacity in ascending order 
sorted_c = sorted([(c[i], i) for i in range(M)])

# Conflicts
conflicts = {} # conflicts[i] = list of courses that cannot be administered in the same period as course i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

def heuristic_2():
  result = [[-1] * M] # initiate with first period 
                      # Result[i, k] = course exam administered in period i+1 and room k+1
  for exam in range(N): #sequentially assign a period and a room to each course
    nextCourse = False
    for period in range(len(result) + 1): #consider existing periods first
      if period == len(result):
        #if this exam cannot be held in any existing period, create a new period
        result.append([-1] * M) # new period with M rooms
      not_ThisPeriod = False
      if exam in conflicts:
        for otherCourse in result[period]:
          if otherCourse in conflicts[exam]:
            not_ThisPeriod = True
            break
        if not_ThisPeriod == True:
          continue 
      for room  in range(M): #consider smaller rooms first to save bigger ones for other courses
        capacity = sorted_c[room][0]
        roomIndex = sorted_c[room][1]
        if result[period][roomIndex] == -1 and capacity >= d[exam]:
          result[period][roomIndex] = exam
          nextCourse = True
          break
      if nextCourse == True:
        break
  return len(result), result

start_time = time.time()
obj_value, solution_matrix = heuristic_2()
end_time = time.time()

# Result
printSolution()
print('------------------')

print(f'Used time: {1000*(end_time - start_time)} milliseconds')