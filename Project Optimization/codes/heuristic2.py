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


#GREEDY ALGORITHM
print('Heuristic 2')
conflicts = {} #conflicts[i] = list of exams that cannot be administered in the same period as exam i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

print('\nPeriod', 'Room', 'Exam', sep='\t')

sortedExams = sorted([(d[i], i) for i in range(N)], reverse=True) #sort exams in ascending order of capacity

schedule = [] #schedule[i, k] = exam administered in period i+1 and room k+1
period = 0
start_time = time.time()
while sortedExams: #sequentially fill each period with as many exams as possible until all exams have been scheduled
    schedule.append([None] * M)
    for room in range(M):
        for exam in sortedExams: #consider more popular exams first
            if exam[0] <= c[room]: #if a hall has adequate capacity
                #check if any exam already scheduled in this period has common candidates with the one being considered
                noConflict = True
                if exam[1] in conflicts:
                    for scheduledExam in schedule[period]:
                        if scheduledExam in conflicts[exam[1]]:
                            noConflict = False
                            break
                if noConflict: #schedule exam in period and room and remove from list of exams to schedule
                    schedule[period][room] = exam[1]
                    sortedExams.remove(exam)
                    break
    period += 1
#PRINT RESULT
end_time = time.time()

print(f'\nUsed time is {(end_time - start_time) * 1000} milliseconds')

print(f'\nThe number of periods to administer all exams is {period}.')

for pe in range(period): #print schedule by period
    if pe % 2 == 0:
        print(f'Day {pe // 4 + 1}:')
    print(f'\tPeriod {pe + 1}:')
    for room in range(M):
        exam = schedule[pe][room]
        conflictsOfThisExam = [e + 1 for e in conflicts.get(exam, [])]
        if exam != None:
            print(f'\t\tRoom {room + 1} (capacity = {c[room]}): Exam {exam + 1} (expected attendants = {d[exam]}, exams with common candidates = {conflictsOfThisExam})')