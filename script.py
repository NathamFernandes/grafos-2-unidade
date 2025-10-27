import os
import sys
from graph_utils import load_graph_from_file, get_adjacency_matrix, get_adjacency_list
from algorithms import bellman_ford

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
