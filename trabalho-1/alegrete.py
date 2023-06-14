import numpy as np

def compute_hypothesis(b, w, x):
    """
    Calcula a altura da reta para um dado valor de x.
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param x: float - valor de x
    :return: float - altura da reta para o dado valor de x
    """
    return b + w * x


def compute_mse(b, w, data):
    """
    Calcula o erro quadratico medio
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """
    N = data.shape[0]
    squared_error = 0
    
    for (area, price) in data:
        squared_error += pow(compute_hypothesis(b, w, area) - price, 2)

    return squared_error / N


def step_gradient(b, w, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de b e w.
    :param b: float - bias (intercepto da reta)
    :param w: float - peso (inclinacao da reta)
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de b e w, respectivamente
    """
    b_gradient = 0
    w_gradient = 0
    N = data.shape[0]

    for (area, price) in data:
        b_gradient += (2 / N) * (compute_hypothesis(b, w, area) - price)
        w_gradient += (2 / N) * (compute_hypothesis(b, w, area) - price) * area

    new_b = b - alpha * b_gradient
    new_w = w - alpha * w_gradient

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
    b_list = []
    w_list = []

    min_val = np.min(data, axis=0)
    max_val = np.max(data, axis=0)
    normalized_dataset = (data - min_val) / (max_val - min_val)


    for i in range(num_iterations):
        b, w = step_gradient(b, w, normalized_dataset, alpha)
        b_list.append(b)
        w_list.append(w)

    return b_list, w_list
