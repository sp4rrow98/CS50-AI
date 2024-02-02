"""
Tic Tac Toe Player
"""

import math
import copy
import random

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
    # Check if X has already played and return the player
    moves = 1
    for row in board:
        for move in row:
            if not move == EMPTY:
                moves += 1

    # Return the correct player
    if moves % 2 == 0:
        return (O)
    else:
        return (X)


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    list = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == EMPTY:
                list.add((i, j))
    return (list)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    try:
        turn = player(board)
        actionRow = action[0]
        actionCol = action[1]
        newBoard = copy.deepcopy(board)
        newBoard[actionRow][actionCol] = turn
        return (newBoard)
    except Exception as e:
        print("Error")


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]
        elif board[0][i] == board[1][i] == board[2][i]:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]

    if len(actions(board)) == 0:
        return ("None")

    return False


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    win = winner(board)
    if not win:
        return False
    else:
        return win


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        _, move = max_value(board)
        return move
    else:
        _, move = min_value(board)
        return move


def max_value(board):
    if terminal(board):
        return utility(board), None

    v = -math.inf
    best_move = None

    for action in actions(board):
        value, _ = min_value(result(board, action))
        if value > v:
            v = value
            best_move = action

    return v, best_move


def min_value(board):
    if terminal(board):
        return utility(board), None

    v = math.inf
    best_move = None

    for action in actions(board):
        value, _ = max_value(result(board, action))
        if value < v:
            v = value
            best_move = action

    return v, best_move