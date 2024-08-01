"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X
    countx,counto = 0,0
    for row in board:
        countx += row.count(X)
        counto += row.count(O)
    if countx-counto == 1: 
        return O
    return X 

    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    for i in range(0,3):
        for j in range(0,3):
            if board[i][j] == EMPTY:
                action.add((i,j))
    return action




def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] not in (0,1,2) and action[1] not in (0,1,2):
        raise Exception("Not valid action")
    newboard = copy.deepcopy(board) 
    newboard[action[0]][action[1]]= player(newboard) 
    return newboard



def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(0,3):
        if board[i] == [X,X,X]:
            return X
        if board[i] == [O,O,O]:
            return O
    for i in range(0,3):
        lis = []
        for j in range(0,3):
            lis.append(board[j][i])
        if lis == [X,X,X]:
            return X
        if lis == [O,O,O]:
            return O
    diag1 = [board[i][i] for i in range(3)]
    if diag1 == [X,X,X]:
        return X
    if diag1 == [O,O,O]:
        return O
    diag2 = [board[i][2-i] for i in range(3)]    
    if diag2 == [X,X,X]:
        return X
    if diag2 == [O,O,O]:
        return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None: 
        return True
    filled=True
    for i in range(3): 
        if EMPTY in board[i]:
            filled=False
            break
    if filled:
        return True
    return False

            


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0
 

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def Max_Value(board):
        if terminal(board):
            return utility(board)
        v = -2
        for action in actions(board):
            v = max(v,Min_Value(result(board,action)))
        return v
    def Min_Value(board):
        if terminal(board):
            return utility(board)
        v = 2
        for action in actions(board):
            v = min(v,Max_Value(result(board,action)))
        return v
    
    bot = player(board)

    if bot == X:
        optimal_move=((0,0),-2)
        for action in actions(board):
            next_score = Min_Value(result(board,action))
            if next_score > optimal_move[1]:
                optimal_move =(action,next_score)
        return optimal_move[0]
    
    else:
        optimal_move=((0,0),2)
        for action in actions(board):
            next_score = Max_Value(result(board,action))
            if next_score < optimal_move[1]:
                optimal_move =(action,next_score)
        return optimal_move[0]
    
    



