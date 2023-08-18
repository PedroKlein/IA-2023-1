from typing import Tuple, Union
from .board import Board

class GameState(object):
    """
    The game state is simply the board 
    configuration and the player to move.
    All the "hard work" is done in the 
    board.Board class
    """

    game_name = "Othello"

    def __init__(self, board:Board, player:str) -> None:
        """
        Initializes the Game state with the given board and player to move.
        You can access the attributes self.board and self.player directly for convenience.

        :param board: the board configuration
        :param player: the player to move (can be none if the state is terminal)
        """
        self.board = board
        self.player = player

    def is_terminal(self) -> bool:
        """
        Returns whether this state is terminal
        """
        return self.board.is_terminal_state()

    def is_legal_move(self, move:Tuple[int,int]) -> bool:
        """
        Returns whether the given move is legal in this state
        """
        return self.board.is_legal(move, self.player)

    def legal_moves(self) -> set:
        """
        Returns a set of legal moves in this state
        """
        return self.board.legal_moves(self.player)

    def winner(self) -> Union[str,None]:
        """
        Returns the string representation of the winner of the game
        (if this is a terminal state)
        """
        return self.board.winner()

    def get_board(self) -> Board:
        """
        Returns the board configuration
        """
        return self.board

    def copy(self) -> 'GameState':
        """
        Returns a copy of this state
        """
        return GameState(self.board.copy(), self.player)
    
    def next_state(self, move:Tuple[int,int]) -> 'GameState':
        """
        Returns the next state given the move.
        The next state is created as a new object
        (i.e. the move is not processed in-place)
        :param move: move in x,y (col,row) coordinates
        """
        next_board = self.board.copy()
        if not next_board.process_move(move, self.player):
            raise ValueError("Invalid move: %s" % str(move))

        opponent = Board.opponent(self.player)
        
        # alternates the player, but checkes if it has valid moves
        # also, if neither the opponent nor the player have
        # valid moves, then the next player is None
        next_player = None
        if next_board.has_legal_move(opponent):
            next_player = opponent
        elif next_board.has_legal_move(self.player):
            next_player = self.player

        next_state = GameState(next_board, next_player)

        return next_state
