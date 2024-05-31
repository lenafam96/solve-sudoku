#!/usr/bin/python
# -*- coding: utf-8 -*-

from random import randint, shuffle
# import pyautogui as pya


def print_board(board):
    """
    Prints the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        None.
    """

    boardString = ""
    for i in range(9):
        for j in range(9):
            boardString += str(board[i][j]) + " "
            if (j + 1) % 3 == 0 and j != 0 and j + 1 != 9:
                boardString += "| "

            if j == 8:
                boardString += "\n"

            if j == 8 and (i + 1) % 3 == 0 and i + 1 != 9:
                boardString += "- - - - - - - - - - - \n"
    print(boardString)


def find_empty(board):
    """
    Finds an empty cell in the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        tuple[int, int]|None: The position of the first empty cell found as a tuple of row and column indices, or None if no empty cell is found.
    """

    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def valid(board, pos, num):
    """
    Checks whether a number is valid in a cell of the sudoku board.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
        pos (tuple[int, int]): The position of the cell to check as a tuple of row and column indices.
        num (int): The number to check.

    Returns:
        bool: True if the number is valid in the cell, False otherwise.
    """

    for i in range(9):
        if board[i][pos[1]] == num:
            return False

    for j in range(9):
        if board[pos[0]][j] == num:
            return False

    start_i = pos[0] - pos[0] % 3
    start_j = pos[1] - pos[1] % 3
    for i in range(3):
        for j in range(3):
            if board[start_i + i][start_j + j] == num:
                return False
    return True


def solve(board):
    """
    Solves the sudoku board using the backtracking algorithm.

    Args:
        board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.

    Returns:
        bool: True if the sudoku board is solvable, False otherwise.
    """

    empty = find_empty(board)
    if not empty:
        return True

    for nums in range(1, 10):
        if valid(board, empty, nums):
            board[empty[0]][empty[1]] = nums

            if solve(board):  # recursive step
                return True
            board[empty[0]][empty[1]] = 0  # this number is wrong so we set it back to 0
    return False


def generate_board():
    """
    Generates a random sudoku board with fewer initial numbers.

    Returns:
        list[list[int]]: A 9x9 sudoku board represented as a list of lists of integers.
    """

    board = [[0 for i in range(9)] for j in range(9)]

    # Fill the diagonal boxes
    for i in range(0, 9, 3):
        nums = list(range(1, 10))
        shuffle(nums)
        for row in range(3):
            for col in range(3):
                board[i + row][i + col] = nums.pop()

    # Fill the remaining cells with backtracking
    def fill_cells(board, row, col):
        """
        Fills the remaining cells of the sudoku board with backtracking.

        Args:
            board (list[list[int]]): A 9x9 sudoku board represented as a list of lists of integers.
            row (int): The current row index to fill.
            col (int): The current column index to fill.

        Returns:
            bool: True if the remaining cells are successfully filled, False otherwise.
        """

        if row == 9:
            return True
        if col == 9:
            return fill_cells(board, row + 1, 0)

        if board[row][col] != 0:
            return fill_cells(board, row, col + 1)

        for num in range(1, 10):
            if valid(board, (row, col), num):
                board[row][col] = num

                if fill_cells(board, row, col + 1):
                    return True

        board[row][col] = 0
        return False

    fill_cells(board, 0, 0)

    # Remove a greater number of cells to create a puzzle with fewer initial numbers
    for _ in range(randint(55, 65)):
        row, col = randint(0, 8), randint(0, 8)
        board[row][col] = 0

    return board


# if __name__ == "__main__":
#     # board = generate_board()
#     # print_board(board)
#     board = [
#         [0,0,7,0,0,5,0,0,3],
#         [0,0,9,0,6,0,0,0,0],
#         [3,6,0,0,0,8,2,0,0],
#         [0,0,6,0,0,0,0,0,0],
#         [5,1,0,0,8,0,0,0,9],
#         [0,0,0,0,0,2,0,4,0],
#         [0,0,0,5,0,0,9,0,0],
#         [8,3,0,0,1,0,0,0,5],
#         [7,0,0,0,0,0,0,0,0],
#     ]
#
#     # with open('broad.csv', 'r') as f:
#     #     board = []
#     #     for line in f:
#     #         row = line.strip().split(',')
#     #         row = [int(x) if x != '' else 0 for x in row]
#     #         board.append(row)
#
#     # read board from xlsx file
#     board = pd.read_excel('board.xlsx', header=None).values.tolist()
#     for i in range(9):
#         for j in range(9):
#             board[i][j] = int(board[i][j]) if math.isnan(board[i][j]) == False else 0
#
#     solve(board)
#     print_board(board)
#     pya.hotkey('alt', 'tab')
#     # time.sleep(0.0001)
#     for i in range(9):
#         if i%2 == 0:
#             for j in range(9):
#                 pya.hotkey(str(board[i][j]))
#                 # time.sleep(0.0001)
#                 pya.hotkey('right')
#                 # time.sleep(0.0001)
#         else:
#             for j in range(8, -1, -1):
#                 pya.hotkey(str(board[i][j]))
#                 # time.sleep(0.0001)
#                 pya.hotkey('left')
#                 # time.sleep(0.0001)
#         pya.hotkey('down')
#         # time.sleep(0.0001)
