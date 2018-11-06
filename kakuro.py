import itertools

def generate_sums():
    for a in range(1,10):
        for b in range(a+1,10):
            yield [a,b]
            for c in range(b+1,10):
                yield [a,b,c]
                for d in range(c+1,10):
                    yield [a,b,c,d]
                    for e in range(d+1,10):
                        yield [a,b,c,d,e]
                        for f in range(e+1,10):
                            yield [a,b,c,d,e,f]
                            for f in range(e+1,10):
                                yield [a,b,c,d,e,f]
                                for g in range(f+1,10):
                                    yield [a,b,c,d,e,f,g]
                                    for h in range(g+1,10):
                                        yield [a,b,c,d,e,f,g,h]
                                        for i in range(h+1,10):
                                            yield [a,b,c,d,e,f,g,h,i]
                                            for j in range(i+1,10):
                                                yield [a,b,c,d,e,f,g,h,i,j]

def get_sums():
    sums = {i:{} for i in range(3,46)}
    for s in generate_sums():
        a = sum(s)
        l = len(s)
        try:
            if s not in sums[a][l]:
                sums[a][l].append(s)
        except KeyError:
            sums[a][l] = [s]
    return sums
S = get_sums()

class BruteForceError(Exception):
    pass

class Board(object):
    def __init__(self,board):
        for r,row in enumerate(board):
            for c,cell in enumerate(row):
                if cell == '.':
                    board[r][c] = list(range(1,10))
        self.board = board
        self.R = len(board)
        self.C = len(board[0])

    def __iter__(self):
        return iter(self.board)

    def __getitem__(self,i):
        return self.board[i]

    def __eq__(self,other):
        for ra,rb in zip(self,other):
            for ca,cb in zip(ra,rb):
                if ca != cb:
                    return False
        return True

    def copy(self):
        board = []
        for row in self.board:
            board.append([])
            for cell in row:
                if isinstance(cell,list):
                    board[-1].append([i for i in cell])
                else:
                    board[-1].append(cell)
        return Board(board)
    
    def has_error(self):
        return self.has_empty_cell()

    def has_empty_cell(self):
        for row in self.board:
            for cell in row:
                if isinstance(cell,list):
                    if len(cell) == 0:
                        return True
        return False

def print_board(board):
    for r in board:
        for c in r:
            print(c,end='\t')
        print()
    print()

def is_solved(board):
    for r,row in enumerate(board):
        for c,cell in enumerate(row):
            if isinstance(cell,list):
                if len(cell) != 1:
                    return False
    return True

def bruteforce(board,cell=None,index=0):
    old_board = board.copy()
    if cell is not None:
        r,c = cell
    else:
        m = 10
        for r,row in enumerate(board):
            for c,cell in enumerate(row):
                if isinstance(cell,list):
                    if 1 < len(cell) < m:
                        m = len(cell)
                        mc = (r,c)
        r,c = mc
    board[r][c] = [board[r][c][index]]
    return board,(old_board,(r,c),index)

def single_eliminate(board,r,c,value):
    dr = r+1
    while dr < board.R and not isinstance(board[dr][c],str):
        try:
            board[dr][c].remove(value)
        except ValueError:
            pass
        dr += 1
    dr = r-1
    while dr > 0 and not isinstance(board[dr][c],str):
        try:
            board[dr][c].remove(value)
        except ValueError:
            pass
        dr -= 1
    dc = c+1
    while dc < board.C and not isinstance(board[r][dc],str):
        try:
            board[r][dc].remove(value)
        except ValueError:
            pass
        dc += 1
    dc = c-1
    while dc > 0 and not isinstance(board[r][dc],str):
        try:
            board[r][dc].remove(value)
        except ValueError:
            pass
        dc -= 1
    return board

def subsolve(board,n,group):
    l = len(group)
    valid_choice = []
    valid_sums = []
    s = []
    for i,j in group:
        s += board[i][j]
    existing_choices = set(s)
    for s in S[n][l]:
        if set(s) == existing_choices.intersection(s):
            valid_choice += s
            valid_sums.append(s)
    to_remove = []
    for cell in group:
        r,c = cell
        for v in board[r][c]:
            if v not in valid_choice:
                to_remove.append(v)
        for i in to_remove[::-1]:
            try:
                board[r][c].remove(i)
            except ValueError:
                pass
    ok_to_keep = {i:{i:False for i in board[cell[0]][cell[1]]} for i in range(l)}
    for s in valid_sums:
        for p in itertools.permutations(s):
            works = True
            for i,pairs in enumerate(zip(p,tuple(board[r][c] for r,c in group))):
                if pairs[0] not in pairs[1]:
                    works = False
                    break
            if works:
                for i,v in enumerate(p):
                    ok_to_keep[i][v] = True
    for index,values in ok_to_keep.items():
        for value,status in values.items():
            if not status:
                r,c = group[index]
                try:
                    board[r][c].remove(value)
                except ValueError:
                    pass
    return board

def solve(board):
    board = Board(board)
    guesses = []
    while not is_solved(board):
        try:
            print_board(board)
            before = board.copy()
            for r,row in enumerate(board):
                for c,cell in enumerate(row):
                    if isinstance(cell,list) and len(cell) == 1:
                        board = single_eliminate(board,r,c,cell[0])
                    elif ',' in cell:
                        down,right = map(int,cell.split(','))
                        if down > 0:
                            group = []
                            dr = r + 1
                            while dr < board.R and not isinstance(board[dr][c],str):
                                group.append((dr,c))
                                dr += 1
                            board = subsolve(board,down,group)
                        if right > 0:
                            group = []
                            dc = c + 1
                            while dc < board.C and not isinstance(board[r][dc],str):
                                group.append((r,dc))
                                dc += 1
                            board = subsolve(board,right,group)
            if board.has_error():
                raise BruteForceError()
            if before == board:
                board,guess = bruteforce(board)
                guesses.append(guess)
        except BruteForceError:
            guess = guesses.pop(-1)
            board,cell,index = guess
            board = bruteforce(board,cell,index+1)
    return board

#board = [
#    ['x','3,0','4,0'],
#    ['0,3','.','.'],
#    ['0,4','.','.']
#]
board = [
    ['x','18,0','11,0','18,0'],        
    ['0,11','.','.','.'],        
    ['0,22','.','.','.'],        
    ['0,14','.','.','.'],        
]

"""
board = [
    [   'x', '4,0','7,0', '6,0',    'x',   'x','3,0','16,0',  'x',  'x'],
    [ '0,6',   '.',  '.',   '.',    'x','28,4',  '.',   '.',  'x',  'x'],
    [ '0,7',   '.',  '.',   '.','23,17',   '.',  '.',   '.','3,0','4,0'],
    [   'x','0,14',  '.',   '.',    '.',   '.','0,7',   '.',  '.',  '.'],
    [   'x',   'x',  'x', '0,7',    '.',   '.',  'x', '0,4',  '.',  '.'],
    [   'x', '3,0','4,0','0,16',    '.',   '.','3,0',   'x',  'x',  'x'],
    [ '0,4',   '.',  '.','13,0',  '0,4',   '.',  '.', '7,0','6,0',  'x'],
    ['0,12',   '.',  '.',   '.', '3,11',   '.',  '.',   '.',  '.','4,0'],
    [   'x',   'x','0,7',   '.',    '.',   '.','0,7',   '.',  '.',  '.'],
    [   'x',   'x','0,4',   '.',    '.',   'x','0,6',   '.',  '.',  '.'],
]
"""

board = solve(board)
print_board(board)

