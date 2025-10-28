import os
import sys
import math
from graph_utils import load_graph_from_file, get_adjacency_matrix, get_adjacency_list
from algorithms import bellman_ford, prim

# === Entrada do arquivo ===
dir = os.path.dirname(__file__)

if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    file_name = input("Escreva o nome do arquivo .gv (ex: graph1.gv): ")

file_path = os.path.join(dir, "data", file_name)

if not os.path.exists(file_path):
    print("O arquivo não existe na pasta 'data'!")
    sys.exit()

# === Carregando o grafo ===
graph = load_graph_from_file(file_path)

# === Representações ===
adjacency_matrix = get_adjacency_matrix(graph)
adjacency_list = get_adjacency_list(graph)

print(f"\nArquivo carregado: {file_name}")
print(f"Tipo do grafo: {graph.get_type()}")
print(f"Nós: {graph.nodes}")
print(f"Arestas: {graph.edges}")

print("\nMatriz de adjacência:\n", adjacency_matrix)
print("\nLista de adjacência:")
for k, v in adjacency_list.items():
    print(f" {k}: {v}")

# === Execução do algoritmo de Bellman-Ford ===
if graph.nodes:
    start_node = graph.nodes[0]
    print(f"\n--- Algoritmo de Bellman-Ford ---")
    print(f"Nó de origem: {start_node}")

    ok, dist, pred = bellman_ford(graph, start_node)

    if not ok:
        print("\nCiclo de peso negativo detectado! O algoritmo não pôde determinar os menores caminhos.")
    else:
        print("\nDistâncias mínimas a partir do nó de origem:")
        for v in graph.nodes:
            d = dist[v]
            p = pred[v]
            if d == float("inf"):
                print(f" {v}: inacessível")
            else:
                print(f" {v}: distância = {d}, predecessor = {p}")

# === Execução do algoritmo de Prim ===
if graph.nodes:
    start_node = list(graph.nodes)[0]

    print(f"\n--- Algoritmo de Prim (Árvore Geradora Mínima - AGM) ---")
    print(f"Nó de origem: {start_node}")

    cost, pred = prim(graph, start_node)

    if cost != math.inf:
        print(f"Custo Total da AGM: {cost}")
    else:
        print("O grafo não é conexo (não foi possível alcançar todos os nós).")

    print("\nEstrutura da AGM:")

    mst_edges = []

    for v in graph.nodes:
        parent = pred.get(v)

        if parent is not None:
            mst_edges.append((parent, v))

    if mst_edges:
        print(f"Arestas (pai -> filho) que compõem a AGM:")
        for u, v in sorted(mst_edges):
            print(f"  {u} -- {v}")
    else:
        if len(graph.nodes) > 1 and cost != 0:
            print("  Não foi possível formar a AGM a partir da origem.")
        elif len(graph.nodes) == 1:
            print("  O grafo tem apenas um nó (AGM trivial).")

    print("\nPredecessores (Nó: Pai na AGM):")
    for v in sorted(graph.nodes):
        predecessor = pred.get(v)
        if predecessor is not None:
            print(f"  {v}: {predecessor}")
        elif v == start_node:
            print(f"  {v}: (Origem)")
        else:
            print(f"  {v}: (Inalcançável)")
