def insertion_sort(arr, contador):


   # adiciona do segundo elemento até o final da lista
   for i in range(1, len(arr)):
       chave = arr[i]
       j = i - 1


       # move os elementos do arr[0..i-1] que são maiores que a chave
       # para uma posição à frente de sua posição atual
       contador['comparacoes'] += 1  # conta a primeira comparação antes de entrar no loop
       while j >= 0 and chave < arr[j]:
           contador['comparacoes'] += 1  # conta as comparações dentro do loop
           arr[j + 1] = arr[j]
           contador['trocas'] += 1
           j -= 1


       arr[j + 1] = chave
       # troca final nao e contada no loop
   return arr




def merge_sort(arr, contador):


   contador['chamadas_recursivas'] += 1
   if len(arr) > 1:
       meio = len(arr) // 2
       metade_esquerda = arr[:meio]
       metade_direita = arr[meio:]


       # chamada recursiva para cada metade
       merge_sort(metade_esquerda, contador)
       merge_sort(metade_direita, contador)


       i = j = k = 0


       # junta as duas metades na lista original
       while i < len(metade_esquerda) and j < len(metade_direita):
           contador['comparacoes'] += 1
           if metade_esquerda[i] < metade_direita[j]:
               arr[k] = metade_esquerda[i]
               i += 1
           else:
               arr[k] = metade_direita[j]
               j += 1
           k += 1


       while i < len(metade_esquerda):
           arr[k] = metade_esquerda[i]
           i += 1
           k += 1


       while j < len(metade_direita):
           arr[k] = metade_direita[j]
           j += 1
           k += 1
   return arr




def binary_search(arr_ordenado, alvo, contador):


   inicio, fim = 0, len(arr_ordenado) - 1
   while inicio <= fim:
       meio = (inicio + fim) // 2
       contador['comparacoes'] += 1
       if arr_ordenado[meio] == alvo:
           return meio


       contador['comparacoes'] += 1
       if arr_ordenado[meio] < alvo:
           inicio = meio + 1
       else:
           fim = meio - 1
   return -1


import sys


# Constante para representar a ausência de um caminho no grafo
INF = sys.maxsize


def _is_safe_n_queens(board, row, col, n, contador):
   #função auxiliar que verificar se é seguro colocar uma rainha em linha ou coluna
   # verifica a coluna
   for i in range(row):
       contador['comparacoes'] += 1
       if board[i][col] == 1:
           return False


   # verifica a diagonal superior esquerda
   for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
       contador['comparacoes'] += 1
       if board[i][j] == 1:
           return False


   # verifica a diagonal superior direita
   for i, j in zip(range(row, -1, -1), range(col, n)):
       contador['comparacoes'] += 1
       if board[i][j] == 1:
           return False


   return True


def _solve_n_queens_util(board, row, n, contador):
   # função recursiva principal para resolver o problema das N-Rainhas.


   contador['chamadas_recursivas'] += 1
   if row >= n:
       return True # todas as rainhas foram colocadas


   for i in range(n):
       contador['passos_laco'] += 1
       if _is_safe_n_queens(board, row, i, n, contador):
           board[row][i] = 1 # coloca a rainha


           if _solve_n_queens_util(board, row + 1, n, contador):
               return True


           # se colocar a rainha em board[row][i] não leva a uma solução
           # então remove a rainha (BACKTRACK)
           board[row][i] = 0
           contador['backtracks'] += 1


   return False # se a rainha não pode ser colocada em nenhuma coluna desta linha


def n_queens_backtracking(n, contador):
   """
   Função de entrada para o problema das N-Rainhas.
   """
   board = [[0 for _ in range(n)] for _ in range(n)]
   _solve_n_queens_util(board, 0, n, contador)
   return board