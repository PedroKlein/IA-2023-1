import unittest
from collections import OrderedDict, defaultdict
from typing import Tuple, Union

import advsearch.your_agent.mcts as mcts  # mude your_agent pelo nome do seu modulo


# jogo muito simples. o estado inicial tem 3 sucessores, 
# em B o jogador (B) vence, em D ha' empate e em W o adversario (W) vence
# ha' um dict pra contar quantas vezes cada estado foi visitado (nao usado ainda)
very_simple_game_tree = {
    'A': OrderedDict({(0,1): 'B', (0,2): 'D', (0,3): 'W'}),
}
very_simple_game_terminals = {
    'B', 'D', 'W'
}
very_simple_game_visits = defaultdict(int)

class TestMCTSVerySimpleGame(unittest.TestCase):
    """
    Este teste checa se sua implementacao do MCTS retorna a acao correta em 
    dois jogos simples
    """

    def setUp(self):
        """
        Reseta o contador de chamadas da funcao de utilidade
        """
        global very_simple_game_visits
        very_simple_game_visits = defaultdict(int)      # reseta o contador de visitas

        
        
    def test_correct_move_very_simple_game(self):
        """
        Verifica se a jogada retornada para o jogo muito simples foi a correta
        """
        # obtem a jogada para o estado inicial
        board = Board()
        state = GameState(board, 'B')
        self.move = mcts.make_move(state)
        # checa se a jogada e' a que leva para o estado de vitoria
        self.assertEqual(self.move,(0, 1))



# *********************************************
# Voce nao precisa se preocupar com o codigo daqui pra baixo
# O codigo e' para fazer a arvore de jogo abstrata ter
# a mesma interface de um jogo normal e sua implementacao 
# poder ser executada normalmente
# *********************************************



class Board:
    """
    A 'fake' board implementation for the abstract game tree
    """
    def __init__(self, game_tree=very_simple_game_tree, utilities=very_simple_game_terminals):
        self.board = 'A'    # defaults to the 'initial' state
        self.game_tree = game_tree
        self.terminals = utilities

    def __str__(self):
        return f'({self.board})'
    
    def decorated_str(self, colors=False, move=None, highlight_flipped=False) -> str:
        return self.board

    def place_marker(self, player, row, col):
        self.board = self.game_tree[self.board][(row, col)]

    def is_empty(self, row, col):
        return self.board == ''

    def is_full(self):
        """
        Equivalent of 'is endgame' for the abstract game tree
        """
        return self.board in self.terminals

    def check_loser(self):
        if self.board == 'B': return 'W'
        elif self.board == 'W': return 'B'
        return None
    
    def copy(self):
        new_board = Board(self.game_tree, self.terminals)
        new_board.board = self.board
        return new_board

class GameState:
    """
    A fake game state implementation for the abstract game tree
    """
    game_name = "Abstract Game"

    def __init__(self, board: Board, player: str, game_tree=very_simple_game_tree, terminals=very_simple_game_terminals, visit_count=very_simple_game_visits):
        self.board = board
        self.player = player
        self.game_tree = game_tree
        self.terminals = terminals
        self.visit_count = visit_count

    def is_terminal(self) -> bool:
        return self.board.board in self.terminals
    
    def is_legal_move(self, move: Tuple[int, int]) -> bool:
        """
        Checks whether the given move (x, y) is legal in this state.
        """
        row, col = move #e' invertido aqui. nos demais jogos e' col, row -- nao se preocupe com isso
        return move in self.game_tree[self.board.board]

    def legal_moves(self) -> set:
        moves = set()
        return self.game_tree[self.board.board].keys()

    def winner(self) -> Union[str, None]:
        loser = self.board.check_loser()
        if loser == 'B': return 'W'
        elif loser == 'W': return 'B'
        else: return None

    def get_board(self) -> Board:
        return self.board

    def copy(self) -> 'GameState':
        new_state = GameState(self.board.copy(), self.player, self.game_tree, self.terminals, self.visit_count)
        return new_state

    def next_state(self, move: Tuple[int, int]) -> 'GameState':
        if not self.is_legal_move(move):
            raise ValueError("Invalid move.")
        
        new_state = self.copy()
        row, col = move #e' invertido aqui. nos demais jogos e' col, row -- nao se preocupe com isso
        new_state.board.place_marker(self.player, row, col)

        # Toggle the player for the next move
        new_state.player = 'B' if self.player == 'W' else 'W'
        self.visit_count[new_state.board.board] += 1
        return new_state
    



if __name__ == '__main__':
    unittest.main()
