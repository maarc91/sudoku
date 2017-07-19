# -*- coding: utf-8 -*-
from test_input import SUDOKU_9x9


class Board:
    __board = []
    __found = {}
    __solving = {}

    def __init__(self, board):
        self.__board = board

    @property
    def found(self):
        return self.__found

    def display_board(self):
        """
        Method prints the SUDOKU board.
        """
        print("The SUDOKU Board")
        cnt = 0
        for i, row in enumerate(self.__board):
            cnt += row.count(0)
            row = [x if x > 0 else " " for x in row ]
            if not i % 3:
                print("+-------+-------+-------+")
            print("|{}  {}  {}|{}  {}  {}|{}  {}  {}|".format(*row))
        else:
            print("+-------+-------+-------+")
            print(f"\nThere {'is' if cnt < 2 else 'are'} {cnt} {'field' if cnt == 1 else 'fields'} to solve.")

    def analyze(self):
        """
        Analyzes the SUDOKU board
        """
        for i in range(9):
            for j in range(9):
                if self.__board[i][j] > 0:
                    self.__found[(i, j)] = self.__board[i][j]

a = Board(SUDOKU_9x9)
a.display_board()
