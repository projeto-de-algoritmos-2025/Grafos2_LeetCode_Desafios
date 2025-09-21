'''
743. Network Delay Time - https://leetcode.com/problems/network-delay-time/description/
'''

import collections
import heapq
from typing import List

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Para representar o grafo, foi utilizada uma lista de adjacências.
        # Onde cada chave é um nó e o valor é uma lista de tuplas (vizinho, peso), permitindo acesso eficiente aos vizinhos de cada nó.
        grafo = collections.defaultdict(list)
        for u, v, w in times:
            grafo[u].append((v, w))

        # Para a implementação do algoritmo de Dijkstra, utilizamos uma fila de prioridade (min-heap), que vai explorar sempre o nó com o menor custo acumulado.
        # Além disso, vai armazenar tuplas (tempo_acumulado, nó_atual).
        fila_prioridade = [(0, k)]  # Começamos com o nó k, com tempo 0.

        # `distancias` armazena o menor tempo conhecido do nó `k` até cada novo nó.
        # Iniciamos todas as distâncias como infinito, pois ainda não conhecemos nenhum caminho.
        distancias = {}

        # Aqui, implementamos o algoritmo de Dijkstra.
        while fila_prioridade:
            # Pega o nó da fila que tem o menor tempo acumulado.
            tempo, no = heapq.heappop(fila_prioridade)

            # Se já encontramos um caminho mais curto para este nó, ignoramos, evitando ciclos.
            if no in distancias:
                continue

            # Registra o tempo mínimo encontrado para chegar a este nó.
            distancias[no] = tempo

            # Agora, exploramos os vizinhos do nó atual.
            for vizinho, tempo_aresta in grafo[no]:
                # Se ainda não encontramos um caminho final para o vizinho, calculamos o novo tempo para chegar ao vizinho através do nó atual.
                if vizinho not in distancias:
                    novo_tempo = tempo + tempo_aresta
                    # Adicionamos o vizinho à fila de prioridade com seu novo tempo.
                    heapq.heappush(fila_prioridade, (novo_tempo, vizinho))

        # Se o número de nós alcançados (o tamanho de `distancias`) for menor que `n`, significa que algum nó é inalcançável a partir de `k`.
        if len(distancias) < n:
            return -1

        # Caso contrário, o tempo necessário para que todos os nós recebam a mensagem é o maior tempo registrado em `distancias`.
        return max(distancias.values())