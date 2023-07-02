# Trabalho 1 - Grupo 2

## Indentificacao

| Nome                           | Matricula   |
| :----------------------------- | :---------: |
| Brenda Streit Schussler        | 00325353    |
| Felipe Bertoglio               | 00262669    |
| Pedro Afonso Klein             | 00324104    |
| Pedro Henrique Casarotto Rigon | 00325358    |

## Rede neural de uma camada

Foram utilizados valores aleatorios para inicializar ***b*** e ***w***. 

A partir de de 300 epocas ja conseguimos uma aproximacao boa da reta desejada e, juntamente com um *alpha* = 0.1, obtivemos um ***erro quadrático médio*** de aproximadamente **10.8**.

## Tensorflow/Keras

Para todas as redes neurais, foi escolhido o algoritmo de otimizacao RMSProp (Root Mean Square Propagation), pois este converge mais rapido em menos epocas de treinamento ([Keras Optimizers Explained with Examples for Beginners](https://machinelearningknowledge.ai/keras-optimizers-explained-with-examples-for-beginners/)), o que o tornou a escolha ideal uma vez que foi-se limitado a 10 epocas.

### Resultados e Características dos datasets

| Dataset       | Resolucao   | Classes | Amostras | Acuracia | Tempo   |
| :-------------| :---------: | :-----: | :------: | :------: | :-----: |
| MNIST         |   28x28x1   |    10   |   60000  |  0.979   |  98.96  |
| Fashion MNIST |   28x28x1   |    10   |   60000  |  0.853   |  97.15  |
| CIFAR10       |   32x32x3   |    10   |   50000  |  0.658   | 130.59  |
| CIFAR100      |   32x32x3   |    100  |   50000  |  0.345   | 129.25  |

> #### Legenda da tabela
>
> - **Dataset**: Nome do dataset.
> - **Resolucao**: Altura x Largura x Canais de cor das imagens no dataset.
> - **Classes**: Numero de classificacoes diferentes.
> - **Amostras**: Numero de amostras totais no dataset.
> - **Acuracia**: Precisao do resultado em comparacao com os dados de teste do dataset.
> - **Tempo**: Tempo de execucao do treinamento da rede com 10 epocas.

#### Questoes

1) Em quais datasets um perceptron simples (sem convolução e sem camadas ocultas) obtem uma
acurácia acima de 80%?

    > Exemplo de resposta

2) Qual a acurácia máxima obtida no CIFAR-10? Qual modificação teve maior impacto positivo?
Qual o maior desafio/dificuldade?

    > Exemplo de resposta

3) Foi possivel obter mais de 60% de acurácia no CIFAR-100? Qual modificação teve maior
impacto positivo? Qual o maior desafio/dificuldade?

    > Exemplo de resposta

4) Quais fatores (tanto das próprias redes quanto dos dados) levam as redes neurais a melhorarem o
desempenho? E quais fatores tornam o desempenho pior?

    > Exemplo de resposta
