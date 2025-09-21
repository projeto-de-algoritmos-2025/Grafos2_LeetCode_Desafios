'''
3600. Maximize Spanning Tree Stability with Upgrades - https://leetcode.com/problems/maximize-spanning-tree-stability-with-upgrades/description/
'''

from typing import List

class UnionFind:
    '''
    Nesse exercício usamos a estrutura de dados Union-Find é essencial para implementar o algoritmo de Kruskal. 
    Assim, é possível verificar se adicionar uma aresta criará um ciclo.
    '''
    def __init__(self, n: int):
        # Inicializa o Union-Find com 'n' elementos, cada um em seu próprio conjunto.
        self.pai = list(range(n))
        self.num_componentes = n

    def find(self, i: int) -> int:
        # Encontra a raiz do conjunto que contém o nó 'i'.
        if self.pai[i] == i: # Se 'i' é a raiz do seu conjunto, retorna 'i'.
            return i
        # Aplica compressão de caminho para otimizar futuras buscas. 
        # Já que 'i' não é raiz, atualiza o pai de 'i' para ser a raiz do seu conjunto.
        self.pai[i] = self.find(self.pai[i]) 
        return self.pai[i]

    def union(self, i: int, j: int) -> bool:
        # Une os conjuntos que contêm os nós 'i' e 'j'.
        raiz_i = self.find(i)
        raiz_j = self.find(j)
        if raiz_i != raiz_j:
            # Se não estão no mesmo conjunto, a união é possível. Entao, retorna True.
            self.pai[raiz_i] = raiz_j
            self.num_componentes -= 1
            return True
        # Se 'i' e 'j' já estavam conectados, adicionar a aresta formaria um ciclo.
        # A união não é possível e retorna False.
        return False  

class Solution:
    '''
    Cálculo da estabilidade máxima de uma árvore geradora mínima (MST) com arestas que podem ser atualizadas.
    '''
    def maxStability(self, n: int, edges: List[List[int]], k: int) -> int:
        # Função para verificar se é possível alcançar uma determinada estabilidade.
        def can_achieve(estabilidade: int) -> bool:
            # Inicializamos uma estrutura Union-Find para os nós.
            union_find = UnionFind(n)
            upgrades = 0
            
            # Primeiro, adicionamos todas as arestas obrigatórias.
            for u, v, s, must in edges: 
                if must == 1:
                    # Se uma aresta obrigatória não atinge a estabilidade alvo, é impossível.
                    if s < estabilidade:
                        return False
                    # Se as arestas obrigatórias já formam um ciclo, não podemos formar uma árvore geradora.
                    if not union_find.union(u, v):
                        return False

            # Agora, separamos as arestas em duas categorias:
            free_edges = []      # Arestas que não precisam de upgrade.
            upgrade_edges = []   # Arestas que precisam de upgrade.

            for u, v, s, must in edges:
                if must == 0:
                    if s >= estabilidade:
                        # Esta aresta já satisfaz a condição, custo de upgrade = 0.
                        free_edges.append((u, v))
                    # Se a força da aresta for menor que a metade da estabilidade desejada, mesmo com upgrade não será suficiente.
                    elif 2 * s >= estabilidade:
                        # Esta aresta PODE satisfazer a condição, custo de upgrade = 1.
                        upgrade_edges.append((u, v))
            
            # Aqui, usamos as arestas que não precisam de upgrade.
            for u, v in free_edges:
                union_find.union(u, v)

            # Se o grafo ainda não estiver totalmente conectado, usamos as arestas que precisam de upgrade, contanto que tenhamos upgrades disponíveis (k).
            for u, v in upgrade_edges:
                if upgrades < k:
                    # Verificamos se a aresta conecta dois componentes diferentes.
                    if union_find.find(u) != union_find.find(v):
                        union_find.union(u, v)
                        upgrades += 1
                else:
                    break 

            # No final, verificamos se todos os nós estão conectados.
            return union_find.num_componentes == 1

        # Usamos busca binária para encontrar a estabilidade máxima possível.
        # O limite superior é baseado na força máxima possível das arestas.
        # A estabilidade mínima possível é 0.
        low = 0
        high = 2 * 10**9 + 7 
        res = -1

        while low <= high:
            mid = (low + high) // 2
            # Sem arestas para conectar
            if mid == 0 and n > 1 and not edges: 
                 high = mid -1
                 continue

            # Se conseguimos alcançar a estabilidade 'mid', tentamos um alvo maior.
            if can_achieve(mid):
                res = mid
                low = mid + 1
            else:
                # Se não conseguimos, 'mid' é muito alto. Precisamos diminuir o alvo.
                high = mid - 1
        
        return res