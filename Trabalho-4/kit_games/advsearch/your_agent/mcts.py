import random
from typing import Tuple
from ..othello.gamestate import GameState
from math import sqrt, log
import time

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class Node:
    def __init__(self, state:GameState, parent: 'Node' = None, last_move=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0
        self.last_move = last_move

def selection(node: Node):
    while node.children:
        node = max(node.children, key=lambda child: child.value / child.visits + sqrt(2 * log(node.visits) / child.visits))
    return node

def expansion(node: Node):
    legal_moves = node.state.legal_moves()
    move = random.choice(list(legal_moves))
    next_state = node.state.next_state(move)
    child = Node(next_state, parent=node, last_move=move)  # Assign last_move during expansion
    node.children.append(child)
    return child

def simulation(node: Node):
    state = node.state.copy()
    while not state.is_terminal():
        legal_moves = state.legal_moves()
        move = random.choice(list(legal_moves))
        state = state.next_state(move)
    return 1 if state.winner() == node.state.player else 0

def backpropagation(node: Node, result: int):
    while node:
        node.visits += 1
        node.value += result
        node = node.parent

def monte_carlo_tree_search(root, max_time):
    start_time = time.time()
    iteration = 0
    
    while time.time() - start_time < max_time:
        selected_node = selection(root)
        if not selected_node.state.is_terminal():
            if not selected_node.children:
                expanded_node = expansion(selected_node)
                result = simulation(expanded_node)
            else:
                expanded_node = random.choice(selected_node.children)
                result = simulation(expanded_node)
        else:
            result = 1 if selected_node.state.winner() == selected_node.state.player else 0
        backpropagation(expanded_node, result)
        
        iteration += 1
    
    best_child = max(root.children, key=lambda child: child.visits)
    return best_child.last_move

def make_move(state:GameState) -> Tuple[int, int]:
    """
    Returns a move for the given game state.
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    
    root = Node(state)

    timeout = 4
    return monte_carlo_tree_search(root, timeout)