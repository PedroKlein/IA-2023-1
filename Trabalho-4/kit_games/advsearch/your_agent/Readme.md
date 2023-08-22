# Trabalho 4 - Grupo 2 - Turma B

## Identificação

| Nome                           | Matricula   |
| :----------------------------- | :---------: |
| Brenda Streit Schussler        | 00325353    |
| Felipe Bertoglio               | 00262669    |
| Pedro Afonso Klein             | 00324104    |
| Pedro Henrique Casarotto Rigon | 00325358    |

#
Para executar a nossa implementação é necessário importar as bibliotecas: ...

#
## Avaliação da poda alfa-beta no Tic-Tac-Toe Misere:
### i) Minimax vs. RandomPlayer:
* ao executar o comando: _python server.py tttm advsearch/randomplayer/agent.py advsearch/your_agent/tttm_minimax.py_ o minimax sempre ganha o randomplayer. Ao inverter a ordem dos jogadores, isto é, executando o comando: _python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/randomplayer/agent.py_ na grande maioria das partidas o minimax é o vencedor,  no entanto foi perceptível a ocorrência de alguns raros empates.



### ii) Minimax vs. Minimax: 
* ao executar o comando: _python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/your_agent/tttm_minimax.py_, isto é, ao realizar as partidas com o minimax disputando consigo mesmo, o resultado obtido foi sempre empate.


### iii) Minimax vs. "Jogadas Perfeitas": 
* ao executar o comando: _python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/humanplayer/agent.py_ ou _python server.py tttm advsearch/humanplayer/agent.py advsearch/your_agent/tttm_minimax.py_ (para testar as duas possibilidades de qual player inicia o jogo), fazendo partidas do minimax contra o humanplayer, e realizando as jogadas perfeitas recomendadas por: https://nyc.cs.berkeley.edu/uni/games/ttt/variants/misere, os resultados obtidos foram sempre empate. 

#
## Othello: 
### Descrição da função de avaliação customizada: 

Os componentes de avaliação (evaluate_custom, evaluate_move) e a heurística de ordenação de movimentos (heuristic_move_ordering) juntos desempenham um papel fundamental no algoritmo Minimax aplicado ao jogo Othello.

* evaluate_custom: Essa função avalia o estado do jogo a partir da perspectiva de um jogador. Ela calcula a diferença entre o número de peças do jogador e o número de peças do oponente. Se o estado é terminal (fim do jogo), atribui pontuações com base em quem ganhou ou se é um empate. Se o estado não é terminal, retorna a diferença de peças como a pontuação.

* evaluate_move: Esta função simula um movimento em um estado do jogo. Ela calcula a próxima situação do tabuleiro após o movimento, e então chama a função evaluate_custom para avaliar essa nova situação.

* heuristic_move_ordering: Essa função ordena os movimentos possíveis com base nas pontuações calculadas pelas funções de avaliação. Ela cria uma lista de movimentos ordenados por pontuação, em ordem decrescente. Isso permite que o algoritmo Minimax explore primeiro os movimentos mais promissores, potencialmente melhorando a eficiência da busca.

O algoritmo Minimax explora a árvore de possibilidades de movimento, alternando entre os jogadores (minimizando para o oponente e maximizando para o jogador), utilizando as funções de avaliação para atribuir uma pontuação a cada estado e os movimentos possíveis. A heurística de ordenação de movimentos ajuda a direcionar a busca para movimentos mais promissores primeiro, reduzindo o número de estados explorados e melhorando o desempenho geral do algoritmo.

### Descrição do critério de parada (profundidade máxima fixa? aprofundamento iterativo?):  

O critério de parada utilizado no algoritmo descrito é uma profundidade máxima fixa igual a 4.

### Resultado da avaliação (qual a melhor implementação, se MCTS ou minimax com qual heurística...):

|Heurística|Poda Alfa-Beta|RandomPlayer|
|--|----|----|
|**Contagem de Peças**|49|15|
|**Valor Posicional**|38|26|
|**Custom - Ordenação**|35|29|

|MCTS|RandomPlayer|
|----|----|
|35|29|

### Poda Alfa-Beta vs Poda Alfa-Beta

|Heurística|Heurística|valor|valor|
|--|----|----|----|
|**Contagem de Peças**|**Valor Posicional**|37|27|
|**Contagem de Peças**|**Custom - Ordenação**|64|0|
|**Custom - Ordenação**|**Valor Posicional**|37|27|

### Poda Alfa-Beta vs MCTS

|Heurística|MCTS|valor|valor|
|--|----|----|----|
|**Contagem de Peças**|**MCTS**|37|27|
|**Valor Posicional**|**MCTS**|64|0|
|**Custom - Ordenação**|**MCTS**|37|27|



### Implementação escolhida para o torneio e se houve implementação de alguma melhoria no minimax ou no MCTS: 

#
## Feedback: 
quão fácil ou difícil foi realizar o trabalho? como foi trabalhar com o auxílio
da IA? quais sugestões teria para melhorar o trabalho? 

