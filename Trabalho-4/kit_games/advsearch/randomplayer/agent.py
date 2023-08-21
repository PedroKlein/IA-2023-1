import random
from typing import Tuple

from ..othello.gamestate import GameState


def make_move(state: 'GameState') -> 'Tuple[int, int]':
    """
    Returns a random move from the list of possible ones
    :param state: the game state to play from
    :return: (int, int)
    """
    legal_moves = list(state.legal_moves())
    return random.choice(legal_moves) if len(legal_moves) > 0 else (-1, -1)
