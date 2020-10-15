# Sudoku cell, board, and solver

from time import time
from gui import SudokuGUI

class Cell(object):
    '''
    Represents individual cells in board
    '''

    def __init__(self, row, column):
        self.row = row  
        self.column = column  
        self.checked_all_nums = False  
        self.number = 0  
        self.possible_numbers = set()  

    def try_new_number(self):
        '''
        Try a new number in the current cell
        '''

        self.number = self.possible_numbers.pop()
        self.checked_all_nums = not self.possible_numbers

    def set_possible_numbers(self, numbers):
        '''
        Determine the possible numbers for this cell
        '''

        self.possible_numbers = numbers
        self.checked_all_nums = not numbers

    def reset_number(self):
        '''
        Reset the number in this cell to 0 from the backtracking algorithm
        '''
        
        self.number = 0

    def reset(self):
        '''
        When no numbers are found, reset this cell completely
        '''

        self.checked_all_nums = False
        self.possible_numbers = set()
        self.number = 0


class Board(object):
    '''
    Represents a standard 9x9 sudoku board with methods to solve a board
    '''

    def __init__(self):
        self.board = [[Cell(r, c) for c in range(9)] for r in range(9)]

    @staticmethod
    def __difference(numbers):
        '''
        Determines the remaining possibilities for values

        Input arguments:
            numbers: Numbers to check
        '''

        return set(range(1, 10)) - set(numbers)

    @staticmethod
    def __validate(numbers):
        '''
        Checks if section of the board is valid

        Input arguments:
            numbers: Numbers to check
        '''

        numbers = list(filter(lambda n: n != 0, numbers))  # remove all 0s
        correct_numbers = set(numbers).issubset(set(range(1, 10)))
        no_duplicates = len(numbers) == len(set(numbers))
        return correct_numbers and no_duplicates

    def __get_row(self, row):
        '''
        Returns a row of numbers

        Input arguments:
            row: Row that we want all the numbers from 
        '''
        
        return [cell.number for cell in self.board[row]]

    def __get_column(self, column):
        '''
        Returns a column of numbers

        Input arguments:
            column: Column that we want all the numbers from 
        '''
        return [self.board[row][column].number for row in range(9)]

    def __get_square(self, row, column):
        '''
        Returns the 3x3 square of cells that the cell specified in function arguments is in

        Input arguments:
            row: Row of the cell that we want to check
            column: Column of the cell that we want to check 
        '''

        return [
            self.board[r][c].number
            for r in range(row - (row % 3), row + (3 - (row % 3)))
            for c in range(column - (column % 3), column + (3 - (column % 3)))
        ]

    def is_valid(self):
        '''
        Check the entire board by calling the __validate method on each column, row, and square
        '''
 
        for column in range(9):
            if not self.__validate(self.__get_column(column)):
                return False

        for row in range(9):
            if not self.__validate(self.__get_row(row)):
                return False
        
        for row in range(0, 9, 3):
            for column in range(0, 9, 3):
                if not self.__validate(self.__get_square(row, column)):
                    return False
        
        return True


    def possible_numbers(self, r, c):
        '''
        Determine all possible values at a given cell

        Input arguments:
            r: Row of the cell
            c: Column of the cell
        '''

        row = self.__get_row(r)
        column = self.__get_column(c)
        square = self.__get_square(r, c)
        return self.__difference(row + column + square)

    def solve(self):
        '''
        Solve the sudoku board using a backtracking algorithm
        '''

        # Check if the initial board is valid
        if not self.is_valid():
            return False, -1
    
        start = time()
        # Initialize a list that will hold all of the cells that we have tried to place a number in, and we will backtrack using this list
        attempted_cells = []
        
        # Begin iterating through all the rows and columns
        row = 0
        while row < 9:
            column = 0
            while column < 9:
                cell = self.board[row][column]
                backtracking = False
                if not cell.number:  # if the cell's number is 0

                    # Check that there are still numbers we haven't checked yet or if we created a list of possible numbers for this cell
                    if not cell.checked_all_nums and not cell.possible_numbers:
                        possible = self.possible_numbers(row, column)
                        cell.set_possible_numbers(possible)

                    # If the cell has possible numbers, one of these numbers
                    if cell.possible_numbers:
                        cell.try_new_number()
                        attempted_cells.append(cell)

                    # Otherwise backtrack to the previous cell
                    elif attempted_cells:
                        backtracking = True
                        cell.reset()  # complete reset this cell
                        prev_cell = attempted_cells.pop(-1)
                        prev_cell.reset_number()  # clear number
                        
                        # Set the row and column loop iterators back to this cell to run validation again
                        row = prev_cell.row
                        column = prev_cell.column

                    # Otherwise there are no possible solutions
                    else:
                        return False, -1

                # If backtracking condition not met, then continue progressing to next column
                if not backtracking:
                    column += 1

            # Move on to the next row after iterating through all columns
            row += 1

        # Solved suodoku board successfully
        end = time()  # finishing time
        return True, end - start

    def clear(self):
        [self.board[r][c].reset() for c in range(9) for r in range(9)]

    def __str__(self):
        '''
        Print board
        '''

        formatted_board = ""
        for i in range(9):
            formatted_board += str(self.__get_row(i))
            formatted_board += "\n"
        return formatted_board

if __name__ == '__main__':

    board = Board()  
    gui = SudokuGUI(board) 
    gui.mainloop()  