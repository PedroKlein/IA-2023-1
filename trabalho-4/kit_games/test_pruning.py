import unittest
from collections import OrderedDict, defaultdict
from typing import Tuple, Union

import advsearch.your_agent.minimax as minimax  # mude your_agent pelo nome do seu modulo

# uma arvore de jogo abstrata que contem o exemplo do  Russel&Norvig's para a poda alfa-beta
# cada nodo eh um dict de acoes e seus nos filhos (cada acao eh uma tupla, conforme os jogos 'reais') 
# nodos de E a M sao terminais
abstract_game_tree = {
    'A': OrderedDict({(0,1): 'B', (0,2): 'C', (0,3): 'D'}),
    'B': OrderedDict({(0,4): 'E', (0,5): 'F', (0,6): 'G'}),
    'C': OrderedDict({(0,7): 'H', (0,8): 'I', (0,9): 'J'}),
    'D': OrderedDict({(0,10): 'K', (0,11): 'L', (0,12): 'M'})
}

# utilidades dos estados terminais na arvore abstrata
utilities = {
    'E': 3, 'F': 12, 'G': 8,
    'H': 2, 'I': 4, 'J': 6,
    'K': 14, 'L': 5, 'M': 2
}

class TestAlphaBetaPruning(unittest.TestCase):
    """
    Este teste checa se sua implementacao da poda alfa-beta 
    retorna a acao correta na arvore de jogo abstrata e poda os nodos corretamente.
    A arvore e' a do slide 37 em: 
    https://docs.google.com/presentation/d/1IPYPito7htL61OKHEWZw402oZQBCjEx9_H3KTEgUna4/edit#slide=id.gbe183847ed_0_95)
    """

    def setUp(self):
        """
        Reseta o contador de chamadas da funcao de utilidade
        e obtem a jogada para o estado inicial
        """
        global calls
        calls = defaultdict(int)

        # obtem a jogada para o estado inicial
        board = Board()
        state = GameState(board, 'B')
        self.move = minimax.minimax_move(state, -1, utility)

    def test_correct_move(self):
        """
        Verifica se a jogada retornada foi a correta
        """

        # verifica se a funcao minimax retornou a melhor jogada
        self.assertEqual(self.move,(0, 1))

    def test_pruning(self):
        """
        Verifica se a funcao poda somente os nodos I e J.
        """
        # nao-terminais nao podem ser avaliados
        for non_terminal in ['A', 'B', 'C', 'D']:
            with self.subTest(f"Non-terminal {non_terminal}"):
                # verifica se a funcao minimax nao chamou a funcao de avaliacao em nenhum estado terminal
                self.assertEqual(calls[non_terminal], 0, 'Erro: a funcao de utilidade nao deve ser chamada nos nao-terminais')

        # nos terminais devem ser avaliados, exceto I e J q sao podados
        for non_pruned in ['E', 'F', 'G', 'H', 'K', 'L', 'M']:
            with self.subTest(f"Non-pruned terminal {non_pruned}"):
                # verifica se a funcao minimax nao chamou a funcao de avaliacao em nenhum estado terminal
                self.assertEqual(calls[non_pruned], 1, 'Erro: a funcao de utilidade deve ser chamada 1 vez para os nos q nao sao podados')

        # I e J devem ser podados
        for pruned in ['I', 'J']:
            with self.subTest(f"Pruned {non_terminal}"):
                # verifica se a funcao minimax nao foi chamada em estado podado
                self.assertEqual(calls[pruned], 0, 'Erro: a funcao de utilidade nao deve ser chamada para os nos q sao podados')
        

# *********************************************
# Voce nao precisa se preocupar com o codigo daqui pra baixo
# O codigo e' para fazer a arvore de jogo abstrata ter
# a mesma interface de um jogo normal e sua implementacao 
# poder ser executada normalmente
# *********************************************

# conta o numero de vezes que a funcao de utilidade e' chamada em cada nodo
calls = defaultdict(int)

def utility(state: 'GameState', player:str) -> float:
    """
    Returns the utility of the given state.
    """
    calls[state.board.board] += 1
    if player == 'B':
        return utilities[state.board.board]
    return -utilities[state.board.board]


class Board:
    """
    A 'fake' board implementation for the abstract game tree
    """
    def __init__(self):
        self.board = 'A'    # defaults to the 'initial' state

    def __str__(self):
        return f'({self.board})'
    
    def decorated_str(self, colors=False, move=None, highlight_flipped=False) -> str:
        return self.board

    def place_marker(self, player, row, col):
        self.board = abstract_game_tree[self.board][(row, col)]

    def is_empty(self, row, col):
        return self.board == ''

    def is_full(self):
        if self.board in utilities.keys():
            return True

    def check_loser(self):
        if self.board in utilities.keys():
            return 'W'
        return None
    
    def copy(self):
        new_board = Board()
        new_board.board = self.board
        return new_board

class GameState:
    """
    A fake game state implementation for the abstract game tree
    """
    game_name = "Russel&Norvig's Example"

    def __init__(self, board: Board, player: str):
        self.board = board
        self.player = player

    def is_terminal(self) -> bool:
        return self.board.is_full() or self.winner() is not None

    def is_legal_move(self, move: Tuple[int, int]) -> bool:
        """
        Checks whether the given move (x, y) is legal in this state.
        """
        row, col = move #e' invertido aqui. nos demais jogos e' col, row -- nao se preocupe com isso
        return move in abstract_game_tree[self.board.board]

    def legal_moves(self) -> set:
        moves = set()
        return abstract_game_tree[self.board.board].keys()

    def winner(self) -> Union[str, None]:
        loser = self.board.check_loser()
        if loser == 'B':
            return 'W'
        elif loser == 'W':
            return 'B'
        else:
            return None

    def get_board(self) -> Board:
        return self.board

    def copy(self) -> 'GameState':
        new_state = GameState(self.board.copy(), self.player)
        return new_state

    def next_state(self, move: Tuple[int, int]) -> 'GameState':
        if not self.is_legal_move(move):
            raise ValueError("Invalid move.")
        
        new_state = self.copy()
        row, col = move #e' invertido aqui. nos demais jogos e' col, row -- nao se preocupe com isso
        new_state.board.place_marker(self.player, row, col)

        # Toggle the player for the next move
        new_state.player = 'B' if self.player == 'W' else 'W'
        return new_state
    



if __name__ == '__main__':
    unittest.main()
