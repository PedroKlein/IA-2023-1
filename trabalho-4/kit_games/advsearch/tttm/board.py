from typing import Tuple, Union

class Board:
    """
    A board implementation for the tic-tac-toe misere game
    """

    
    BLACK = 'B'
    WHITE = 'W'
    EMPTY = '.'

    def __init__(self):
        self.board = [['.' for _ in range(3)] for _ in range(3)]

    @staticmethod
    def from_string(board_str: str) -> 'Board':
        lines = board_str.strip().split('\n')
        if len(lines) != 3 or any(len(line) != 3 for line in lines):
            raise ValueError("Invalid board string representation")

        board = Board()
        for row, line in enumerate(lines):
            for col, cell in enumerate(line):
                if cell in ['B', 'W', '.']:
                    board.board[row][col] = cell
                else:
                    raise ValueError("Invalid cell value in the board string representation")

        return board

    def __str__(self):
        return '\n'.join([' '.join(row) for row in self.board])
    
    def decorated_str(self, colors=False, move=None, highlight_flipped=False) -> str:
        # Create a decorated board with coordinates outside the main board
        decorated_board = [[' ' for _ in range(7)] for _ in range(7)]
        
        # Add column coordinates
        for col in range(3):
            decorated_board[0][col*2 + 2] = str(col)

        for row in range(3):
            # Add row coordinate
            decorated_board[row*2 + 2][0] = str(row)
            for col in range(3):
                decorated_board[row*2 + 2][col*2 + 2] = self.board[row][col]

        # Format the decorated board as a string
        return '\n'.join([' '.join(row) for row in decorated_board])

        # Format the decorated board as a string
        return '\n'.join([' '.join(row) for row in decorated_board])

    def place_marker(self, player, row, col):
        self.board[row][col] = player

    def is_empty(self, row, col):
        return self.board[row][col] == '.'

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == '.':
                    return False
        return True

    def check_loser(self):
        # Check rows, columns, and diagonals for a loser
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != '.':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != '.':
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != '.':
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != '.':
            return self.board[0][2]

        return None
    
    def copy(self):
        new_board = Board()
        new_board.board = [row[:] for row in self.board]
        return new_board