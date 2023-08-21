from typing import Tuple, Callable
from ..tttm.gamestate import GameState


def minimax_move(
    state: GameState, max_depth: int, eval_func: Callable
) -> Tuple[int, int]:
    def minimax(node, depth, maximizing_player, alpha, beta):
        if depth == 0 or node.is_terminal():
            return eval_func(node, state.player)

        if maximizing_player:
            max_eval = float("-inf")
            for move in node.legal_moves():
                child = node.next_state(move)
                eval = minimax(child, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in node.legal_moves():
                child = node.next_state(move)
                eval = minimax(child, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    best_move = None
    best_eval = float("-inf")

    for move in state.legal_moves():
        child = state.next_state(move)
        eval = minimax(child, max_depth, False, float("-inf"), float("inf"))
        if eval > best_eval:
            best_eval = eval
            best_move = move

    return best_move
