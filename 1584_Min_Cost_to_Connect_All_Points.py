'''
1584. Min Cost to Connect All Points - https://leetcode.com/problems/min-cost-to-connect-all-points/description/
'''


import math 

class Solution:
    def minCostConnectPoints(self, points: list[list[int]]) -> int:
        """
        Encontra o custo mínimo para conectar todos os pontos usando a distância de Manhattan.
        Usa o algoritmo de Prim para encontrar a Árvore Geradora Mínima

        """
        n = len(points)

        # Inicializa as estruturas de dados para o algoritmo de Prim
        custo_min = [math.inf] * n  # Distância mínima para conectar cada vértice à MST
        visitado = [False] * n     # Rastreia quais vértices já estão na MST
        custo_total = 0
        arestas_adicionadas = 0

        # Começa pelo vértice 0
        custo_min[0] = 0

        # O laço principal continua até que todos os n vértices estejam na MST
        while arestas_adicionadas < n:
            # Encontra o vértice não visitado com a menor distância para a MST
            vertice_atual = -1
            menor_distancia = math.inf

            for i in range(n):
                if not visitado[i] and custo_min[i] < menor_distancia:
                    menor_distancia = custo_min[i]
                    vertice_atual = i
            
            # Se não encontrou nenhum vértice, pode parar (embora isso não deva acontecer em um grafo conectado)
            if vertice_atual == -1:
                break

            # Adiciona o custo do vértice encontrado e o marca como visitado
            custo_total += menor_distancia
            visitado[vertice_atual] = True
            arestas_adicionadas += 1

            # Atualiza as distâncias mínimas para os vértices vizinhos
            x1, y1 = points[vertice_atual]
            for vizinho in range(n):
                if not visitado[vizinho]:
                    x2, y2 = points[vizinho]
                    distancia = abs(x1 - x2) + abs(y1 - y2)
                    
                    # Se a nova distância for menor, atualiza o custo mínimo para aquele vizinho
                    if distancia < custo_min[vizinho]:
                        custo_min[vizinho] = distancia
        
        return custo_total