import unittest

# mude your_agent pelo nome do seu modulo nos imports abaixo
from advsearch.your_agent.othello_minimax_count import evaluate_count 
from advsearch.your_agent.othello_minimax_mask import evaluate_mask  
from advsearch.othello.board import Board
from advsearch.othello.gamestate import GameState

class TestEvaluateCount(unittest.TestCase):
    """
    Testa a funcao de avaliacao de contagem
    """
    def test_evaluate_count(self):
        """
        Testa a funcao de avaliacao de contagem
        """

        # Test case 1: Player 'B' has 2 pieces, and Player 'W' has 2 pieces.
        state1 = Board.from_string("""........
........
........
...WB...
...BW...
........
........
........""")
        game_state1 = GameState(state1, 'B')
        expected_score1_B = 0  # 2 pieces (B) - 2 pieces (W)
        expected_score1_W = 0  # 2 pieces (W) - 2 pieces (B)

        # Test evaluation for Player 'B' in state1
        score1_B = evaluate_count(game_state1, 'B')
        self.assertEqual(score1_B, expected_score1_B, "Caso de teste 1B: Pontuação incorreta para o estado inicial (Jogador B).")

        # Testar avaliação para o Jogador 'W' no state1
        score1_W = evaluate_count(game_state1, 'W')
        self.assertEqual(score1_W, expected_score1_W, "Caso de teste 1W: Pontuação incorreta para o estado inicial (Jogador W).")

        # Test case 2: Player 'B' has 3 pieces, and Player 'W' has 3 piece.
        state2 = Board.from_string("""........
........
.....B..
...WBW..
...BW...
........
........
........""")
        game_state2 = GameState(state2, 'B')
        expected_score2_B = 0  # 2 pieces (B) - 1 piece (W)
        expected_score2_W = 0  # 1 piece (W) - 2 pieces (B)

        # Test evaluation for Player 'B' in state2
        score2_B = evaluate_count(game_state2, 'B')
        self.assertEqual(score2_B, expected_score2_B, "Caso de teste 2B: Pontuação incorreta para estado não vazio (Jogador B).")

        # Test evaluation for Player 'W' in state2
        score2_W = evaluate_count(game_state2, 'W')
        self.assertEqual(score2_W, expected_score2_W, "Caso de teste 2W: Pontuação incorreta para estado não vazio (Jogador W).")

        # Test case 3: Player 'B' has 33 pieces, and Player 'W' has 31 pieces.
        state3 = Board.from_string('BBBBBBB.\n'
                                   'BBWWWWBB\n'
                                   'BWBWWBBB\n'
                                   'BWWWBBBB\n'
                                   'BWBBBBBB\n'
                                   'BWBWBBBB\n'
                                   'BBWWBBBB\n'
                                   'BBBWBBBB\n')
        game_state3 = GameState(state3, 'B')
        expected_score3_B = 31  #  47 pieces (B) - 16 pieces (W)
        expected_score3_W = -31  # 16 pieces (W) - 47 pieces (B)  
        score3_B = evaluate_count(game_state3, 'B')
        self.assertEqual(score3_B, expected_score3_B, "Caso de teste 3B: Pontuação incorreta para estado complexo (Jogador B).")

        # Test evaluation for Player 'W' in state3
        score3_W = evaluate_count(game_state3, 'W')
        self.assertEqual(score3_W, expected_score3_W, "Caso de teste 3W: Pontuação incorreta para estado complexo (Jogador W).")

        # Test case 4: Player 'B' has 11 pieces, and Player 'W' has 19 pieces.
        state4 = Board.from_string("""WWWWWWWW
WWWWWBBW
WWWWBWBW
WBWBWBBW
WBWWBWBW
WBBWBWBW
WBBBWBWW
WWWWWWW.""")
        game_state4 = GameState(state4, 'B')
        expected_score4_B = -25  # 19 pieces (B) - 44 pieces (W)
        expected_score4_W = 25  # 44 pieces (W) - 19 pieces (B)

        # Test evaluation for Player 'B' in state4
        score4_B = evaluate_count(game_state4, 'B')
        self.assertEqual(score4_B, expected_score4_B, "Caso de teste 4B: Pontuação incorreta para estado complexo (Jogador B).")

        # Testar avaliação para o Jogador 'W' no state4
        score4_W = evaluate_count(game_state4, 'W')
        self.assertEqual(score4_W, expected_score4_W, "Caso de teste 4W: Pontuação incorreta para estado complexo (Jogador W).")

class TestEvaluateMask(unittest.TestCase):
    """
    Testa a funcao de avaliacao posicional
    """
    def test_evaluate_mask(self):
        """
        Testa a funcao de avaliacao posicional (q aplica a mascara de valores)
        """

        # Test case 1: Player 'B' has 2 pieces, and Player 'W' has 2 pieces.
        state1 = GameState(Board.from_string("""\
........
........
........
...WB...
...BW...
........
........
........"""), 'B')
        expected_score1_B = 0 
        expected_score1_W = 0 
        # Test evaluation for Player 'B' in state1
        score1_B = evaluate_mask(state1, 'B')
        self.assertEqual(score1_B, expected_score1_B, "Caso de teste 1B: Pontuação incorreta para o estado inicial (Jogador B).")

        # Testar avaliação para o Jogador 'W' no state1
        score1_W = evaluate_mask(state1, 'W')
        self.assertEqual(score1_W, expected_score1_W, "Caso de teste 1W: Pontuação incorreta para o estado inicial (Jogador W).")

        # test case 2: surprisingly, it's a winning situation for B but it is evaluated negatively
        state2 = GameState(Board.from_string('''\
BBBBBBB.
BBWWWWBB
BWBWWBBB
BWWWBBBB
BWBBBBBB
BWBWBBBB
BBWWBBBB
BBBWBBBB
'''), 'B')
        expected_score_B = -74 
        expected_score_W = 74
        # Test evaluation for Player 'B' in state
        score_B = evaluate_mask(state2, 'B')
        self.assertEqual(score_B, expected_score_B, "Caso de teste 2B: Pontuação incorreta para o estado (Jogador B).")

        # Testar avaliação para o Jogador 'W' no state
        score_W = evaluate_mask(state2, 'W')
        self.assertEqual(score_W, expected_score_W, "Caso de teste 2W: Pontuação incorreta para o estado (Jogador W).")


        # test case 3: it's a winning situation for W
        state3 = GameState(Board.from_string("""\
WWWWWWWW
WWWWWBBW
WWWWBWBW
WBWBWBBW
WBWWBWBW
WBBWBWBW
WBBBWBWW
WWWWWWW."""), 'B')
        
        expected_score_B = -122 
        expected_score_W = 122
        # Test evaluation for Player 'B' in state
        score_B = evaluate_mask(state3, 'B')
        self.assertEqual(score_B, expected_score_B, "Caso de teste 3B: Pontuação incorreta para o estado (Jogador B).")

        # Testar avaliação para o Jogador 'W' no state
        score_W = evaluate_mask(state3, 'W')
        self.assertEqual(score_W, expected_score_W, "Caso de teste 3W: Pontuação incorreta para o estado (Jogador W).")




if __name__ == '__main__':
    unittest.main()