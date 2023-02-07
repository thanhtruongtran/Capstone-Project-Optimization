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

#GREEDY ALGORITHM

conflicts = {} #conflicts[i] = list of exams that cannot be administered in the same period as exam i+1
for pair in p:
    conflicts.setdefault(pair[0], []).append(pair[1])
    conflicts.setdefault(pair[1], []).append(pair[0])

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

solution = []
for pe in range(period): #print schedule by period
    for room in range(M):
        exam = schedule[pe][room]
        conflictsOfThisExam = [e + 1 for e in conflicts.get(exam, [])]
        if exam != None:
            solution.append([exam+1,pe+1,room+1])
solution = sorted(solution, key= lambda x: x[0])
for i in solution:
    print(*i)

# print(f'Used time: {1000*(end_time - start_time)} milliseconds')