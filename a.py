#tester: https://open.kattis.com/problems/interactivetictactoe
# be careful, list() is passed by reference
INF = 1 << 63

memo = dict()
def hash(table: list[list[str]], turn: int) -> int:
    val = 0
    for r in table:
        for c in r:
            val = 3 * val + '.ox'.index(c)
    return val * 3 + turn

def isValidTable(table: list[list[str]], turn: int) -> bool:
    pass

def gameOver(table: list[list[str]]) -> tuple[bool, int]:
    x = 'x'
    o = 'o'
    
    for k in range(3):
        # column checking
        xCount, oCount = 0, 0
        for i in range(3):
            xCount += table[i][k] == x
            oCount += table[i][k] == o
        if xCount == 3:
            return True, 1
        if oCount == 3:
            return True, -1
                
        # row checking
        xCount, oCount = 0, 0
        for j in range(3):
            xCount += table[k][j] == x
            oCount += table[k][j] == o
        if xCount == 3:
            return True, 1
        if oCount == 3:
            return True, -1
                
    # diag1 checking
    xCount, oCount = 0, 0
    for i in range(3):
        xCount += table[i][i] == x
        oCount += table[i][i] == o
    if xCount == 3:
        return True, 1
    if oCount == 3:
        return True, -1

    # diag2 checking
    xCount, oCount = 0, 0
    for i in range(3):
        xCount += table[i][2 - i] == x
        oCount += table[i][2 - i] == o
    if xCount == 3:
        return True, 1
    if oCount == 3:
        return True, -1
    
    draw = True
    for r in table:
        if '.' in r:
            draw = False
            break
    return draw, 0


def instantWin(table: list[list[str]], turn: int) -> tuple[int, int]:
    # assert(not gameOver(table, turn)[0])
    # table may be invalid but its okay
    x = 'x'
    if not turn:
        x = 'o'
    
    for k in range(3):
        # column checking
        dotCount, xCount = 0, 0
        for i in range(3):
            xCount += table[i][k] == x
            dotCount += table[i][k] == '.'
        if dotCount == 1 and xCount == 2:
            for i in range(3):
                if table[i][k] == '.':
                    return i, k
                
        # row checking
        dotCount, xCount = 0, 0
        for j in range(3):
            xCount += table[k][j] == x
            dotCount += table[k][j] == '.'
        if dotCount == 1 and xCount == 2:
            for j in range(3):
                if table[k][j] == '.':
                    return k, j
                
    # diag1 checking
    dotCount, xCount = 0, 0
    for i in range(3):
        xCount += table[i][i] == x
        dotCount += table[i][i] == '.'
    if dotCount == 1 and xCount == 2:
        for i in range(3):
            if table[i][i] == '.':
                return i, i
            
    # diag2 checking
    dotCount, xCount = 0, 0
    for i in range(3):
        xCount += table[i][2 - i] == x
        dotCount += table[i][2 - i] == '.'
    if dotCount == 1 and xCount == 2:
        for i in range(3):
            if table[i][2 - i] == '.':
                return i, 2 - i
            
    return -1, -1

# x: max
# o: min
def minimaxImplement(table: list[list[str]], turn: bool, alpha: int, beta: int) -> tuple[int, int, int]:
    h = hash(table, turn)
    if h in memo:
        return memo[h]

    isOver, score = gameOver(table)
    if isOver:
        memo[h] = score, -1, -1
        return score, -1, -1
    
    iy, ix = instantWin(table, turn)
    if iy != -1 and ix != -1:
        memo[h] = (1 if turn else -1), iy, ix
        return (1 if turn else -1), iy, ix
    
    iy, ix = instantWin(table, turn ^ 1)
    if iy != -1 and ix != -1:
        table[iy][ix] = 'ox'[turn]
        score, _, _ = minimaxImplement(table, turn ^ 1, alpha, beta)
        table[iy][ix] = '.'
        memo[h] = score, iy, ix
        return score, iy, ix

    val = -INF if turn else INF
    y, x = -1, -1
    cut = False
    for i in range(3):
        for j in range(3):
            if table[i][j] != '.':
                continue
            table[i][j] = 'ox'[turn]
            nval, _, _ = minimaxImplement(table, turn ^ 1, alpha, beta)
            table[i][j] = '.'
            # x turn
            if turn:
                if val < nval:
                    val, y, x = nval, i, j
                if val >= beta:
                    cut = True
                    break
                alpha = max(alpha, val)
            # o turn
            else:
                if val > nval:
                    val, y, x = nval, i, j
                if val <= alpha:
                    cut = True
                    break
                beta = min(beta, val)

        if cut:
            break
    
    memo[h] = val, y, x
    return val, y, x

def minimaxTicTacToe(table: list[list[str]], turn: int) -> tuple[int, int]:
    # assert(isValidTable(table, turn))
    _, i, j = minimaxImplement(table, turn, -INF, INF)
    return i, j

from sys import stdout
def answer(a: list[list[str]]) -> None:
    for r in a:
        print(''.join(r))
    stdout.flush()

if __name__ == '__main__':
    t = input().strip()
    while True:
        a = [list(input().strip()) for _ in range(3)]
        i, j = minimaxTicTacToe(a, 1)
        if i == -1 and j == -1:
            break
        a[i][j] = 'x'
        answer(a)
        if gameOver(a)[0]:
            break
