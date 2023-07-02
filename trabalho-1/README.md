# Trabalho 1 - Grupo 2

## Instalação

O ambiente do miniconda esta descrito no arquivo ```environment.yml``` e pode ser instalado atraves do seguinte comando:

```bash
conda env create -f environment.yml 
```
## Indentificação

| Nome                           | Matricula   |
| :----------------------------- | :---------: |
| Brenda Streit Schussler        | 00325353    |
| Felipe Bertoglio               | 00262669    |
| Pedro Afonso Klein             | 00324104    |
| Pedro Henrique Casarotto Rigon | 00325358    |

## Rede neural de uma camada

Foram utilizados valores aleatorios para inicializar ***b*** e ***w***. 

A partir de de 300 epocas ja conseguimos uma aproximacao boa da reta desejada e, juntamente com um *alpha* = 0.1, obtivemos um ***erro quadrático médio*** de aproximadamente **10.8**. Foi necessário realizar a normalização dos dados para garanitir uma regressão correta para valores de *alpha* mais altos. 

## Tensorflow/Keras

Para todas as redes neurais, foi escolhido o algoritmo de otimização RMSProp (Root Mean Square Propagation), pois este converge mais rápido em menos epocas de treinamento ([Keras Optimizers Explained with Examples for Beginners](https://machinelearningknowledge.ai/keras-optimizers-explained-with-examples-for-beginners/)), o que o tornou a escolha ideal uma vez que foi-se limitado a 10 epocas.

### Resultados e Características dos datasets

| Dataset       | Resolução   | Classes | Amostras | Acuracia | Tempo   |
| :-------------| :---------: | :-----: | :------: | :------: | :-----: |
| MNIST         |   28x28x1   |    10   |   60000  |  0.984   |  91.14  |
| Fashion MNIST |   28x28x1   |    10   |   60000  |  0.852   |  91.32  |
| CIFAR10       |   32x32x3   |    10   |   50000  |  0.684   | 100.17  |
| CIFAR100      |   32x32x3   |    100  |   50000  |  0.333   | 113.32  |

> #### Legenda da tabela
>
> - **Dataset**: Nome do dataset.
> - **Resolução**: Altura x Largura x Canais de cor das imagens no dataset.
> - **Classes**: Numero de classificacoes diferentes.
> - **Amostras**: Numero de amostras totais no dataset.
> - **Acuracia**: Precisão do resultado em comparacao com os dados de teste do dataset.
> - **Tempo**: Tempo de execucao em segundos do treinamento da rede com 10 epocas.

#### Questões

1) Em quais datasets um perceptron simples (sem convolução e sem camadas ocultas) obtem uma
acurácia acima de 80%?

    > **Foi obtido acurácia acima de 80% desta maneira apenas com o dataset MNIST, pois é o mais simples dentre os quatro datasets.**

2) Qual a acurácia máxima obtida no CIFAR-10? Qual modificação teve maior impacto positivo?
Qual o maior desafio/dificuldade?

    > **A acurácia maxima foi de aproximadamente 68%. A modificação mais significativa foi a utilização de duas camadas de convolução separadas por uma camada de MaxPool. Tentou-se elaborar redes mais coplexas, porem o aumento da complexidade sempre gerava *overfitting*.**

3) Foi possivel obter mais de 60% de acurácia no CIFAR-100? Qual modificação teve maior
impacto positivo? Qual o maior desafio/dificuldade?

    > **Atingiu-se uma acurácia de aproximadamente 33% e, assim como no dataset CIFAR-10, a modificação mais significativa foir com relação ao aumento da camada de convolução, separando-as por uma camada de MaxPool. Infelizmente não foi possivel obter uma acurácia acima de 60% em função da complexidade do dataset, pois redes mais complexas geravam *overfitting*. Para resolver este problema tentou-se utilizar camadas de [Dropout](https://www.tensorflow.org/tutorials/keras/overfit_and_underfit#add_dropout), porem sem sucesso.**

4) Quais fatores (tanto das próprias redes quanto dos dados) levam as redes neurais a melhorarem o desempenho? E quais fatores tornam o desempenho pior?

    > **Nos dois primeiros datasets (MNIST e Fashion MNIST) o fato de serem imagens sem canais de cor, tornou o treinamento muito mais facil, uma vez que os filtros podem passar a detectar apenas formas. Ja os dois ultimos datasets (CIFAR-10 e CIFAR-100) adicionam a complexidade de 3 canais de cores, tornando não mais trivial o treinamento dos filtros implementados. Nestes dois datasets também foi necessário normalizar os dados em função dos canais de cores.**
