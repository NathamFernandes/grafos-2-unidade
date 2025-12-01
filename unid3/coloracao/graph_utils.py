import numpy as np
import pydot

GRAPH = "graph"
DIGRAPH = "digraph"


def load_graph_from_file(file_path: str):
    """Carrega o grafo a partir de um arquivo DOT."""
    with open(file_path, "r", encoding="utf-8") as f:
        dot_str = f.read()

    graphs = pydot.graph_from_dot_data(dot_str)
    graph = graphs[0]

    edges = [(e.get_source(), e.get_destination()) for e in graph.get_edges()]
    nodes = sorted(set([a for (a, b) in edges] + [b for (a, b) in edges]))

    graph.nodes = nodes
    graph.edges = edges
    return graph


def get_adjacency_matrix(graph):
    """Retorna a matriz de adjacência do grafo."""
    is_digraph = graph.get_type() == DIGRAPH
    n = len(graph.nodes)

    matrix = np.zeros((n, n), dtype=int)
    for (a, b) in graph.edges:
        row, col = graph.nodes.index(a), graph.nodes.index(b)
        matrix[row][col] = 1
        if not is_digraph:
            matrix[col][row] = 1
    return matrix


def get_adjacency_list(graph):
    """Retorna a lista de adjacência do grafo."""

    is_digraph = graph.get_type() == DIGRAPH
    adj_list = {node: [] for node in graph.nodes}

    for (a, b) in graph.edges:
        adj_list[a].append(b)
        if not is_digraph:
            adj_list[b].append(a)

    for node in adj_list:
        adj_list[node] = sorted(adj_list[node])

    return adj_list


def ler_grafo_matriz_com_label(texto_matriz):
    """
    Lê uma matriz de adjacência em formato de texto e retorna uma lista de adjacência.
    Assume que a primeira linha pode ser um cabeçalho e as demais são no formato 'Label val1 val2...'.

    Exemplo:
         A B C D
       E 0 1 0 0
       F 1 0 1 1
       G 0 1 0 1
       H 0 1 1 0
    """
    linhas = texto_matriz.strip().split('\n')
    adj_list = {}

    for linha in linhas:
        partes = linha.strip().split()

        if len(partes) == 21:
            label_no = partes[0]
            conexoes = partes[1:]

            adj_list[label_no] = []
            for i, valor in enumerate(conexoes):
                if valor == '1':
                    no_destino = str(i + 1)
                    if label_no != no_destino:
                        adj_list[label_no].append(no_destino)

    return adj_list


def ler_grafo_matriz_sem_labels(file_path: str):
    """
    Carrega um grafo a partir de um arquivo de texto contendo matriz de adjacência
    (apenas 0s e 1s, sem labels). Retorna um objeto compatível com pydot.Dot.

    Exemplo:
         0 1 0 0
         1 0 1 1
         0 1 0 1
         0 1 1 0
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Usamos 'digraph' pois as matrizes definem conexões de i -> j.
    # Se a matriz for simétrica (e o grafo então é não direcionado), ficamos com
    # arestas (i,j) e (j,i), o que ainda é compatível com a lógica do
    # get_adjacency_list para Digrafos.
    graph = pydot.Dot(graph_type=DIGRAPH)

    lines = [l.strip() for l in content.strip().split('\n') if l.strip()]

    edges = []
    nodes = [str(i + 1) for i in range(len(lines))]

    for i, line in enumerate(lines):
        u = str(i + 1)
        vals = line.split()
        for j, val in enumerate(vals):
            if val == '1':
                v = str(j + 1)
                if u != v and not (u, v) in edges:
                    edges.append((u, v))

    graph.nodes = nodes
    graph.edges = edges

    return graph


def validar_coloracao(lista_adjacencia, coloracao):
    """
    Verifica se uma coloração é válida para um dado grafo.

    Args:
        lista_adjacencia (dict): {no: [vizinhos]}
        coloracao (dict): {no: cor}

    Returns:
        tuple: (bool, list) -> (Eh_Valido, Lista_de_Erros)
    """
    erros = []

    # 1. Verifica completude (se todos os nós do grafo estão coloridos)
    nos_grafo = set(lista_adjacencia.keys())
    nos_coloridos = set(coloracao.keys())

    nao_coloridos = nos_grafo - nos_coloridos
    if nao_coloridos:
        erros.append(f"Nós sem cor atribuída: {nao_coloridos}")

    # 2. Verifica conflitos de adjacência
    # Usamos um set para evitar duplicar erros
    conflitos_encontrados = set()

    for u, vizinhos in lista_adjacencia.items():
        if u not in coloracao:
            continue

        cor_u = coloracao[u]

        for v in vizinhos:
            if v not in coloracao:
                continue

            cor_v = coloracao[v]

            # Se a cor for igual temos um problema
            if cor_u == cor_v:
                aresta_conflito = tuple(sorted((str(u), str(v))))

                if aresta_conflito not in conflitos_encontrados:
                    erros.append(f"Conflito: Vértices {u} e {
                                 v} são vizinhos e têm a mesma cor ({cor_u}).")
                    conflitos_encontrados.add(aresta_conflito)

    eh_valido = len(erros) == 0
    return eh_valido, erros
