import unittest
from typing import Callable, Tuple

from advsearch.tttm.board import Board
from advsearch.tttm.gamestate import GameState
import advsearch.timer as timer

# mude your_agent pelo nome do seu modulo nos imports abaixo
import advsearch.your_agent.minimax as minimax          
import advsearch.your_agent.tttm_minimax as tttm_agent  

def mirror_move(state: GameState) -> Tuple[int, int]:
    """
    Retorna a jogada simetrica 'a jogada anterior do oponente.
    Retorna a jogada de centro para o primeiro movimento.
    Jogar assim garante o empate, mas apenas para o primeiro jogador.
    (nao usada por enquanto pq ela nao exploita erros do adversario)
    """
    mirror = {0: 2, 1: 1, 2: 0}     # maps a position to its mirror position

    opponent = 'B' if state.player == 'W' else 'W'
    if state.board.is_empty():
        return 1, 1
    else:
        for x, y in state.legal_moves():
            if state.board.board[mirror[x]][mirror[y]] == opponent:
                return (x,y)


class TestAlphaBetaTTTM(unittest.TestCase):

    def run_with_timeout(self, timeout: int, function: Callable, args: tuple) -> Tuple:
        """
        Funcao auxiliar que executa uma funcao com um timeout especificado. Se o tempo se esgotar,
        o teste que a chamou falha com 'timeout'
        :param timeout: timeout em segundos
        :param function: funcao a executar
        :param args: argumentos da funcao
        :return: resultado da funcao ou faz o teste falhar se houver timeout
        """
        time_check = timer.FunctionTimer(function, args)  
        try:
            move = time_check.run(timeout)
            return move     
        except TimeoutError:
            self.fail("timeout")


    def test_utility(self):
        """
        Esse teste verifica a funcao utility em advsearch.your_agent.tttm_minimax
        """

        # estado terminal com vitoria das brancas
        board_str = """
W.B
WB.
BW.
"""
        board = Board.from_string(board_str)
        state = GameState(board, 'W')
        # a avaliacao deve ser positiva para as brancas que vencem e negativa para as pretas que perdem
        self.assertGreater(tttm_agent.utility(state, 'W'), 0)
        self.assertLess(tttm_agent.utility(state, 'B'), 0)

    def test_correct_move_initial_state_(self):
        """
        Esse teste verifica se o agente consegue retornar a jogada correta pro estado inicial.
        Deve ser no centro, caso contrario o jogo sera' perdido se o oponente jogar com perfeicao.
        :return:
        """
        #global board, state
        board = Board()
        state = GameState(board, 'B')

        # configura a funcao minimax pra receber o estado, profundidade ilimitada e a funcao de utilidade definida no agente
        move = self.run_with_timeout(60, minimax.minimax_move, (state, -1, tttm_agent.utility) )

        # checa se a primeira jogada e' no centro
        self.assertEquals(move, (1, 1), "Erro: a primeira jogada deve ser no centro, senao o jogo sera' perdido")

    def test_proven_win_exploiting_first_blunder(self):
        """
        Verifica se o agente consegue vencer uma partida quando a primeira jogada nao e' otima
        :return:
        """
        board_str = """
..B
...
...
"""
        board = Board.from_string(board_str)
        state = GameState(board, 'W')

        # a jogada vencedora nao pode ser no centro nem nas diagonais, restando as pontas da 'cruz'
        winning_moves = {(0,1), (1,0), (0,2), (2,1)}

        # configura a funcao minimax pra receber o estado, profundidade ilimitada e a funcao de utilidade definida no agente
        move = self.run_with_timeout(60, minimax, (state, -1, tttm_agent.utility) )  
        self.assertIn(move, winning_moves, "Erro: a jogada vencedora apos erro na primeira jogada nao foi encontrada")


    def test_perfect_play(self):
        """
        Verifica se a implementacao joga o jogo com perfeicao (i.e. nao retorna uma jogada sub-otima)
        """
        board = Board()
        state = GameState(board, 'W')

        # cria uma funcao 'auxiliar' que recebe o estado e executa o make_move com os demais parametros pre-definidos
        agent_timeout_call = lambda state: self.run_with_timeout(60, tttm_agent.make_move, (state,))

        # primeira jogada deve ser no centro
        move = agent_timeout_call(state.copy())
        self.assertEqual(move, (0,0), "Erro: a primeira jogada deve ser no centro.")

        #aplica a jogada retornada 
        state = state.next_state(move)

        # efetua jogada (perfeita) no canto superior direito
        state = state.next_state((2, 0))

        # a resposta deve ser jogada no canto inferior esquerdo
        move = agent_timeout_call(state.copy())
        self.assertEqual(move, (0,2), "Erro: a resposta a (2,0) deve ser (0,2).")

        #aplica a jogada retornada 
        state = state.next_state(move)

        # efetua jogada (perfeita) no meio à esquerda
        state = state.next_state((0, 1))

        # a resposta deve ser jogada no meio à direita
        move = agent_timeout_call(state.copy())
        self.assertEqual(move, (2, 1), "Erro: a resposta a (0,1) deve ser (2,1).")

        #aplica a jogada retornada 
        state = state.next_state(move)

        # efetua jogada (perfeita) acima no meio
        state = state.next_state((1, 0))

        # a resposta deve ser jogada no embaixo no meio
        move = agent_timeout_call(state.copy())
        self.assertEqual(move, (1,2), "Erro: a resposta a (1,0) deve ser (1,2).")

        #aplica a jogada retornada 
        state = state.next_state(move)

        # efetua jogada (perfeita) no canto inferior direito
        state = state.next_state((2, 2))

        # a resposta deve ser jogada no canto superior esquerdo
        move = agent_timeout_call(state.copy())
        self.assertEqual(move, (0,0), "Erro: a resposta a (2,2) deve ser (0,0).")

if __name__ == '__main__':
    unittest.main()
