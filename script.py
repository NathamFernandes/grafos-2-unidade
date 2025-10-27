import os
import sys
from graph_utils import load_graph_from_file, get_adjacency_matrix, get_adjacency_list
from algorithms import bfs, bfs_mat_adj, dfs, dfs_forest

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

print(f"\n Arquivo carregado: {file_name}")
print(f" Tipo do grafo: {graph.get_type()}")
print(f" Nós: {graph.nodes}")
print(f" Arestas: {graph.edges}")

print("\nMatriz de adjacência:\n", adjacency_matrix)
print("\nLista de adjacência:")
for k, v in adjacency_list.items():
    print(f" {k}: {v}")

# === Execução de algoritmos ===
if graph.nodes:
    start_node = graph.nodes[0]  # pega o 1º nó ordenado
    print(f"\n BFS a partir de {start_node}: {
        bfs(adjacency_list, start_node)}")
    print(f"\n BFS (mat. adjacência) a partir de {start_node}: {
        bfs_mat_adj(adjacency_matrix, graph.nodes, start_node)}")
    print(f" DFS a partir de {start_node}: {dfs(adjacency_list, start_node)}")
    print(f" Floresta DFS a partir de {start_node}: {
          dfs_forest(adjacency_list)}")
