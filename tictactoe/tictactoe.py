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
    number_of_xs = 0
    number_of_os = 0
    for row in board:
        for element in row:
            if element == "X":
                number_of_xs += 1
            elif element == "O":
                number_of_os += 1
    # since X makes the first move , when they are equal it is X's turn otherwise it is O's .
    if number_of_xs - number_of_os:
        next_player = "O"
    else:
        next_player = "X"

    return next_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for x in range(3):
        for y in range(3):
            if board[x][y] == EMPTY:
                possible_actions.add((x, y))
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # first make a deepcopy of the object
    new_board = copy.deepcopy(board)
    # check whether it is possible to apply the wanted action, if not
    if board[action[0]][action[1]] == EMPTY:
        new_board[action[0]][action[1]] = player(board)
    else:
        raise Exception("impossible move")

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for element in ("X", "O"):
        # check horizontally
        for row in range(3):
            if board[row][0] == element and board[row][1] == element and board[row][2] == element:
                return element

        # check vertically
        for col in range(3):
            if board[0][col] == element and board[1][col] == element and board[2][col] == element:
                return element

        # check diagonally
        if (board[0][0] == element and board[1][1] == element and board[2][2] == element) or (board[0][2] == element and board[1][1] == element and board[2][0] == element):
            return element

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check whether there is a winner
    if winner(board) != None:
        return True
    # there is no winner check whether the table is full or not
    else:
        for row in board:
            for element in row:
                if element == EMPTY:
                    return False
        return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # since the game is over , it is enough just check whether there is winner
    winner_of_game = winner(board)
    if winner_of_game == "X":
        return 1
    elif winner_of_game == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # if the game is over return None
    if terminal(board):
        return None
    # the game is not over find the optimal move:
    else:
        # first find whose turn it is
        game_player = player(board)
        # if player is X , then it would want to make the value max therefore call max_of_minimums
        if game_player == "X":
            return max_of_minimums(board)[1]
        # it is O's turn it would want to make the score as low as possible
        else:
            return min_of_maximums(board)[1]


"""
functions needed to find the optimal move , one of them finds the best action to maximize the the value so that current player wins , the other one finds the best action to minimize the value so that the opponent wins. by calling them recursively we assumed the opponent plays optimally and minimax function finds the best move for the AI  

"""


def max_of_minimums(board):
    if terminal(board):
        return (utility(board), (0, 0))
    else:
        possible_actions = actions(board)
        maximizing_move_info = (-2, (0, 0))
        for action in possible_actions:
            temp = min_of_maximums(result(board, action))
            if temp[0] > maximizing_move_info[0]:
                maximizing_move_info = (temp[0], action)
                # alpa beta prunning. If it is equals to 1, there is no need to look for other actions since this action already has the maximum possible value which is 1. all the other actions will produce a value less than or equal to 1
                if temp[0] == 1:
                    return maximizing_move_info

    return maximizing_move_info


def min_of_maximums(board):
    if terminal(board):
        return (utility(board), (0, 0))
    else:
        possible_actions = actions(board)
        minimizing_move_info = (2, (0, 0))
        for action in possible_actions:
            temp = max_of_minimums(result(board, action))
            if temp[0] < minimizing_move_info[0]:
                minimizing_move_info = (temp[0], action)
                # alpa beta prunning. If it is equals to -1, there is no need to look for other actions since this action already has the minimum possible value which is -1. all the other actions will produce a value greater than or equal to -1
                if temp[0] == -1:
                    return minimizing_move_info

    return minimizing_move_info
