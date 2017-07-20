# -*- coding: utf-8 -*-
from test_input import SUDOKU_9x9
from itertools import permutations, product
import copy


class Board:
    __board = []
    __found = {}
    __suggestions = {}
    __try_cnt = 0

    def __init__(self, board):
        self.__board = board
        for i in range(9):
            for j in range(9):
                self.__suggestions[(i, j)] = [x for x in range(1, 10)]

        #

    @property
    def found(self):
        return self.__found

    @property
    def suggestions(self):
        return self.__suggestions

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
            print("\nThere {} {} {} to solve.".format('is' if cnt < 2 else 'are', cnt, 'field' if cnt == 1 else 'fields'))

    def analyze_board(self):
        """
        Goes through every field on the SUDOKU board
        """
        for i, j in ((i, j) for i in range(9) for j in range(9)):
            self.analyze_field(i, j)

    def analyze_field(self, i, j):
        if (i, j) not in self.__found:
            field_value = self.__board[i][j]
            if field_value > 0:
                self.__found[(i, j)] = field_value
                self.__suggestions[(i, j)] = []
                self.update_suggestions(i, j, field_value)
            else:
                if len(self.__suggestions[(i, j)]) == 1:
                    print("a", i, j)
                    print(self.__suggestions[(i, j)])
                    self.__found[(i, j)] = copy.deepcopy((self.__suggestions[(i, j)]))
                    self.__board[i][j] = field_value

                    self.__suggestions[(i, j)] = []
                    self.update_suggestions(i, j, field_value)
                    self.__try_cnt = 0

    def update_suggestions(self, i, j, field_value):
        self.delete_suggestions_vertically(j, field_value)
        self.delete_suggestions_horizontally(i, field_value)
        self.delete_suggestions_square(i, j, field_value)

    def update_board(self, i, j, value):
        self.__board[i, j] = value

    def solve(self):
        while self.__try_cnt < 10:
            self.analyze_board()
            self.__try_cnt += 1

    def delete_suggestions_vertically(self, column_number, value):
        """
        Deletes all the suggestions of found number in the column.
        :param column_number:
        :param value:
        :return:
        """
        for row_nr in range(9):
            suggestions = self.__suggestions[(row_nr, column_number)]
            # print(suggestions)
            try:
                suggestions.pop(suggestions.index(value))
            except ValueError:
                pass

    def delete_suggestions_horizontally(self, row_nr, value):
        """
        Deletes all the suggestions of found number in the column.
        :param column_number:
        :param value:
        :return:
        """
        for column_nr in range(9):
            suggestions = self.__suggestions[(row_nr, column_nr)]
            # print(suggestions)
            try:
                suggestions.pop(suggestions.index(value))
            except ValueError:
                pass

    def delete_suggestions_square(self, row_nr, col_nr, value):
        rows_range , col_range = self.__select_square(row_nr, col_nr)
        for indexes in product(range(*rows_range), range(*col_range)):
            suggestions = self.__suggestions[indexes]
            try:
                suggestions.pop(suggestions.index(value))
            except ValueError:
                pass
        pass

    @staticmethod
    def __select_square(i, j):
        l_02 = [0, 1, 2]
        l_35 = [3, 4, 5]
        l_68 = [6, 7, 8]
        if i in l_02 and j in l_02:
            return (0, 3), (0, 3)
        elif i in l_02 and j in l_35:
            return (0, 3), (3, 6)
        elif i in l_02 and j in l_68:
            return (0, 3), (6, 9)

        elif i in l_35 and j in l_02:
            return (3, 6), (0, 3)
        elif i in l_35 and j in l_35:
            return (3, 6), (3, 6)
        elif i in l_35 and j in l_68:
            return (3, 6), (6, 9)
        elif i in l_68 and j in l_02:
            return (6, 9), (0, 3)
        elif i in l_68 and j in l_35:
            return (6, 9), (3, 6)
        elif i in l_68 and j in l_68:
            return (6, 9), (6, 9)


a = Board(SUDOKU_9x9)
a.display_board()

a.analyze_board()
# a.solve()
# a.display_board()

suggs = a.suggestions
print(suggs[(7,7)])
# for i, j in ((i, j) for i in range(9) for j in range(9)):
#     print(suggs[(i, j)])
# print(a.found)

# for a in product(range(3), range(3)):
#     print(a, suggs[a])
# print(suggs[(8, 1)])


