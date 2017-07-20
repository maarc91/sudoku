# -*- coding: utf-8 -*-
from test_input import SUDOKU_9x9, SUDOKU_9x9_v2
from itertools import product


class Board:
    """
    Class of a SUDOKU board.
    Contains information about numbers written into the board
    and suggestions for new ones.
    """
    __board = []
    __suggestions = {}
    __try_cnt = 0

    def __init__(self, board):
        self.__board = board
        self.display_board()
        for i, j in ((i, j) for i in range(9) for j in range(9)):
            self.__suggestions[(i, j)] = [x for x in range(1, 10)]

        for i, j in ((i, j) for i in range(9) for j in range(9)):
            field_value = self.__board[i][j]
            if field_value > 0:
                self.__suggestions[(i, j)] = []
                self.update_suggestions(i, j, field_value)
        self.solve()

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
            row = [x if x > 0 else " " for x in row]
            if not i % 3:
                print("+-------+-------+-------+")
            print("|{}  {}  {}|{}  {}  {}|{}  {}  {}|".format(*row))
        print("+-------+-------+-------+")
        print("\nThere {} {} {} to solve.".format('is' if cnt < 2 else 'are',
                                                  cnt,
                                                  'field' if cnt == 1 else 'fields'))

    def solve(self):
        while self.__try_cnt < 10:
            self.try_write_numbers()
            self.__try_cnt += 1

    def set_field_number(self, i, j, new_value):
        """
        Sets new value to the field and clears suggestion about the field.
        :param i: int
        :param j: int
        :param new_value: int
        """
        self.__board[i][j] = new_value
        self.update_suggestions(i, j, new_value)

    def update_suggestions(self, i, j, field_value):
        self.__suggestions[(i, j)] = []
        self.delete_suggestions_in_column(j, field_value)
        self.delete_suggestions_in_row(i, field_value)
        self.delete_suggestions_in_square(i, j, field_value)

    def delete_suggestions_in_column(self, col_nr, value):
        """
        Deletes all the suggestions of found number in the column.
        :param col_nr:
        :param value:
        :return:
        """
        for row_nr in range(9):
            suggestions = self.__suggestions[(row_nr, col_nr)]
            try:
                suggestions.pop(suggestions.index(value))
            except ValueError:
                pass

    def delete_suggestions_in_row(self, row_nr, value):
        """
        Deletes all the suggestions of found number in the column.
        :param row_nr:
        :param value:
        :return:
        """
        for col_nr in range(9):
            suggestions = self.__suggestions[(row_nr, col_nr)]
            try:
                suggestions.pop(suggestions.index(value))
            except ValueError:
                pass

    def delete_suggestions_in_square(self, row_nr, col_nr, number):
        """
        Deletes all instances of number in the suggestions of the square.
        :param row_nr:
        :param col_nr:
        :param number:
        :return:
        """
        rows_range, cols_range = self.__select_square(row_nr, col_nr)
        for indexes in product(range(*rows_range), range(*cols_range)):
            suggestions = self.__suggestions[indexes]
            try:
                suggestions.pop(suggestions.index(number))
            except ValueError:
                pass
        pass

    def try_write_numbers(self):
        """
        Checks if any number is unique for this
        :return:
        """
        for i, j in ((i, j) for i in range(9) for j in range(9)):
            if not self.__board[i][j]:
                for number in self.__suggestions[(i, j)]:
                    if self.check_if_unique_in_row(number, i):
                        self.set_field_number(i, j, number)
                        break
                    if self.check_if_unique_in_column(number, j):
                        self.set_field_number(i, j, number)
                        break
                    if self.check_if_unique_in_square(number, i, j):
                        self.set_field_number(i, j, number)
                        break

        for i, j in ((i, j) for i in range(9) for j in range(9)):
            if not self.__board[i][j]:
                for number in self.__suggestions[(i, j)]:
                    if self.check_if_unique_in_square(number, i, j):
                        self.set_field_number(i, j, number)
                        break

    def check_if_unique_in_row(self, number, row_nr):
        all_suggestions = []
        for j in range(9):
            all_suggestions.extend(self.__suggestions[(row_nr, j)])
        if all_suggestions.count(number) == 1:
            return True
        return False

    def check_if_unique_in_column(self, number, col_nr):
        all_suggestions = []
        for row_nr in range(9):
            all_suggestions.extend(self.__suggestions[(row_nr, col_nr)])
        if all_suggestions.count(number) == 1:
            return True
        return False

    def check_if_unique_in_square(self, number, row_nr, col_nr):
        all_suggestions = []
        rows_range, cols_range = self.__select_square(row_nr, col_nr)
        for indexes in product(range(*rows_range), range(*cols_range)):
            all_suggestions.extend(self.__suggestions[indexes])
        if all_suggestions.count(number) == 1:
            return True
        return False

    @staticmethod
    def __select_square(i, j):
        l_02 = [0, 1, 2]
        l_35 = [3, 4, 5]
        l_68 = [6, 7, 8]
        if i in l_02 and j in l_02:
            ret = (0, 3), (0, 3)
        elif i in l_02 and j in l_35:
            ret = (0, 3), (3, 6)
        elif i in l_02 and j in l_68:
            ret = (0, 3), (6, 9)
        elif i in l_35 and j in l_02:
            ret = (3, 6), (0, 3)
        elif i in l_35 and j in l_35:
            ret = (3, 6), (3, 6)
        elif i in l_35 and j in l_68:
            ret = (3, 6), (6, 9)
        elif i in l_68 and j in l_02:
            ret = (6, 9), (0, 3)
        elif i in l_68 and j in l_35:
            ret = (6, 9), (3, 6)
        elif i in l_68 and j in l_68:
            ret = (6, 9), (6, 9)
        return ret


a = Board(SUDOKU_9x9)
a.display_board()

b = Board(SUDOKU_9x9_v2)
b.display_board()

