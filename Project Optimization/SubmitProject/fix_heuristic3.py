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
N,M,d,c,K,p =input()
c.insert(0,0)
d.insert(0,0)

conflicts = {} #conflicts[i] = list of exams that cannot be administered in the same period as exam i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

sortedRooms = sorted([(c[i], i) for i in range(1,M+1)]) #sort halls in ascending order of capacity
sortedRooms.insert(0,0)
result = [0,[None] * (M+1)] #result[i, k] = exam administered in period i+1 and room k+1
def heuristic_3():
    for exam in range(1,N+1): #sequentially assign a period and a room to each exam
        stop = False
        for period in range(1,len(result)+1): #consider existing periods first 
            for room in range(1,M+1): #consider smaller halls first to save bigger ones for other exams
                capacity = sortedRooms[room][0]
                roomIndex = sortedRooms[room][1]
                if capacity >= d[exam] and result[period][roomIndex] == None:
                    noConflict = True
                    if exam in conflicts:
                        for otherExam in result[period]:
                            if otherExam in conflicts[exam]:
                                noConflict = False
                                break
                    if noConflict:
                        result[period][roomIndex] = exam
                        print(exam, period, room, sep=' ') #print schedule by exam
                        stop = True
                        break
            if stop:
                break
            if period == len(result) - 1:
                #if this exam cannot be held in any existing period, set up a new period
                result.append([None] * (M+1))
    return len(result) - 1, result

#PRINT RESULT
start_time = time.time()
obj_value, solution_matrix = heuristic_3()
end_time = time.time()



# print(f'\nSolution found in {(end_time - start_time) * 1000} milliseconds')

# numberOfDays = ceil(len(result) / 4)
# print(f'\nThe number of days to administer all exams is {numberOfDays}.')

# def printSolution():
#   # Print the objective value
#   print(f'The minimum number periods needed: {obj_value}, equivalent to: {ceil(obj_value / 4)} days.')
#   print('------------------')
#   # Print the solution matrix
#   for i in range(1, obj_value):
#     print(f'Period {i}')
#     for j in range(1,M+1):
#       if solution_matrix[i][j] != None:
#         print(f'\tRoom {j}: Course {solution_matrix[i][j]}, attendance {d[solution_matrix[i][j]]}, capacity {c[j]}.')


# printSolution()