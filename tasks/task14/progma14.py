#!/usr/bin/env python3

from typing import List, Dict, Set
import sys
import pyperclip

def get_prefix(s: str):
   return s[:-1]

def get_suffix(s: str):
    return s[1:]

def reconstruct_str_from_ordered_patterns(patterns: List[str]) -> str:
    if (len(patterns) <= 1):
        return ''.join(patterns)
    return patterns[0] + ''.join([pattern[-1] for pattern in patterns[1:]])

class Edge(object):
    def __init__(self, edge_name: str, id: int):
        self.value: str = edge_name
        self.id: int = id

    def get_from_node(self):
        return get_prefix(self.value)

    def get_to_node(self):
        return get_suffix(self.value)

    def __str__(self) -> str:
        return str(self.__dict__)
    
    __repr__ = __str__


class Node(object):
    def __init__(self):
        self.in_edges: List[Edge] = list()
        self.out_edges: List[Edge] = list()

    def __str__(self) -> str:
        return str(self.__dict__)

    __repr__ = __str__


class DeBuijnGraph:
    start_node_name: str
    finish_node_name: str
    nodes: Dict[str, Node] = dict()
    edges: List[Edge] = list()    
    virtual_edge_name: str = 'NONE'

    contings: List[List[str]] = []

    def add_edge(self, from_node_name: str, to_node_name: str, edge: str):
        """Добавялет ребро в граф Де Брейна"""
        edge_id = len(self.edges)
        new_edge = Edge(edge, edge_id)

        self.edges.append(new_edge)
        
        node_from = self.nodes.get(from_node_name, Node())
        node_from.out_edges.append(new_edge)
        self.nodes[from_node_name] = node_from
        
        node_to = self.nodes.get(to_node_name, Node())
        node_to.in_edges.append(new_edge)
        self.nodes[to_node_name] = node_to

    def find_all_contings(self):
        # поиск всех стартовых ребер (которые выходят из вершин ! (in(v) == out(v) == 1))
        start_edges = []
        for edge in self.edges:
            from_node = self._get_from_node(edge)
            if not self._is_non_branching_node(from_node):
                start_edges.append(edge)

        unused_edges = set(range(len(self.edges)))
        for start_edge in start_edges:
            self._traverse_graph(start_edge, unused_edges)

        return self.contings

    def _traverse_graph(self, edge: Edge, unused_edges: Set[int]):
        path = [edge.value]
        unused_edges.remove(edge.id)
        to_node = self._get_to_node(edge)
        while self._is_non_branching_node(to_node):
            edge = to_node.out_edges[0]
            path.append(edge.value)
            unused_edges.remove(edge.id)
            to_node = self._get_to_node(edge)

        self.contings.append(path)

    def _get_from_node(self, edge: Edge):
        return self.nodes[edge.get_from_node()]

    def _get_to_node(self, edge: Edge):
        return self.nodes[edge.get_to_node()]

    def _is_non_branching_node(self, node):
        return len(node.out_edges) == 1 and len(node.in_edges) == 1


def main(patterns: List[str]):
    graph = DeBuijnGraph()
    for pattern in patterns:
        graph.add_edge(get_prefix(pattern), get_suffix(pattern), pattern)
    contings = graph.find_all_contings()
    ans = list()
    for conting in contings:
        # print(' => '.join(conting))
        ans.append(reconstruct_str_from_ordered_patterns(conting))
    ans.sort()
    res = ' '.join(ans)
    print(res)
    return res


# data = [
#     'ATG',
#     'ATG',
#     'TGT',
#     'TGG',
#     'CAT',
#     'GGA',
#     'GAT',
#     'AGA'
# ]
# true_ans = ' '.join('AGA ATG ATG CAT GAT TGGA TGT'.split(' '))

f = open('./test.txt')
data = f.read().split()
f.close()

# output_idx = data.index('Output:')

ans = main(data)
# assert(ans == ' '.join(sorted(data[output_idx + 1:])))

pyperclip.copy(ans)
