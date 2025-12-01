# algorithm.py

def paint_dsatur(adjacency_list):
    """
    Algoritmo de DSATUR (Degree of Saturation).
    Faz a coloração de vértices de um grafo tentando minimizar o número de cores.

    Args:
        adjacency_list (dict): A lista de adjacência {no: [vizinhos]}.

    Returns:
        dict: Dicionário contendo a coloração {no: id_cor}.
    """

    # 1. Pré-processamento: Garantimos que o grafo seja tratado como
    # não-direcionado para a coloração (a existência de A->B implica
    # necessariamente que A e B devem ter cores diferentes independente da
    # existência de B -> A).
    adj = _get_symmetric_adj(adjacency_list)
    print(adj)

    vertices = list(adj.keys())

    # Estruturas de controle
    cores = {v: None for v in vertices}
    saturacao_adj = {v: set() for v in vertices}
    graus = {v: len(adj[v]) for v in vertices}
    nao_coloridos = set(vertices)

    print(f"Iniciando DSATUR com {len(vertices)} vértices")

    while nao_coloridos:
        # 2. Seleção do vértice:
        # Critério 1: Maior grau de saturação
        # Critério 2: Maior grau original
        u = _seleciona_vertice_ideal(nao_coloridos, saturacao_adj, graus)

        # Remove vértice processado
        nao_coloridos.remove(u)

        # 3. Escolha da cor:
        # Busca a menor cor não usada pelos vizinhos
        cores_vizinhos = saturacao_adj[u]
        cor_escolhida = 0
        while cor_escolhida in cores_vizinhos:
            cor_escolhida += 1
        cores[u] = cor_escolhida

        # 4. Atualização:
        # Registra pros vizinhos sua coloração
        for vizinho in adj[u]:
            if vizinho in saturacao_adj:
                saturacao_adj[vizinho].add(cor_escolhida)

    _imprimir_resultado(cores)

    return cores


def _seleciona_vertice_ideal(nao_coloridos, saturacao, graus):
    """
    Seleciona o próximo vértice a ser colorido baseando-se em:
    1. Maior Saturação (len(saturacao[v]))
    2. Maior Grau (graus[v])
    """
    melhor_v = None
    max_sat = -1
    max_grau = -1

    for v in nao_coloridos:
        sat = len(saturacao[v])
        grau = graus[v]

        if sat > max_sat:
            max_sat = sat
            max_grau = grau
            melhor_v = v
        elif sat == max_sat:
            # Desempate pelo grau
            if grau > max_grau:
                max_grau = grau
                melhor_v = v

    return melhor_v


def _get_symmetric_adj(adjacency_list):
    """
    Garante que a lista de adjacência seja simétrica (não direcionada).
    Se A é vizinho de B, B deve ser vizinho de A.
    Isso é crucial para colorir Digrafos corretamente.
    """
    sym_adj = {u: set(vizinhos) for u, vizinhos in adjacency_list.items()}

    for u, vizinhos in adjacency_list.items():
        for v in vizinhos:
            if v not in sym_adj:
                sym_adj[v] = set()
            sym_adj[v].add(u)

    return sym_adj


def _imprimir_resultado(cores):
    """
    Agrupa e imprime os vértices por cor.
    """
    grupos = {}
    for v, cor in cores.items():
        if cor not in grupos:
            grupos[cor] = []
        grupos[cor].append(v)

    print("\n======== Resultado da DSATUR ========")
    print(f"Total de cores utilizadas: {len(grupos)}")

    for cor in sorted(grupos.keys()):
        vertices = sorted(grupos[cor])
        print(f"Cor {cor}: {vertices}")
    print("=======================================\n")
