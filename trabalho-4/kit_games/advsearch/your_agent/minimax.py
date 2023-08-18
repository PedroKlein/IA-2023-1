from typing import Tuple, Callable

def minimax_move(state, max_depth: int, eval_func: Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    def max_value(state, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return eval_func(state, state.player)

        v = float("-inf")
        for move in state.legal_moves():
            new_state = state.next_state(move)
            if new_state is not None:  # Check if the new state is valid
                v = max(v, min_value(new_state, alpha, beta, depth - 1))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if state.is_terminal() or depth == 0:
            return eval_func(state, state.player)

        v = float("inf")
        for move in state.legal_moves():
            new_state = state.next_state(move)
            if new_state is not None:  # Check if the new state is valid
                v = min(v, max_value(new_state, alpha, beta, depth - 1))
                if v <= alpha:
                    return v
                beta = min(beta, v)
        return v

    best_move = None
    alpha = float("-inf")
    beta = float("inf")

    for move in state.legal_moves():
        new_state = state.next_state(move)
        if new_state is not None:  # Check if the new state is valid
            v = min_value(new_state, alpha, beta, max_depth - 1)
            if v > alpha:
                alpha = v
                best_move = move

    return best_move
