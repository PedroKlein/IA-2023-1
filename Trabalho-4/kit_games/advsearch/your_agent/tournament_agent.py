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

def heuristic_move_ordering(game_state: GameState, color: str) -> list:
    legal_moves = game_state.legal_moves()

    # Create a list of tuples: (move, score)
    ordered_moves = []
    for move in legal_moves:
        score = evaluate_move(game_state, move, color)
        ordered_moves.append((move, score))

    # Sort the list based on the scores (higher score first)
    ordered_moves.sort(key=lambda x: x[1], reverse=True)

    # Extract and return the sorted moves
    sorted_moves = [move for move, _ in ordered_moves]
    return sorted_moves

def evaluate_move(game_state: GameState, move: Tuple[int, int], color: str) -> float:
    """
    Evaluates the desirability of a move in the given game state for the given player color.
    :param game_state: the current game state
    :param move: the move to evaluate
    :param color: the player's color (B or W)
    :return: a float representing the desirability of the move (higher is better)
    """
    # Make a copy of the game state and simulate the move
    next_state = game_state.next_state(move)
    
    # Perform the evaluation based on custom criteria
    return evaluate_custom(next_state, color)

def evaluate_custom(state: GameState, player: str) -> float:
    """
    Evaluates an Othello state from the point of view of the given player.
    If the state is terminal, returns its utility.
    If non-terminal, returns an estimate of its value based on the difference in the number of pieces.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    :return: a float representing the estimated value of the state (higher is better for the player)
    """
    player_pieces = state.get_board().num_pieces(player)
    opponent_pieces = state.get_board().num_pieces(Board.opponent(player))

    if state.is_terminal():
        if player_pieces > opponent_pieces:
            return 1.0  # Player wins
        elif player_pieces < opponent_pieces:
            return -1.0  # Player loses
        else:
            return 0.0  # It's a draw
    else:
        return player_pieces - opponent_pieces  # Simple difference in piece count
