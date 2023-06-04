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
N,M,d,c,K,p =input()
d.insert(0,0)
c.insert(0,0)


# List of (capacity, room) are sorted by capacity in ascending order 
sorted_c = sorted([(c[i], i) for i in range(1,M+1)])
sorted_c.insert(0,0)
# Conflicts
conflicts = {} # conflicts[i] = list of courses that cannot be administered in the same period as course i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])


result = [0,[-1] * (M+1)] # initiate with first period 
                      # Result[i, k] = course exam administered in period i+1 and room k+1
def heuristic_2():
  for exam in range(1,N+1): #sequentially assign a period and a room to each course
    nextCourse = False
    for period in range(1,len(result) + 1): #consider existing periods first
      if period == len(result):
        #if this exam cannot be held in any existing period, create a new period
        result.append([-1] * (M+1)) # new period with M rooms
      not_ThisPeriod = False
      if exam in conflicts:
        for otherCourse in result[period]:
          if otherCourse in conflicts[exam]:
            not_ThisPeriod = True
            break
        if not_ThisPeriod == True:
          continue 
      for room in range(1,M+1): #consider smaller rooms first to save bigger ones for other courses
        capacity = sorted_c[room][0]
        roomIndex = sorted_c[room][1]
        if result[period][roomIndex] == -1 and capacity >= d[exam]:
          result[period][roomIndex] = exam #stick this exam to this period and room
          nextCourse = True
          break
      if nextCourse == True:
        break
  return len(result)-1, result

start_time = time.time()
obj_value, solution_matrix = heuristic_2()
end_time = time.time()

# Result

res = []
for period in range(1,len(result)):
    for room in range(1,M+1):
        if result[period][room] != -1:
            res.append([result[period][room], period, room])
res = sorted(res, key= lambda x: x[0])
for i in res:
    print(*i)

# print(f'Used time: {1000*(end_time - start_time)} milliseconds')