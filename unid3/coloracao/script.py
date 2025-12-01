# script.py

import os
import sys
from graph_utils import load_graph_from_file, get_adjacency_matrix, get_adjacency_list, ler_grafo_matriz_sem_labels, validar_coloracao

from algorithm import paint_dsatur

# === Entrada do arquivo ===

dir = os.path.dirname(__file__)

if len(sys.argv) >= 2:
    file_name = sys.argv[1]
else:
    # Caso padrão para teste rápido se nenhum argumento for passado
    file_name = input("Escreva o nome do arquivo .gv (ex: graph1.gv): ")

file_path = os.path.join(dir, "data", file_name)

if not os.path.exists(file_path):
    print(f"O arquivo não existe na pasta 'data': {file_path}")
    sys.exit()

# === Carregando o grafo ===
try:
    # Direciona a forma de leitura para cada formato
    if file_path.endswith("gvm"):
        graph = ler_grafo_matriz_sem_labels(file_path)
    else:
        graph = load_graph_from_file(file_path)
except Exception as e:
    print(f"Erro ao ler o arquivo: {e}")
    sys.exit()

# === Impressão ===
adjacency_list = get_adjacency_list(graph)

print(f"\nArquivo carregado: {file_name}")
print(f"Tipo do grafo: {graph.get_type()}")
print(f"Nós: {graph.nodes}")

print("\nLista de adjacência (Original):")
for k, v in adjacency_list.items():
    print(f" {k}: {v}")

print("\n--- Executando DSATUR ---")
coloracao = paint_dsatur(adjacency_list)

print("\n--- Validando Coloração ---")
valido, lista_erros = validar_coloracao(adjacency_list, coloracao)

if valido:
    print("SUCESSO: A coloração é válida! Nenhum conflito encontrado.")
else:
    print("ERRO: A coloração é INVÁLIDA.")
    for erro in lista_erros:
        print(f" - {erro}")
