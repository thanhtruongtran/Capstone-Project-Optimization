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


print('Heuristic 3')

startTime = time.time()

conflicts = {} #conflicts[i] = list of exams that cannot be administered in the same period as exam i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

sortedRooms = sorted([(c[i], i) for i in range(M)]) #sort rooms in ascending order of capacity
result = [[None] * M] #result[i, k] = exam administered in period i+1 and room k+1
print('\nExam', 'Period', 'Room', sep='\t')
for exam in range(N): #sequentially assign a period and a room to each exam
    stop = False
    for period in range(len(result) + 1): #consider existing periods first 
        for room in range(M): #consider smaller rooms first to save bigger ones for other exams
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
                    print(exam + 1, period + 1, room + 1, sep='\t') #print schedule by exam
                    stop = True
                    break
        if stop:
            break
        if period == len(result) - 1:
            #if this exam cannot be held in any existing period, set up a new period
            result.append([None] * M)

#PRINT RESULT

print(f'\nUsed time: {(time.time() - startTime) * 1000} milliseconds')

numberOfDays = ceil(len(result) / 4)
print(f'\nThe number of days to administer all exams is {numberOfDays}.')

if input('\nEnter "y" to see details. ').lower() in ("y", "yes"):
    for period in range(len(result)): #print schedule by period
        if period % 4 == 0:
            print(f'Day {period // 4 + 1}:')
        print(f'\tPeriod {period + 1}:')
        for room in range(M):
            exam = result[period][room]
            conflictsOfThisExam = [e + 1 for e in conflicts.get(exam, [])]
            if exam != None:
                print(f'\t\tRoom {room + 1} (capacity = {c[room]}): Exam {exam + 1} (expected attendants = {d[exam]}, exams with common candidates = {conflictsOfThisExam})')