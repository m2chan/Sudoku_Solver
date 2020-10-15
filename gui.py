# GUI using Tkinter

from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import tkinter.font as font

MARGIN = 15 
SIDE = 60 
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9 

class SudokuGUI(Frame):
    '''
    Tkinter UI which displays the board and allows the user to input values directly into the board
    '''

    def __init__(self, board):
        '''Initialize Tk frame'''
        self.sudoku = board
        self.parent = Tk()
        Frame.__init__(self, self.parent)

        self.row, self.col = -1, -1

        self.__initialize_gui()

    def __initialize_gui(self):
        '''
        Set up widgets
        '''

        myFont = font.Font(family='Arial', size=16)

        self.parent.title('Sudoku Solver')
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self, text='Clear board', command=self.__clear)
        clear_button.pack(fill=BOTH, side=BOTTOM)
        clear_button['font'] = myFont 
        solve_button = Button(self, text='Solve', command=self.__solve)
        solve_button.pack(fill=BOTH, side=BOTTOM)
        solve_button['font'] = myFont

        self.__draw_board()
        self.__draw_puzzle()

        self.canvas.bind('<Button-1>', self.__cell_clicked)
        self.canvas.bind('<Key>', self.__key_pressed)

    def __draw_board(self):
        '''
        Draw blank sudoku board
        '''

        for i in range(10):
            color = 'black' if i % 3 == 0 else 'gray'

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        '''
        Fill in numbers on the board
        '''

        self.canvas.delete('result')
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                cell = self.sudoku.board[i][j]
                answer = cell.number
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    self.canvas.create_text(x, y, text=answer, tags='numbers', fill='black', font=('Arial', 20))

    def __draw_cursor(self):
        '''
        Creates a border around the currently selected cell
        '''

        self.canvas.delete('cursor')
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle( x0, y0, x1, y1, outline='green2', tags='cursor')

    def __draw_result(self, success, time):
        '''
        Create rectangle output that shows if the solve completed or failed
        '''

        # Rectangle output dimenstions
        x0 = MARGIN + SIDE * 2.5
        y0 = MARGIN + SIDE * 3.5
        x1 = MARGIN + SIDE * 6.5
        y1 = MARGIN + SIDE * 5.5
        
        # Output either success message or invalid board
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        if success:
            self.canvas.create_rectangle(x0, y0, x1, y1, tags='result', fill='green', outline='black')
            
            self.canvas.create_text(
                x, y,
                text='Solved in\n {0:.4f}s!'.format(time), tags='result',
                fill='white', font=('Arial', 24)
            )
        else:
            self.canvas.create_rectangle(x0, y0, x1, y1, tags='result', fill='red', outline='black')
            
            self.canvas.create_text(
                x, y,
                text='Invalid board!', tags='result',
                fill='white', font=('Arial', 20)
            )

    def __cell_clicked(self, event):
        '''
        Selects a cell that has been clicked
        '''

        self.canvas.delete('result') 
        x, y = event.x, event.y

        # Get coordinates of the clicked cell and place curosr there
        if MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN:
            self.canvas.focus_set()
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        
        else:
            self.row, self.col = -1, -1

        self.__draw_cursor()

    def __go_next(self):
        '''
        Advance to the next cell on the board
        '''

        row = self.row
        col = self.col
        if col < 8:
            self.col += 1
        elif row < 8:
            self.row += 1
            self.col = 0
        else:
            self.row = 0
            self.col = 0

    def __key_pressed(self, event):
        '''
        Tracks and records key presses to navigate the board and enter numbers
        '''

        if self.row >= 0 and self.col >= 0:
            if event.keysym in ['Up', 'w']:
                self.row = ((self.row + 8) % 9)
            elif event.keysym in ['Down', 'Return', 's']:
                self.row = ((self.row + 10) % 9)
            elif event.keysym in ['Right', 'd', 'Tab']:
                self.col = ((self.col + 10) % 9)
            elif event.keysym in ['Left', 'a']:
                self.col = ((self.col + 8) % 9)
            elif event.keysym in ['Delete', 'BackSpace']:
                self.sudoku.board[self.row][self.col].reset()
            elif event.char != '' and event.char in '1234567890':
                self.sudoku.board[self.row][self.col].number = int(event.char)
                self.__go_next()

            self.__draw_puzzle()
            self.__draw_cursor()

    def __clear(self):
        '''
        Clears the board
        '''

        self.sudoku.clear()
        self.__draw_puzzle()

    def __solve(self):
        '''
        Solves the board and outputs message
        '''

        success, time = self.sudoku.solve()
        self.__draw_puzzle()
        self.__draw_result(success, time)
