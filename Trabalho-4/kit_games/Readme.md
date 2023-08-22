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

|Heurística|Poda Alfa-Beta|RandomPlayer|
|--|----|----|
|**Contagem de Peças**|20|20|
|**Valor Posicional**|10|10|
|**Custom - Ordenação**|10|10|
|**e_vitoria**|100|100|
|**mobilidade**|10|20|
|**cantos_capturados**|20|30|
|**estabilidade**|40|40|


### ii) Minimax vs. Minimax: 
* ao executar o comando: _python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/your_agent/tttm_minimax.py_, isto é, ao realizar as partidas com o minimax disputando consigo mesmo, o resultado obtido foi sempre empate.

|Heurística|Poda Alfa-Beta|RandomPlayer|
|--|----|----|
|**Contagem de Peças**|20|20|
|**Valor Posicional**|10|10|
|**Custom - Ordenação**|10|10|
|**e_vitoria**|100|100|
|**mobilidade**|10|20|
|**cantos_capturados**|20|30|
|**estabilidade**|40|40|

### iii) Minimax vs. "Jogadas Perfeitas": 
* ao executar o comando: _python server.py tttm advsearch/your_agent/tttm_minimax.py advsearch/humanplayer/agent.py_ ou _python server.py tttm advsearch/humanplayer/agent.py advsearch/your_agent/tttm_minimax.py_ (para testar as duas possibilidades de qual player inicia o jogo), fazendo partidas do minimax contra o humanplayer, e realizando as jogadas perfeitas recomendadas por: https://nyc.cs.berkeley.edu/uni/games/ttt/variants/misere, os resultados obtidos foram sempre empate. 

|Heurística|Poda Alfa-Beta|RandomPlayer|
|--|----|----|
|**Contagem de Peças**|20|20|
|**Valor Posicional**|10|10|
|**Custom - Ordenação**|10|10|
|**e_vitoria**|100|100|
|**mobilidade**|10|20|
|**cantos_capturados**|20|30|
|**estabilidade**|40|40|

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

O melhor desempenho encontrado foi no minmax count. Dentre os melhores desempenhos, encontramos o minmax_count e minmax_custom, em ambos os casos o primeiro jogador tem uma ampla vantagem. Entretanto, notamos que o minmax_count tem um desempenho mais consistente e nos casos em que perde (quando é o player 2), tem uma diferença menor em relação ao vencedor.  

 minimax_count (39) x (25) mcts  
 mcts (30) x (34) minimax_count  
 
 minimax_count (64) x (0) minimax_custom  
 minimax_custom (55) x (9) minimax_count  

 mcts (31) x (33) minimax_custom  
 minimax_custom (51) x (13) mcts  

 minimax_count (39) x (25) random  
 random (18) x (46) minimax_count       

### Implementação escolhida para o torneio e se houve implementação de alguma melhoria no minimax ou no MCTS: 

Com base nos resultados encontrados anteriormente, escolhemos submeter ao torneio o minimax com heuristica de contagem. 

Foi adotada uma política de timeout na implementação do loop do MCTS. Dessa forma, buscamos garantir que a busca respeita o timeout definido pelo professor e não correr risco de ultrapassar o tempo em um loop de tamanho fixo.

#
## Feedback: 
quão fácil ou difícil foi realizar o trabalho? como foi trabalhar com o auxílio
da IA? quais sugestões teria para melhorar o trabalho? 


