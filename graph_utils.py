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

    # Edges
    edges = [(e.get_source(), e.get_destination()) for e in graph.get_edges()]

    # Nodes (garante ordem alfabética)
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

    # Ordena vizinhos para consistência
    for node in adj_list:
        adj_list[node] = sorted(adj_list[node])

    return adj_list

def to_weighted(graph):
    weighted = {}
    for u, neighbors in graph.items():
        weighted[u] = {v: 1 for v in neighbors}
    return weighted
