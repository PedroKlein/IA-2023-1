import random
from typing import Tuple
from ..othello.gamestate import GameState
from math import sqrt, log

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


class MCTSNode:
    def __init__(self, state: GameState, parent=None, last_move=None):
        self.state = state
        self.parent:GameState = parent
        self.children:GameState = []
        self.last_move: Tuple[int, int] = last_move
        self.visits = 0
        self.value = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.legal_moves())

    def best_child(self, exploration_weight=1.0):
        best_child = max(self.children, key=lambda child: child.value / (child.visits + 1e-6)
                         + exploration_weight * sqrt(log(self.visits + 1) / (child.visits + 1e-6)))
        return best_child




def make_move(state:GameState) -> Tuple[int, int]:
    """
    Returns a move for the given game state.
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    
    root = MCTSNode(state)

    iterations = 1000
    for _ in range(iterations):
        node = root

        # Selection and expansion
        while not node.state.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        if not node.state.is_terminal():
            unexpanded_moves = node.state.legal_moves() - {child.last_move for child in node.children}
            move = random.choice(list(unexpanded_moves))
            next_state = node.state.next_state(move)
            node.children.append(MCTSNode(next_state, parent=node, last_move=move))
            node = node.children[-1]

        # Simulation
        sim_state = node.state.copy()
        while not sim_state.is_terminal():
            random_move = random.choice(list(sim_state.legal_moves()))
            sim_state = sim_state.next_state(random_move)

        # Backpropagation
        value = 1 if sim_state.winner() == state.player else 0
        while node is not None:
            node.visits += 1
            node.value += value
            node = node.parent

    best_child = root.best_child(exploration_weight=0.0)
    best_move = best_child.last_move

    print(f"best move: {best_move}")

    return best_move