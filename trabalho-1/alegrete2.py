import numpy as np
import pandas as pd


#leitura do arquivo com os dados
#dados = np.genfromtxt('/home/brendaschussler/Área de Trabalho/trab1IA/kit_neural_net/alegrete.csv', delimiter=',')

def compute_mse(b, w, data):
    """
    Calcula o erro quadratico medio
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """

    numLinhas = (data.shape[0]) #shape[0] pois quero pegar num de linhas

    #x lidos do csv -> é a primeira coluna 
    #y lidos do csv -> segunda coluna = previsão real 
    #f(x) = func -> predição 
    soma_erros_quad = 0

    for area, preco in data:
        #f(x) = b + w*x
        func = b + w*area 
        soma_erros_quad += ((func - preco)**2)

    erro_quad_medio = soma_erros_quad / numLinhas

    return erro_quad_medio


def step_gradient(b, w, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de b e w.
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de b e w, respectivamente
    """
    numLinhas = (data.shape[0]) #shape[0] pois quero pegar num de linhas
    grad_b = 0
    grad_w = 0 

    for area, preco in data:
        #f(x) = b + w*x
        func = b + w*area 
        #calculo das derivadas parciais
        grad_b += (2/numLinhas) * (func - preco)
        grad_w += (2/numLinhas) * (func - preco) * area

    #Atualiza b e w
    new_b = b - (alpha*grad_b)
    new_w = w - (alpha*grad_w)

    return new_b, new_w

def fit(data, b, w, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de b e w.
    Ao final, retorna duas listas, uma com os b e outra com os w
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os b e outra com os w obtidos ao longo da execução
    """
    lista_b = []
    lista_w = []

    for epoch in range(num_iterations):
        b, w = step_gradient(b, w, data, alpha)
        lista_b.append(b)
        lista_w.append(w)
    
    return lista_b, lista_w


#epocas = 50000
#bests = fit(dados, 0.1, 0.1, 0.01, epocas)
#best_b = bests[0][epocas-1]
#best_w = bests[1][epocas-1]
#print(best_b, best_w)
#print(compute_mse(best_b, best_w, dados))
