from typing import Iterable, Set, Tuple

#funcao para pegar a posicao do espaco ( _ ) na string 
#posicoes na string: 012345678
def busca_posicao_espaco(string): 
    for i in range(len(string)):
        if string[i] == '_':
            return i 
    return -1 

#acima = -3 na posicao 
#abaixo = +3 na posicao 
#direita = +1 na posicao 
#esquerda = -1 na posicao 

def troca_posicao(string, acao):
    posicao = busca_posicao_espaco(string)
    
    if acao == "direita":
        lista_string = list(string)
        trocado = string[posicao+1]
        lista_string[posicao+1] = '_'
        lista_string[posicao] = trocado
        return ''.join(lista_string)

    if acao == "esquerda":
        lista_string = list(string)
        trocado = string[posicao-1]
        lista_string[posicao-1] = '_'
        lista_string[posicao] = trocado
        return ''.join(lista_string)
    
    if acao == "acima":
        lista_string = list(string)
        trocado = string[posicao-3]
        lista_string[posicao-3] = '_'
        lista_string[posicao] = trocado
        return ''.join(lista_string)
        
    if acao == "abaixo":
        lista_string = list(string)
        trocado = string[posicao+3]
        lista_string[posicao+3] = '_'
        lista_string[posicao] = trocado
        return ''.join(lista_string)
    
class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai:Nodo, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        raise NotImplementedError

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (acao,estado atingido)
    para cada acao possivel no estado recebido.
    Tanto a acao quanto o estado atingido sao strings tambem.
    :param estado:
    :return:
    """
    pos_espaco = busca_posicao_espaco(estado)
    lista_de_tuplas = []
    #se a posicao for 0, 1 ou 2 nao pode ir para cima
    if (pos_espaco!=0 and pos_espaco!=1 and pos_espaco!=2):
        nova_str = troca_posicao(estado, "acima")
        tupla_acima = ("acima", nova_str)
        lista_de_tuplas.append(tupla_acima) 
    #se a posicao for 6, 7 ou 8 nao pode ir para baixo 
    if (pos_espaco!=6 and pos_espaco!=7 and pos_espaco!=8):
        nova_str = troca_posicao(estado, "abaixo")
        tupla_abaixo = ("abaixo", nova_str)
        lista_de_tuplas.append(tupla_abaixo) 
    #se a posicao for 2,5 ou 8 nao pode ir para direita 
    if (pos_espaco!=2 and pos_espaco!=5 and pos_espaco!=8):
        nova_str = troca_posicao(estado, "direita")
        tupla_direita = ("direita", nova_str)
        lista_de_tuplas.append(tupla_direita) 
    #se a posicao for 0,3 ou 6 nao pode ir para esquerda
    if (pos_espaco!=0 and pos_espaco!=3 and pos_espaco!=6):
        nova_str = troca_posicao(estado, "esquerda")
        tupla_esquerda = ("esquerda", nova_str)
        lista_de_tuplas.append(tupla_esquerda) 

    return lista_de_tuplas


def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
