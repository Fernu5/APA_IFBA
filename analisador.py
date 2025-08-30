# Ferramenta para análise de performance e complexidade de algoritmos.
import timeit
import random
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import defaultdict

from algoritmos import (
   insertion_sort,
   merge_sort,
   binary_search,
   n_queens_backtracking,
   INF
)

class AnalisadorDeAlgoritmos:
   """
   Classe que encapsula a lógica para analisar e comparar algoritmos
   em diferentes cenários e exibe a complexidade nos resultados
   """

   def __init__(self):
       self.algoritmos = {}
       self.resultados = []
       self.complexidades = {}

   def adicionar_algoritmo(self, nome, funcao, pior_caso, melhor_caso):
       self.algoritmos[nome] = funcao
       self.complexidades[nome] = {"pior_caso": pior_caso, "melhor_caso": melhor_caso}
       print(f"Algoritmo '{nome}' adicionado com complexidade teórica (Pior: {pior_caso}, Melhor: {melhor_caso}).")

   def _gerar_entrada(self, tamanho, tipo='ordenacao', cenario='aleatorio'):
       """
       Gera dados de entrada para os testes
       """
       if tipo == 'ordenacao':
           arr = np.arange(tamanho)
           np.random.shuffle(arr)
           arr = arr.tolist()
           if cenario == 'ordenado':
               arr.sort()
           elif cenario == 'invertido':
               arr.sort(reverse=True)
           return arr
       elif tipo == 'busca':
           arr = sorted(np.random.randint(0, tamanho * 10, size=tamanho).tolist())
           if cenario == 'melhor':
               alvo = arr[tamanho // 2]
           elif cenario == 'pior':
               alvo = -1
           else:
               alvo = random.randint(0, tamanho * 10)
           return arr, alvo
       return tamanho

   def executar_analise(self, tamanhos_entrada, cenarios=['aleatorio']):
       print(f"\nIniciando análise para os cenários: {', '.join(cenarios)}...")
       self.resultados = []
       for cenario in cenarios:
           print(f"\n--- Processando Cenário: {cenario.upper()} ---")
           for nome, funcao in self.algoritmos.items():
               print(f"  Analisando '{nome}'...")
               for n in tamanhos_entrada:
                   contador = defaultdict(int)
                   def run_test():
                       if "Busca Binária" in nome:
                           tipo_entrada = 'busca'
                       elif "Floyd-Warshall" in nome:
                           tipo_entrada = 'floyd_warshall'
                       elif "N-Rainhas" in nome:
                           tipo_entrada = 'n_queens'
                       else:
                           tipo_entrada = 'ordenacao'
                       entrada_dados = self._gerar_entrada(n, tipo=tipo_entrada, cenario=cenario)
                       contador.clear()
                       if tipo_entrada == 'ordenacao':
                           funcao(entrada_dados.copy(), contador)
                       elif tipo_entrada == 'busca':
                           funcao(entrada_dados[0].copy(), entrada_dados[1], contador)
                       else:
                           funcao(n, contador)
                   tempo = timeit.timeit(stmt=run_test, number=5) / 5
                   run_test()
                   self.resultados.append({
                       "Algoritmo": nome,
                       "Cenário": cenario.replace('_', ' ').capitalize(),
                       "Tamanho (N)": n,
                       "Tempo (s)": tempo,
                       "Operações": sum(contador.values()),
                   })
       print("Análise concluída.")

   def exibir_resultados(self):
       if not self.resultados:
           print("Nenhum resultado para exibir. Execute a análise primeiro.")
           return
       headers = ["Algoritmo", "Cenário", "Tamanho (N)", "Tempo (s)", "Operações", "Pior Caso (Teórico)",
                  "Melhor Caso (Teórico)"]
       dados_tabela = []
       for r in sorted(self.resultados, key=lambda x: (x["Algoritmo"], x["Cenário"], x["Tamanho (N)"])):
           complexidade = self.complexidades.get(r["Algoritmo"], {})
           dados_tabela.append([
               r["Algoritmo"],
               r["Cenário"],
               r["Tamanho (N)"],
               f"{r['Tempo (s)']:.6f}",
               r["Operações"],
               complexidade.get("pior_caso", "N/A"),
               complexidade.get("melhor_caso", "N/A")
           ])
       print("\n" + "=" * 120)
       print(" " * 45 + "Resultados da Análise Empírica e Teórica")
       print("=" * 120)
       print(tabulate(dados_tabela, headers=headers, tablefmt="grid"))

   def plotar_graficos(self, titulo_figura='Análise Comparativa'):
       if not self.resultados: return
       fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))
       fig.suptitle(titulo_figura, fontsize=16)
       ax1.set_title('Tempo de Execução vs. Tamanho da Entrada (N)');
       ax1.set_xlabel('Tamanho da Entrada (N)');
       ax1.set_ylabel('Tempo de Execução (segundos)');
       ax1.grid(True)
       ax2.set_title('Total de Operações vs. Tamanho da Entrada (N)');
       ax2.set_xlabel('Tamanho da Entrada (N)');
       ax2.set_ylabel('Número de Operações');
       ax2.grid(True)
       grouped_results = defaultdict(list)
       for r in self.resultados: grouped_results[(r['Algoritmo'], r['Cenário'])].append(r)
       for (nome_algo, cenario), dados in grouped_results.items():
           dados.sort(key=lambda x: x['Tamanho (N)'])
           tamanhos = [r['Tamanho (N)'] for r in dados];
           tempos = [r['Tempo (s)'] for r in dados];
           operacoes = [r['Operações'] for r in dados]
           label = f"{nome_algo} ({cenario})"
           ax1.plot(tamanhos, tempos, marker='o', label=label);
           ax2.plot(tamanhos, operacoes, marker='x', linestyle='--', label=label)
       ax1.legend();
       ax2.legend()
       plt.tight_layout(rect=[0, 0, 1, 0.96])

if __name__ == '__main__':
   analisador_ordenacao = AnalisadorDeAlgoritmos()
   analisador_ordenacao.adicionar_algoritmo("Insertion Sort", insertion_sort, pior_caso="O(n²)", melhor_caso="Ω(n)")
   analisador_ordenacao.adicionar_algoritmo("Merge Sort", merge_sort, pior_caso="Θ(n log n)", melhor_caso="Θ(n log n)")
   tamanhos_ordenacao = [100, 250, 500, 1000, 2000]
   cenarios_ordenacao = ['ordenado', 'aleatorio', 'invertido']
   analisador_ordenacao.executar_analise(tamanhos_ordenacao, cenarios=cenarios_ordenacao)
   analisador_ordenacao.exibir_resultados()

   analisador_busca = AnalisadorDeAlgoritmos()
   analisador_busca.adicionar_algoritmo("Busca Binária", binary_search, pior_caso="O(log n)", melhor_caso="Ω(1)")
   tamanhos_busca = [1000, 10000, 50000, 100000, 200000]
   cenarios_busca = ['melhor', 'pior', 'aleatorio']
   analisador_busca.executar_analise(tamanhos_busca, cenarios=cenarios_busca)
   analisador_busca.exibir_resultados()

   def fw_wrapper(V, contador):
       graph = [[(random.randint(1, 100) if i != j else 0) for j in range(V)] for i in range(V)]
       return floyd_warshall(graph, contador)

   # analise do algoritmo n-rainhas com backtracking
   analisador_nq = AnalisadorDeAlgoritmos()
   analisador_nq.adicionar_algoritmo("N-Rainhas", n_queens_backtracking, pior_caso="O(N!)", melhor_caso="O(N!)")
   tamanhos_nq = [4, 5, 6, 7, 8, 9]
   analisador_nq.executar_analise(tamanhos_nq, cenarios=['aleatorio'])
   analisador_nq.exibir_resultados()

   print("\nExibindo todos os gráficos...")
   analisador_ordenacao.plotar_graficos("Análise de Algoritmos de Ordenação")
   analisador_busca.plotar_graficos("Análise de Algoritmo de Busca")
   analisador_nq.plotar_graficos("Análise do Algoritmo N-Rainhas")
   plt.show()