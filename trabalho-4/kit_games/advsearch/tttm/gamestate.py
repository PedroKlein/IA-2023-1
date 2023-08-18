from typing import Tuple, Union
from .board import Board

class GameState:

    game_name = "Tic-Tac-Toe Misere"

    def __init__(self, board: Board, player: str):
        self.board = board
        self.player = player

    def is_terminal(self) -> bool:
        return self.board.is_full() or self.winner() is not None

    def is_legal_move(self, move: Tuple[int, int]) -> bool:
        """
        Checks whether the given move (x, y) is legal in this state.
        """
        col, row = move
        return 0 <= row < 3 and 0 <= col < 3 and self.board.is_empty(row, col)

    def legal_moves(self) -> set:
        moves = set()
        for row in range(3):
            for col in range(3):
                if self.is_legal_move((col, row)):
                    moves.add((col, row))
        return moves

    def winner(self) -> Union[str, None]:
        loser = self.board.check_loser()
        if loser == 'B':
            return 'W'
        elif loser == 'W':
            return 'B'
        else:
            return None

    def get_board(self) -> Board:
        return self.board

    def copy(self) -> 'GameState':
        new_state = GameState(self.board.copy(), self.player)
        return new_state

    def next_state(self, move: Tuple[int, int]) -> 'GameState':
        if not self.is_legal_move(move):
            raise ValueError("Invalid move.")
        
        new_state = self.copy()
        col, row = move
        new_state.board.place_marker(self.player, row, col)

        # Toggle the player for the next move
        new_state.player = 'B' if self.player == 'W' else 'W'

        return new_state
