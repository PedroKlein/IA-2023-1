import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state: GameState) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # Chamar a função minimax_move para obter o melhor movimento usando a função evaluate_count.
    return minimax_move(state, max_depth=4, eval_func=evaluate_count)  # Você pode ajustar max_depth conforme necessário



def evaluate_count(board, player):
    if player is None:  # Caso em que nenhum jogador tem movimentos possíveis
        return 0

    player_pieces = board.get_board().num_pieces(player)  # Ajuste aqui
    opponent = Board.opponent(player)
    opponent_pieces = board.get_board().num_pieces(opponent)  # Ajuste aqui

    # Retorne a diferença entre as peças do jogador e do oponente como função de avaliação
    return player_pieces - opponent_pieces
