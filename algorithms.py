from collections import deque


def bfs(adj_list, start):
    """Executa BFS e retorna ordem de visita."""
    visitados = set()
    fila = deque([start])
    ordem = []

    while fila:
        no = fila.popleft()
        if no not in visitados:
            visitados.add(no)
            ordem.append(no)
            for vizinho in adj_list[no]:
                if vizinho not in visitados:
                    fila.append(vizinho)
    return ordem


def bfs_mat_adj(adj_m, nodes, start):
    """Executa BFS em matriz de adjacência e retorna ordem de visita."""
    visitados = set()
    fila = deque([start])
    ordem = []

    # mapa de nó para índice da coluna
    index = {node: i for i, node in enumerate(nodes)}

    while fila:
        no = fila.popleft()
        if no not in visitados:
            visitados.add(no)
            ordem.append(no)
            i = index[no]
            for j, conectado in enumerate(adj_m[i]):
                if conectado == 1:
                    vizinho = nodes[j]
                    if vizinho not in visitados:
                        fila.append(vizinho)
    return ordem


def dfs(adj_list, start):
    """Executa DFS recursiva e retorna ordem de visita."""
    visitados = set()
    ordem = []

    def _dfs(no):
        if no in visitados:
            return
        visitados.add(no)
        ordem.append(no)
        for vizinho in adj_list[no]:
            if vizinho not in visitados:
                _dfs(vizinho)

    _dfs(start)
    return ordem


def dfs_forest(adj_list):
    """
    Executa DFS em todo o grafo (floresta DFS) e retorna:
    - ordem de visita
    - tempos de início e fim de cada nó
    """
    visitados = set()
    ordem = []
    tempos = {}
    tempo = 0

    def _dfs(no):
        nonlocal tempo
        if no in visitados:
            return
        tempo += 1
        inicio = tempo
        visitados.add(no)
        ordem.append(no)

        for vizinho in adj_list[no]:
            if vizinho not in visitados:
                _dfs(vizinho)

        tempo += 1
        fim = tempo
        tempos[no] = (inicio, fim)

    for no in sorted(adj_list.keys()):
        if no not in visitados:
            _dfs(no)

    return ordem, tempos
