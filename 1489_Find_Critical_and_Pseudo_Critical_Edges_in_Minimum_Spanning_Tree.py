from typing import List

class UnionFind:
    
    def __init__(self, n: int) -> None:
        """Inicializa n conjuntos disjuntos, cada um contendo um elemento."""
        self.parent = list(range(n))  # Cada nó é inicialmente seu próprio pai
        self.num_components = n       # Número de componentes conectados

    def union(self, node_a: int, node_b: int) -> bool:
        """
        Une os dois conjuntos que contêm node_a e node_b.
        Retorna True se eles estavam em conjuntos diferentes, False caso contrário.
        """
        root_a = self.find(node_a)
        root_b = self.find(node_b)

        if root_a == root_b:
            return False  # Já estão no mesmo conjunto

        # Une os dois conjuntos fazendo uma raiz apontar para a outra
        self.parent[root_a] = root_b
        self.num_components -= 1
        return True

    def find(self, node: int) -> int:
        """
        Encontra a raiz do conjunto que contém o nó.
        Aplica compressão de caminho para otimização.
        """
        if self.parent[node] != node:
            # Compressão de caminho: faz todos os nós apontarem diretamente para a raiz
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

class Solution:
    def findCriticalAndPseudoCriticalEdges(
        self, n: int, edges: List[List[int]]
    ) -> List[List[int]]:
        """
        Encontra arestas críticas e pseudo-críticas em uma MST.

        Aresta crítica: O peso da MST aumenta se esta aresta for removida.
        Aresta pseudo-crítica: Pode estar em alguma MST, mas não é crítica.
        """
        # Adiciona o índice original a cada aresta para rastreá-las após a ordenação
        for idx, edge in enumerate(edges):
            edge.append(idx)

        # Ordena as arestas por peso para o algoritmo de Kruskal
        edges.sort(key=lambda edge: edge[2])

        # Encontra o peso da MST usando o algoritmo de Kruskal padrão
        uf_mst = UnionFind(n)
        mst_weight = 0
        for from_node, to_node, weight, _ in edges:
            if uf_mst.union(from_node, to_node):
                mst_weight += weight
      
        critical_edges = []
        pseudo_critical_edges = []

        # Verifica cada aresta para determinar se é crítica ou pseudo-crítica
        for from_node, to_node, weight, original_idx in edges:
            # Teste 1: Tenta construir a MST SEM esta aresta
            uf_without = UnionFind(n)
            weight_without = 0
            
            for curr_from, curr_to, curr_weight, curr_idx in edges:
                if curr_idx != original_idx:  # Pula a aresta atual
                    if uf_without.union(curr_from, curr_to):
                        weight_without += curr_weight

            # Se o grafo ficou desconectado ou o peso aumentou, a aresta é crítica
            if uf_without.num_components > 1 or weight_without > mst_weight:
                critical_edges.append(original_idx)
                continue # Pula para a próxima aresta

            # Teste 2: FORÇA a inclusão desta aresta e constrói o resto da MST
            uf_with = UnionFind(n)
            uf_with.union(from_node, to_node)
            weight_with = weight  # Começa com o peso da aresta atual
            
            for curr_from, curr_to, curr_weight, curr_idx in edges:
                # A aresta atual já foi incluída, então a ignoramos aqui
                if uf_with.union(curr_from, curr_to):
                    weight_with += curr_weight
            
            # Se o peso da MST permaneceu o mesmo, a aresta é pseudo-crítica
            if weight_with == mst_weight:
                pseudo_critical_edges.append(original_idx)

        return [critical_edges, pseudo_critical_edges]