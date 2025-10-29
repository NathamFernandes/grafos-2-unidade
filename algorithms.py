import math
import heapq


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

def floyd_warshall(graph):
    """
    Algoritmo de Floyd-Warshall.
    Calcula as distâncias mínimas entre todos os pares de vértices.
    graph: dicionário de adjacência com pesos (ex: {'a': {'b': 3, 'c': 5}})
    Retorna: dicionário com distâncias mínimas entre todos os pares.
    """
    vertices = list(graph.keys())
    dist = {u: {v: float('inf') for v in vertices} for u in vertices}

    # Distância de cada vértice para si mesmo é 0
    for v in vertices:
        dist[v][v] = 0

    # Inicializa as distâncias diretas (arestas existentes)
    for u in graph:
        for v, w in graph[u].items():
            dist[u][v] = w

    # Relaxamento de todas as combinações de vértices
    for k in vertices:
        for i in vertices:
            for j in vertices:
                if dist[i][j] == float('inf'):
                    dist[i][j] = math.inf

    return dist


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


def prim(graph, source):
    """
    Implementa o algoritmo de Prim para encontrar a Árvore Geradora Mínima (AGM).
    A complexidade é O(E log V) usando uma min-heap.
    """

    # Inicializações
    key = {v: math.inf for v in graph.nodes}
    pred = {v: None for v in graph.nodes}

    key[source] = 0

    Q = [(key[v], v) for v in graph.nodes]
    heapq.heapify(Q)

    in_mst = set()

    # Estrutura de adjacências
    adj = {node: [] for node in graph.nodes}
    for e in graph.get_edges():
        u, v = e.get_source(), e.get_destination()
        label = e.get_label()
        weight = e.get("weight")
        val = label or weight

        try:
            w = int(val) if val is not None else 1
        except ValueError:
            w = 1
        adj[u].append((v, w))
        adj[v].append((u, w))

    # Laço principal
    while Q:
        # Extrai o nó u com a menor chave
        k, u = heapq.heappop(Q)

        # Se 'u' já foi adicionado à AGM, esse 'k' é de uma entrada
        # antiga e mais cara
        if u in in_mst:
            continue

        in_mst.add(u)

        # Para cada vizinho v de u
        for v, w in adj[u]:
            if v in in_mst:
                continue

            if w < key[v]:
                key[v] = w
                pred[v] = u
                heapq.heappush(Q, (key[v], v))

    total_cost = sum(key[v] for v in graph.nodes if key[v] != math.inf)

    return total_cost, pred
