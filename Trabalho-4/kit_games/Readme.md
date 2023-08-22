# Trabalho 4 - Grupo 2 - Turma B

## Indentificação

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

### Descrição do critério de parada (profundidade máxima fixa? aprofundamento iterativo?): 

### Resultado da avaliação (qual a melhor implementação, se MCTS ou minimax com qual heurística...):

### Implementação escolhida para o torneio e se houve implementação de alguma melhoria no minimax ou no MCTS: 

#
## Feedback: 
quão fácil ou difícil foi realizar o trabalho? como foi trabalhar com o auxílio
da IA? quais sugestões teria para melhorar o trabalho? 


