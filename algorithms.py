import math

def initialize_single_source(nodes, source):
    """
    Inicializa as distâncias e predecessores para o Bellman-Ford.
    Distância de cada nó é infinita, exceto a do nó fonte (0).
    """
    dist = {v: math.inf for v in nodes}
    pred = {v: None for v in nodes}
    dist[source] = 0
    return dist, pred


def relax(u, v, w, dist, pred):
    """
    Passo de relaxamento de uma aresta (u, v).
    Se o caminho via u for menor, atualiza dist[v] e pred[v].
    """
    if dist[u] + w < dist[v]:
        dist[v] = dist[u] + w
        pred[v] = u


def bellman_ford(graph, source):
    """
    Implementa o algoritmo de Bellman-Ford.
    
    Parâmetros:
        graph: objeto carregado via pydot (deve ter graph.edges e graph.nodes)
        source: nó de origem

    Retorna:
        (ok, dist, pred)
        - ok: False se houver ciclo negativo, True caso contrário
        - dist: dicionário {nó: distância mínima}
        - pred: predecessores {nó: pai no caminho mínimo}
    """
    # === Inicialização ===
    dist, pred = initialize_single_source(graph.nodes, source)

    # === Obter pesos das arestas ===
    # Se o arquivo DOT tiver 'label' como peso, extrai. Caso contrário, usa 1.
    weighted_edges = []
    for e in graph.get_edges():
        u, v = e.get_source(), e.get_destination()
        label = e.get_label()
        weight = e.get("weight")
        val = label or weight

        try:
            w = int(val) if val is not None else 1
        except ValueError:
            w = 1

        weighted_edges.append((u, v, w))

    # === Relaxamento (|V| - 1) vezes ===
    for _ in range(len(graph.nodes) - 1):
        for (u, v, w) in weighted_edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = u

    # === Detecção de ciclo negativo ===
    for (u, v, w) in weighted_edges:
        if dist[u] + w < dist[v]:
            return False, dist, pred 

    return True, dist, pred
