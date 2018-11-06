def summation_inc(terms,n):
    L = len(terms)
    if terms[0] >= n-L+1:
        return terms
    for i in range(L-1,-1,-1):
        if terms[i] < n-L+i:
            break
    terms[i] += 1
    itr = 1
    for j in range(i+1,L):
        terms[j] = terms[i] + itr
        itr += 1
    return terms
    
def get_summations(value,n,term_limit=False):
    if not term_limit:
        term_limit = value
    sums = []
    temp = [i for i in range(n)]
    while temp[0] < value-n+1:
        if sum(temp) == value:
            sums.append([i for i in temp])
        summation_inc(temp,term_limit)
    return sums
    
def solve_inc(indexes,boundaries):
    i = len(indexes)-1
    while i >= 0:
        if indexes[i] == boundaries[i]-1:
            indexes[i] = 0 
            i += -1
        else:
            indexes[i] += 1
            return indexes
    raise IndexError

def valid_solution(soln,solution):
    if sum(soln) == solution:
        for i in soln:
            if soln.count(i) > 1:
                return False
        return True
    return False


def solve(equation,solution):
    indexes = [0]*len(equation)
    bounds = [len(i) for i in equation]
    solns = []
    while True:
        try:
            soln = []
            for i,index in enumerate(indexes):
                soln.append(equation[i][index])
            if valid_solution(soln,solution):
                solns.append([i for i in soln])
            indexes = solve_inc(indexes,bounds)
        except:
            break
    return solns

#     12/ 12/ 10/ 
# 4/ |  3|  1|
# 21/|  9|  4|  8|
# 9/     |  7|  2|

eq1 = [[1,3,4],[1,3]]
s1 = 4

eq2 = [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]
s2 = 12

eq3 = [[i for i in range(1,10)]]*5
s3 = 22

class Cell:
    def __init__(self,h_sum,v_sum,left,right,up,down,*args,**kwargs):
        self.h_sum = h_sum
        self.v_sum = v_sum
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def get_h_group(self):
        group = [self]
        itr = self.right
        while itr is not None:
            group.append(itr)
            itr = itr.right
        itr = self.left
        while itr is not None:
            group.insert(0,itr)
            itr = itr.left
        return group

    def get_v_group(self):
        pass

class Board:
    cells = []
    def __init__(self,cells,*args,**kwargs):
        self.cells = cells


print solve(eq3,s3)
print get_summations(s3,5,10)
