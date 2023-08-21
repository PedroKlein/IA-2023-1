import random
from typing import Tuple
from collections import defaultdict

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def select(self):
        best_value = float('-inf')
        best_nodes = []

        for child in self.children:
            ucb = 0 if child.visits == 0 else child.wins / child.visits + (2 * (self.visits ** 0.5) / child.visits)
            if ucb == best_value:
                best_nodes.append(child)
            if ucb > best_value:
                best_value = ucb
                best_nodes = [child]

        return random.choice(best_nodes)

    def expand(self):
        legal_moves = self.state.legal_moves()
        for move in legal_moves:
            if move not in [child.state.board.board for child in self.children]:
                self.children.append(Node(self.state.next_state(move), self))

    def simulate(self):
        current_state = self.state.copy()
        while not current_state.is_terminal():
            current_state = current_state.next_state(random.choice(list(current_state.legal_moves())))
        return current_state.winner()

    def backpropagate(self, result):
        self.visits += 1
        if result == self.state.player:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)


def mcts(state, num_simulations=1000):
    root = Node(state)

    for _ in range(num_simulations):
        node = root
        # Selection
        while node.children:
            node = node.select()

        # Expansion
        if not node.state.is_terminal():
            node.expand()

        # Simulation
        outcome = node.simulate()

        # Backpropagation
        node.backpropagate(outcome)

    # Choose the child with the highest number of visits as the next move
    return max(root.children, key=lambda c: c.visits).state.board.board


def make_move(state) -> Tuple[int, int]:
    action = mcts(state)
    for move, st in state.game_tree[state.board.board].items():
        if st == action:
            return move

    return (-1, -1)  # Default move if nothing is found.
