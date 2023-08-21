from typing import Tuple
from .minimax import minimax_move
from ..tttm.gamestate import GameState


def make_move(state: GameState) -> Tuple[int, int]:
    return minimax_move(state, -1, utility)


def utility(state: GameState, player: str) -> float:
    winner = state.winner()
    if winner == player:
        return 1000  # O jogador atual ganhou
    elif winner is None:
        return -100  # Empate
    else:
        return -1000  # O oponente ganhou


# para testar contra ele mesmo
# python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/your_agent/tttm_minimax.py

# contra random
# python server.py tttm advsearch/randomplayer/agent.py advsearch/your_agent/tttm_minimax.py

# contra humano
# python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/humanplayer/agent.py
