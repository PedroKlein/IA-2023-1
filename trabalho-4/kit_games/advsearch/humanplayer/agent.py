from typing import Tuple
from advsearch.othello.gamestate import GameState


def make_move(state: 'GameState') -> 'Tuple[int, int]':
    move = input(f"Você é o jogador {state.player}. Escreva sua jogada (<coluna> <linha>): ")
    x = -1
    y = -1

    try:
        x, y = move.split()
        ok = True
    except ValueError:
        ok = False
    x, y = int(x), int(y)
    while not ok or not (x,y) in state.legal_moves():
        move = input("Sua jogada foi ilegal, tente outra vez: ")

        try:
            print(move)
            x, y = move.split()
            x, y = int(x), int(y)
            ok = True
        except ValueError:
            ok = False

    return int(x), int(y)
