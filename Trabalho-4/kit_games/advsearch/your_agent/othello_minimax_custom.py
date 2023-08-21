import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    player_color = state.player
    return minimax_move(state, 4, evaluate_custom)

def evaluate_custom(state, player: str) -> float:
    """
    Evaluates an othello state from the point of view of the given player.
    If the state is terminal, returns its utility.
    If non-terminal, returns an estimate of its value based on the difference in the number of pieces.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    player_pieces = state.get_board().num_pieces(player)
    opponent_pieces = state.get_board().num_pieces(Board.opponent(player))

    if player_pieces + opponent_pieces == 64:  # If the game is over
        if player_pieces > opponent_pieces:
            return 1.0  # Player wins
        elif player_pieces < opponent_pieces:
            return -1.0  # Player loses
        else:
            return 0.0  # It's a draw
    else:
        return player_pieces - opponent_pieces  # Simple difference in piece count

# Note que esta é uma heurística muito simples e não leva em conta a posição das peças no tabuleiro
# ou outras estratégias avançadas. Você pode melhorá-la considerando outros fatores.
