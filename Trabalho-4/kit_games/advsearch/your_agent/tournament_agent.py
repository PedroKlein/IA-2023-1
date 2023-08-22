import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move  # Certifique-se de ter o módulo minimax definido e importado corretamente.

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    return minimax_move(state, 4, evaluate_count)  # Chamando o algoritmo Minimax com a função de avaliação

def evaluate_count(state, player: str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the number of pieces of each color.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    player_pieces = state.get_board().num_pieces(player)
    opponent_pieces = state.get_board().num_pieces(Board.opponent(player))

    return player_pieces - opponent_pieces  # Retorna a diferença de peças entre os jogadores
