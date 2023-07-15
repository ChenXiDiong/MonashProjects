"""
Template for Programming Assignment FIT1045 - S2 2021
Sudoku

Version 3 (2021-09-22) - containing reference solutions for Part 1

Sudoku boards partially retrieved from
- https://puzzlemadness.co.uk
- https://sudokudragon.com
"""

########### Sudoku boards ##############################

small = [[1, 0, 0, 0],
         [0, 4, 1, 0],
         [0, 0, 0, 3],
         [4, 0, 0, 0]]

small2 = [[0, 0, 1, 0],
          [4, 0, 0, 0],
          [0, 0, 0, 2],
          [0, 3, 0, 0]]

big = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [4, 0, 0, 7, 8, 9, 0, 0, 0],
       [7, 8, 0, 0, 0, 0, 0, 5, 6],
       [0, 2, 0, 3, 6, 0, 8, 0, 0],
       [0, 0, 5, 0, 0, 7, 0, 1, 0],
       [8, 0, 0, 2, 0, 0, 0, 0, 5],
       [0, 0, 1, 6, 4, 0, 9, 7, 0],
       [0, 0, 0, 9, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 3, 0, 0, 0, 2]]

big2 = [[7, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 5, 0, 0, 0, 9, 0, 0, 0],
        [8, 0, 0, 0, 3, 0, 0, 4, 0],
        [0, 0, 0, 7, 6, 0, 0, 0, 8],
        [6, 2, 0, 0, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 3, 0, 7, 0],
        [0, 0, 0, 6, 0, 0, 9, 8, 0],
        [0, 0, 0, 0, 2, 7, 3, 0, 0],
        [0, 0, 2, 0, 8, 0, 0, 5, 0]]

big3 = [[0, 0, 8, 1, 9, 0, 0, 0, 6],
        [0, 4, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 7, 6, 0, 0, 1, 3, 0],
        [0, 0, 6, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 8, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 2, 0, 0, 5],
        [0, 0, 0, 0, 3, 0, 9, 0, 0],
        [0, 1, 0, 4, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 5, 7]]

big4 = [[0, 0, 0, 6, 0, 0, 2, 0, 0],
        [8, 0, 4, 0, 3, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 9, 0, 0, 0],
        [4, 0, 5, 0, 0, 0, 0, 0, 7],
        [7, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 0, 5, 0, 0, 0, 8],
        [3, 0, 0, 0, 7, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 1, 9, 0, 0],
        [0, 0, 0, 2, 0, 0, 0, 6, 0]]

giant = [[ 0,  0, 13,  0,  0,  0,  0,  0,  2,  0,  8,  0,  0,  0, 12, 15],
         [ 7,  8, 12,  2, 10,  0,  0, 13,  0,  0, 14, 11,  6,  9,  0,  4],
         [11, 10,  0,  0,  0,  6, 12,  5,  0,  3,  0,  0,  0, 14,  0,  8],
         [ 1,  0,  0,  0, 14,  0,  2,  0,  0,  4,  6,  0, 16,  3,  0, 13],
         [12,  6,  0,  3,  0,  0, 16, 11,  0, 10,  1,  7, 13, 15,  0,  0],
         [ 0, 13,  0,  0,  0, 15,  8,  0, 14,  0,  0,  0,  0, 16,  5, 11],
         [ 8,  0, 11,  9, 13,  0,  7,  0,  0,  0,  0,  3,  2,  4,  0, 12],
         [ 5,  0,  0, 16, 12,  9,  0, 10, 11,  2, 13,  0,  0,  0,  8,  0],
         [ 0,  0,  0,  0, 16,  8,  9, 12,  0,  0,  0,  0,  0,  6,  3,  0],
         [ 2, 16,  0,  0,  0, 11,  0,  0,  7,  0, 12,  6,  0, 13, 15,  0],
         [ 0,  0,  4,  0,  0, 13,  0,  7,  3, 15,  0,  5,  0,  0,  0,  0],
         [ 0,  7,  0, 13,  4,  5, 10,  0,  1,  0, 11, 16,  9,  0, 14,  2],
         [ 0,  2,  8,  0,  9,  0,  0,  0,  4,  0,  7,  0,  0,  5,  0,  0],
         [14,  0,  0,  0, 15,  2, 11,  4,  9, 13,  3,  0, 12,  0,  0,  0],
         [ 0,  1,  9,  7,  0,  0,  5,  0,  0, 11, 15, 12,  0,  0,  0,  0],
         [16,  3, 15,  0,  0, 14, 13,  6, 10,  1,  0,  2,  0,  8,  4,  9]]

giant2 = [[ 0,  5,  0,  0,  0,  4,  0,  8,  0,  6,  0,  0,  0,  0,  9, 16],
          [ 1,  0,  0,  0,  0,  0,  0, 13,  4,  0,  0,  7, 15,  0,  8,  0],
          [13,  0,  0,  0,  0,  7,  3,  0,  0,  0,  0,  9,  5, 10,  0,  0],
          [ 0, 11, 12, 15, 10,  0,  0,  0,  0,  0,  5,  0,  3,  4,  0, 13],
          [15,  0,  1,  3,  0,  0,  7,  2,  0,  0,  0,  0,  0,  5,  0,  0],
          [ 0,  0,  0, 12,  0,  3,  0,  5,  0, 11,  0, 14,  0,  0,  0,  9],
          [ 4,  7,  0,  0,  0,  0,  0,  0, 12,  0, 15, 16,  0,  0,  0,  0],
          [ 0,  0,  0,  0, 14,  0, 15,  0,  6,  9,  0,  0,  0,  0, 12,  0],
          [ 3,  0, 15,  4,  0, 13, 14,  0,  0,  0,  0,  1,  0,  0,  7,  8],
          [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  9, 10,  0,  0,  0,  0],
          [11,  0, 16, 10,  0,  0,  0,  0,  0,  7,  0,  0,  0,  3,  5,  0],
          [ 0,  0, 13,  0,  0,  0,  0,  0, 14,  0, 16, 15,  0,  9,  0,  1],
          [ 9,  0,  2,  0,  0, 14,  0,  4,  8,  0,  0,  0,  0,  0,  0,  0],
          [ 0, 14,  0,  0,  0,  0,  0, 10,  9,  0,  3,  0,  0,  0,  1,  7],
          [ 8,  0,  0,  0, 16,  0,  0,  1,  2, 14, 11,  4,  0,  0,  0,  3],
          [ 0,  0,  0,  1,  0,  0,  5,  0,  0, 16,  0,  6,  0, 12,  0,  0]]

giant3 = [[ 0,  4,  0,  0,  0,  0,  0, 12,  0,  1,  0,  0,  9,  0,  8,  0],
          [15, 14,  0,  0,  9,  0,  0, 13,  8,  0,  0, 10,  1,  0,  0,  0],
          [ 0,  7,  0,  0,  0,  0,  0,  8, 16,  0, 14,  0,  0,  2,  0,  0],
          [ 0,  0,  0,  9,  0,  0, 11,  0,  0,  0,  0,  0,  5,  0,  0, 15],
          [ 3,  0, 12,  0,  7,  0, 10,  0,  0, 11,  2,  0,  0,  0,  0,  6],
          [14,  8,  0,  0,  0, 12,  0,  6,  0,  0,  0, 16,  0,  0,  0, 10],
          [ 0, 16,  0,  0, 13,  0,  0,  0,  0,  0,  0,  0,  0,  0, 12,  0],
          [ 6,  0,  0,  0,  0,  8,  0,  5,  1,  7, 13,  0, 11,  0,  0, 14],
          [ 0,  0,  0,  2,  0,  0, 16,  0, 15, 12,  0,  3, 10,  7,  0,  0],
          [ 0,  9,  0,  5, 11,  0,  3,  0,  4, 13, 16,  0,  0, 15,  6,  0],
          [ 0,  0,  0,  0,  5,  4,  0,  0,  9,  6,  0,  2,  0,  0,  0,  0],
          [ 1,  0,  0,  0,  0, 15, 12,  0,  0,  0,  5,  0,  0,  0,  9,  0],
          [12, 10,  0, 15,  0,  1,  0,  0,  2,  9,  3,  4,  0,  0,  5,  0],
          [ 0,  0,  0,  3, 10,  0,  4,  0,  0, 15,  0,  0,  0,  0,  0,  0],
          [ 0,  0,  0,  0, 16,  0,  0,  0,  0,  0,  0,  0,  0,  0, 10, 11],
          [11,  6,  8,  0,  0,  0, 15,  0, 14,  0,  0,  0,  0, 13,  0,  2]]

sudokus = [[], [], [small, small2], [big, big2, big3, big4], [giant, giant2, giant3]]

########### Module functions ###########################

from math import sqrt

symbols = [' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G']

def print_board(board, hint=None):
    """
    Prints a given board to the console in a way that aligns the content of columns and makes
    the subgrids visible.

    Input : a Sudoku board (board) of size 4x4, 9x9, or 16x16,
            optionally the coordinates of a field where to display the hint symbol ('*')
    Effect: prints the board to the console 

    For example:

    >>> print_board(small2)
    -------
    |  |1 |
    |4 |  |
    -------
    |  | 2|
    | 3|  |
    -------
    >>> print_board(big)
    -------------
    |   |   |   |
    |4  |789|   |
    |78 |   | 56|
    -------------
    | 2 |36 |8  |
    |  5|  7| 1 |
    |8  |2  |  5|
    -------------
    |  1|64 |97 |
    |   |9  |   |
    |   | 3 |  2|
    -------------
    >>> print_board(giant2)
    ---------------------
    | 5  | 4 8| 6  |  9G|
    |1   |   D|4  7|F 8 |
    |D   | 73 |   9|5A  |
    | BCF|A   |  5 |34 D|
    ---------------------
    |F 13|  72|    | 5  |
    |   C| 3 5| B E|   9|
    |47  |    |C FG|    |
    |    |E F |69  |  C |
    ---------------------
    |3 F4| DE |   1|  78|
    |    |    |  9A|    |
    |B GA|    | 7  | 35 |
    |  D |    |E GF| 9 1|
    ---------------------
    |9 2 | E 4|8   |    |
    | E  |   A|9 3 |  17|
    |8   |G  1|2EB4|   3|
    |   1|  5 | G 6| C  |
    ---------------------
    """
    n = len(board)
    k = round(sqrt(n))
    for i in range(n):
        if i % k == 0:
            print('-'*(len(board)+k+1))
        for j in range(n):
            if j % k == 0:
                print('|', end='')
            if hint and hint[0]==i and hint[1]==j:
                print('*', end='')
            else:
                print(symbols[board[i][j]], end='')
        print('|')
    print('-'*(len(board)+k+1))

def subgrid_values(board, r, c):
    """
    Input : Sudoku board (board), row index (r), and column index (c)
    Output: list of all numbers that are present in the subgrid of the board related to the
            field (r, c)

    For example:

    >>> subgrid_values(small2, 1, 3)
    [1]
    >>> subgrid_values(big, 4, 5)
    [3, 6, 7, 2]
    >>> subgrid_values(giant2, 4, 5)
    [7, 2, 3, 5, 14, 15]
    """
    n = len(board)
    k = round(sqrt(n))
    res = []
    for i in range((r // k) * k, ((r // k) + 1) * k):
        for j in range((c // k) * k, ((c // k) + 1) * k):
            if board[i][j]:
                res.append(board[i][j])
    return res 


def options(board, r, c):
    """
    Input : Sudoku board (board), row index (r), and column index (c)
    Output: list of all numbers that player is allowed to place on field (r, c),
            i.e., those that are not already present in row r, column c,
            and subgrid related to field (r, c)

    For example:

    >>> options(small2, 0, 0)
    [2, 3]
    >>> options(big, 6, 8)
    [3, 8]
    >>> options(giant2, 1, 5)
    [2, 5, 6, 9, 11, 12, 16]
    """
    if board[r][c]:
        return []

    res = []
    n = len(board)
    k = round(sqrt(n))    
    col_vals = [board[s][c] for s in range(n)]
    row_vals = board[r]
    subgrid_vals = subgrid_values(board, r, c)
    for x in range(1, n+1):
        if x not in col_vals and x not in row_vals and x not in subgrid_vals:
            res.append(x)
    return res

def empty_fields(board):
    """
    Input : Sudoku board
    Output: list of fields, i.e., pairs of row and column indices, that are not
            empty (i.e., value is not equal to 0)
    """
    n = len(board)
    k = int(sqrt(n))
    res = []
    for i in range(n):
        for j in range(n):
            if not board[i][j]:
                res.append((i, j))
    return res

def hint(board):
    """
    Input : Sudoku board
    Output: field, i.e., pair of row and column index, with the minimum
            number of options among all empty-fields

    Hints are generated based in the number of available options for a field.
    Fields with less options are easier to fill for the player, hence, pointing
    to the minimum makes a useful hint.
    """
    fields = empty_fields(board)
    if not fields:
        return None
    min_field = fields[0]
    min_options = len(options(board, fields[0][0], fields[0][1]))
    for i, j in fields[1:]:
        opts = options(board, i, j)
        if len(opts) < min_options:
            min_field = (i, j)
            min_options = len(opts)
    return min_field

from copy import deepcopy

def rowcheck(board,row):
    rowlist = []
    for i in range(len(board)):
        if board[row][i] in rowlist:
            return False
        elif board[row][i]:
            rowlist.append(board[row][i])
    return True

def colcheck(board,col):
    collist = []
    for i in range(len(board)):
        if board[i][col] in collist:
            return False
        elif board[i][col]:
            collist.append(board[i][col])
    return True

def subgridcheck(board,r,c):
    n = len(board)
    k = round(sqrt(n))
    gridlist = []
    for i in range((r // k) * k, ((r // k) + 1) * k):
        for j in range((c // k) * k, ((c // k) + 1) * k):
            if board[i][j] in gridlist:
                return False
            elif board[i][j]:
                gridlist.append(board[i][j])
    return True

from random import shuffle,randint

def play(board):
    """
    Input : Sudoku board
    Effect: Allows user to play board via console
    """
    boards = [board]
    print_board(boards[-1])
    while True:
        if not empty_fields(boards[-1]):
            print('solved')
        inp = input().split(' ')
        if len(inp) == 3 and inp[0].isdecimal() and inp[1].isdecimal() and inp[2].isdecimal():
            i = int(inp[0])
            j = int(inp[1])
            x = int(inp[2])
            opt = options(boards[-1], i, j)
            if x in opt:
                boards.append(deepcopy(boards[-1]))
                boards[-1][i][j] = x
                print_board(boards[-1])
            else:
                print('invalid move; valid options:' + str(opt))
        elif len(inp)==3 and (inp[0] == 'n' or inp[0] == 'new') and inp[1].isdecimal() and inp[2].isdecimal():
            k = int(inp[1])
            d = int(inp[2])
            if k < len(sudokus) and 0 < d <= len(sudokus[k]):
                boards = [sudokus[k][d-1]]
                print_board(boards[-1])
            else:
                print('board not found')
        elif inp[0] == 'q' or inp[0] == 'quit':
            return
        elif inp[0] == 'u' or inp[0] == 'undo':
            if len(boards) > 1:
                boards = boards[:-1]
                print_board(boards[-1])
            else:
                print('nothing to undo')
        elif inp[0] == 'r' or inp[0] == 'restart':
            boards = boards[:1]
            print_board(boards[-1])
        elif inp[0] == 'h' or inp[0] == 'help':
            hnt = hint(boards[-1])
            print_board(boards[-1], hint=hnt)
            print(hnt, options(boards[-1], hnt[0], hnt[1]))
        elif inp[0] == 'i' or inp[0] == 'infer':
            inferred_board = inferred(boards[-1])
            print_board(inferred_board)
        elif inp[0] == 's' or inp[0] == 'solve':
            res = deepcopy(board)
            print_board(solve(res))
        elif len(inp)==2 and (inp[0] == 'g' or inp[0] == 'generate') and inp[1].isdecimal():
            k = int(inp[1])
            newboard = [[0 for i in range(1,k**2+1)] for i in range(1,k**2+1)]
            def gensol(board):
                if inferred(board) != board:
                    board = inferred(board)
                fields = empty_fields(board)
                if not fields:
                    return board
                hnt = hint(board)
                row,col = hnt[0], hnt[1]
                opt = options(board,row,col)
                """
                By adding in the shuffle() function into the options, the backtracking function selects a different option every time the generate function is called, and this selection branches into
                different ways, resulting in a random solution board being generated.
                """
                shuffle(opt)
                for o in opt:
                    board[row][col] = o
                    if not empty_fields(inferred(board)):
                        return inferred(board)
                    if solve(board):
                        sol = solve(board)
                        return sol
                    else:
                        board[row][col] = 0
                return False
            newboard = gensol(newboard)
            boards = [generate(newboard)]
            print_board(boards[-1])
        else:
            print('Invalid input')

########### Functions for Part II ########
"""
Assignment Part 1 Sample Solution is used as a template for Part 2
"""
def value_by_single(board, i, j):
    """
    Input : board, row, and column index
    Output: The correct value for field (i, j) in board if it can be inferred as
            either a forward or a backward single; or None otherwise. 
    
    For example:

    >>> value_by_single(small2, 0, 1)
    2
    >>> value_by_single(small2, 0, 0)
    3
    >>> value_by_single(big, 0, 0)
    """
    option_lst = options(board,i,j)
    if len(option_lst) == 1: #if there is only 1 possible value, return that value
        return option_lst[0]
    """
    Forward Single
    """
    #checking by the row:
    for item in option_lst:
        items_to_remove = []
        for m in range(len(board)):
            if m == j or board[i][m] == 0:
                continue
            elif item in options(board,i,m):
                items_to_remove.append(item)
        for item in items_to_remove:
            if item in option_lst:
                option_lst.remove(item)
        if len(option_lst) == 0:  #if there is an option that is only available to that field, return that value
            return option_lst[0]
    #checking by the column:
    for item in option_lst:
        items_to_remove = []
        for m in range(len(board)):
            if m == i or board[m][j] == 0:
                continue
            elif item in options(board,m,j):
                items_to_remove.append(item)
        for item in items_to_remove:
            if item in option_lst:
                option_lst.remove(item)
        if len(option_lst) == 1:  #if there is an option that is only available to that field, return that value
            return option_lst[0]
    """
    Backward Single
    """ 
    options_of_subgrid = []
    step = round(sqrt(len(board)))
    for a in range((i // step) * step, ((i // step) + 1) * step):
        for b in range((j // step) * step, ((j // step) + 1) * step):
            if board[a][b]:
                options_of_subgrid.append([None])
            else:
                options_of_subgrid.append(options(board,a,b))
            if a == i and b == j:
                checknum = len(options_of_subgrid)-1
    for i in range(len(options_of_subgrid)):
        if i == checknum:
            continue
        else:
            for value in options_of_subgrid[i]:
                if value in options_of_subgrid[checknum]:
                    options_of_subgrid[checknum].remove(value)
    if len(options_of_subgrid[checknum]) == 1:
        return options_of_subgrid[checknum][0]
    return None


def inferred(board):
    """
    Input : Sudoku board
    Output: new Soduko board with all values field from input board plus
            all values that can be inferred by repeated application of 
            forward and backward single rule

    For example board big can be completely inferred:

    >>> inferred(big) # doctest: +NORMALIZE_WHITESPACE
    [[2, 1, 3, 4, 5, 6, 7, 8, 9],
    [4, 5, 6, 7, 8, 9, 1, 2, 3],
    [7, 8, 9, 1, 2, 3, 4, 5, 6],
    [1, 2, 4, 3, 6, 5, 8, 9, 7],
    [3, 6, 5, 8, 9, 7, 2, 1, 4],
    [8, 9, 7, 2, 1, 4, 3, 6, 5],
    [5, 3, 1, 6, 4, 2, 9, 7, 8],
    [6, 4, 2, 9, 7, 8, 5, 3, 1],
    [9, 7, 8, 5, 3, 1, 6, 4, 2]]

    But function doesn't modify input board:

    >>> big # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [4, 0, 0, 7, 8, 9, 0, 0, 0],
     [7, 8, 0, 0, 0, 0, 0, 5, 6],
     [0, 2, 0, 3, 6, 0, 8, 0, 0],
     [0, 0, 5, 0, 0, 7, 0, 1, 0],
     [8, 0, 0, 2, 0, 0, 0, 0, 5], 
     [0, 0, 1, 6, 4, 0, 9, 7, 0],
     [0, 0, 0, 9, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 3, 0, 0, 0, 2]]

    In board big4 there is nothing to infer:
    
    >>> inferred(big4) # doctest: +NORMALIZE_WHITESPACE
    [[0, 0, 0, 6, 0, 0, 2, 0, 0],
     [8, 0, 4, 0, 3, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 9, 0, 0, 0], 
     [4, 0, 5, 0, 0, 0, 0, 0, 7],
     [7, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 0, 5, 0, 0, 0, 8],
     [3, 0, 0, 0, 7, 0, 0, 0, 4],
     [0, 0, 0, 0, 0, 1, 9, 0, 0],
     [0, 0, 0, 2, 0, 0, 0, 6, 0]]
    """
    inferred_board = deepcopy(board)
    count = 0
    for i in range(len(inferred_board)):
        for j in range(len(inferred_board)):
            if inferred_board[i][j] == 0:
                if value_by_single(inferred_board,i,j):
                    inferred_board[i][j] = value_by_single(inferred_board,i,j)
                    count += 1
    if count == 0:
        return inferred_board
    else:
        return inferred(inferred_board)

"""
In the solve function, the board is first scanned for empty fields. If there are no empty fields left on the board, it means that the board has been solved and the function will return the solved board. (base case)
If the board is not yet solved,  the function finds an empty field and get the options for that field using the options() function. Then, the function tries out each option and sees if it can yield a valid solution.
If the current option cannot allow the board to be solved any further, the function will backtrack to the previous phase and try again for other options. Ultimately the function can solve the board using backtracking.
"""
"""
The field to be solved is selected by the hint() function, where it returns the field with the least amount of options in the current board. In that way, the function does not need to iterate through that many options
as the "easily" solved fields would eliminate some of the wrong options from other fields.  
"""
"""
Inference can be implemented in each recursion before backtracking to help reduce the computational cost. If the inferred board has updates to the empty fields, I keep the board and pass it into the backtracking 
algorithm. Otherwise I just pass the current board to do backtracking normally. If all the remaining empty fields of the board only have one option left, it is not needed to backtrack anymore as by the solution can be 
generated using inference. This would save (possibly) a lot of backtracking recursions and thus it would require less time to fully generate the solution.
"""
def solve(board):
    if inferred(board) != board:
        board = inferred(board)
    fields = empty_fields(board)
    if not fields:
        return board
    hnt = hint(board)
    row,col = hnt[0], hnt[1]
    opt = options(board,row,col)
    for o in opt:
        board[row][col] = o
        if not empty_fields(inferred(board)):
            return inferred(board)
        if solve(board):
            sol = solve(board)
            return sol
        else:
            board[row][col] = 0
    return False

def isunique(board):
    res = deepcopy(board)
    res = solve(res)
    board=inferred(board)
    if not empty_fields(inferred(board)):
        return True
    hnt=hint(board)
    row,col = hnt[0],hnt[1]
    opt = options(board,row,col)
    for o in opt:
        board[row][col] = o
        temp = deepcopy(board)
        temp = solve(temp)
        if not empty_fields(temp) and temp != res:
            return False 
    return True


def generate(board):
    """
    The random solution board has already been generated in the play function upon the call 'g' or 'generate', therefore this function (ideally) only creates all the possible empty fields and returns
    a minimal sudoku board. This function creates random empty spaces in each iteration and is checked with the function isunique() to determine if the current board is still a unique board. It is done 
    by checking if the removal of the current non-zero field results in more than one of its options creating a different solution. If there is a second unique solution, then the isunique() function 
    will return False and therefore ending the generation function.
    """
    while isunique(board):
        i,j = randint(0,len(board)-1),randint(0,len(board)-1)
        board[i][j] = 0
    return board
            
########### Driver code (executed when running module) #

import doctest
doctest.testmod()

play(small)
