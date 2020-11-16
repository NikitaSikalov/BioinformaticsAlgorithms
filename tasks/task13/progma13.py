#!/usr/bin/env python3

from typing import List, Dict, Set
import sys
import pyperclip

sys.setrecursionlimit(10000)

SEPARATOR = '|'

def get_prefix(s: str):
   s1, s2 = s.split(SEPARATOR)
   return SEPARATOR.join([s1[:-1], s2[:-1]])

def get_suffix(s: str):
    s1, s2 = s.split(SEPARATOR)
    return SEPARATOR.join([s1[1:], s2[1:]])

def unique_ordered_patterns(all_ordered_patterns: List[List[str]]):
    separator = '#'
    unqiue_ordered_patterns_strs = list(set([separator.join(ordered_pattern) for ordered_pattern in all_ordered_patterns]))
    return [ordered_patterns_str.split(separator) for ordered_patterns_str in unqiue_ordered_patterns_strs]

def reconstruct_str_from_read_pairs(pairs: List[str], k, d):
    n = len(pairs)
    columns_count = (n - 1) + 2 * k + d 
    matrix = [[None] * columns_count for _ in range(n)]
    res = [None] * columns_count
    for row in range(n):
        offset = row
        part1, part2 = pairs[row].split(SEPARATOR)
        for idx, column in enumerate(range(offset, offset + k)):
            matrix[row][column] = part1[idx]
        for idx, column in enumerate(range(offset + k + d, offset + 2 * k + d)):
            matrix[row][column] = part2[idx]
    for column in range(columns_count):
        for row in range(n):
            letter = matrix[row][column]
            if letter is not None:
                if letter is not None and res[column] is not None and res[column] != letter:
                    return None
                elif letter is not None and res[column] is None:
                    res[column] = letter
    return ''.join(res)

def print_matrix(matrix):
    for row in matrix:
        print('\t'.join([str(x) for x in row]))

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

# TESTS -------------------------------------------
def tests():
    # get_prefix
    assert(get_prefix('AG|TC') == 'A|T')
    assert(get_prefix('AAAG|TCAA') == 'AAA|TCA')

    # get_suffix
    assert(get_suffix('AG|TC') == 'G|C')
    assert(get_suffix('AGTC|TCAA') == 'GTC|CAA')
    print('TESTS PASSED')

# tests()
# -------------------------------------------------


class DeBuijnGraph:
    start_node_name: str
    finish_node_name: str
    nodes: Dict[str, Node] = dict()
    edges: List[Edge] = list()    
    virtual_edge_name: str = 'NONE'

    _paths: List[List[int]] = []

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

    def find_all_ordered_paths(self) -> List[List[str]]:
        self._add_virtual_edge()
        self._traverse_graph()
        all_ordered_patterns = self._get_all_ordered_patterns()
        return unique_ordered_patterns(all_ordered_patterns)


    def _add_virtual_edge(self):
        start_vertex = self._get_start_vertex()
        finish_vertex = self._get_finish_vertex()
        self.add_edge(finish_vertex, start_vertex, self.virtual_edge_name)
        
        self.start_node_name = start_vertex
        self.finish_node_name = finish_vertex
        
        start_node = self.nodes[self.start_node_name]
        assert(len(start_node.out_edges) == 1)
        assert(len(start_node.in_edges) == 1)
        
        finish_node = self.nodes[self.finish_node_name]
        assert(len(finish_node.in_edges) == 1)
        assert(len(finish_node.out_edges) == 1)
    
    def _traverse_graph(self, edge: Edge = None, path: List[int] = None, unused_edges: Set[int] = None, used_nodes: Set[str] = None, next_edge_id: int = None):
        if path is None or unused_edges is None or used_nodes is None or edge is None or next_edge_id is None:
            number_of_edges = len(self.edges)
            path = [-1] * number_of_edges
            unused_edges = set(range(len(self.edges)))
            used_nodes = set()
            edge = self.edges[unused_edges.pop()]
            next_edge_id = edge.id
        
        to_node_name = self._get_to_node_name(edge)
        from_node_name = self._get_from_node_name(edge)

        used_nodes.add(to_node_name)
        used_nodes.add(from_node_name)
        
        to_node = self.nodes[to_node_name]
        continue_build_path = False
        for out_edge in to_node.out_edges:
            if out_edge.id in unused_edges:
                next_path = path.copy()
                next_path[edge.id] = out_edge.id

                next_unused_edges = unused_edges.copy()
                next_unused_edges.remove(out_edge.id)

                continue_build_path = True
                self._traverse_graph(
                    edge=out_edge,
                    path=next_path,
                    unused_edges=next_unused_edges,
                    used_nodes=used_nodes.copy(),
                    next_edge_id=next_edge_id,
                )
        
        if not continue_build_path:
            # завершение цикла
            path[edge.id] = next_edge_id
            if len(unused_edges) == 0:
                self._paths.append(path)
            else:
                for unused_edge in [self.edges[edge_id] for edge_id in unused_edges]:
                    # рассматриваем каждое не посещенное на пред шагах ребро, начало (вершину) которого мы уже посетили
                    from_node_name = self._get_from_node_name(unused_edge)
                    if from_node_name in used_nodes:
                        next_unused_edges = unused_edges.copy()
                        next_unused_edges.remove(unused_edge.id)
                        next_path = path.copy()
                        
                        from_node = self.nodes[from_node_name]
                        # рассматривем каждое ребро, которое входит в эту вершину
                        for to_edge in from_node.in_edges:
                            if to_edge.id not in unused_edges:
                                next_edge_id = next_path[to_edge.id]
                                next_path[to_edge.id] = unused_edge.id
                                break
                        
                        self._traverse_graph(
                            edge=unused_edge,
                            path=next_path,
                            unused_edges=next_unused_edges,
                            used_nodes=used_nodes.copy(),
                            next_edge_id=next_edge_id
                        )

    def _get_all_ordered_patterns(self) -> List[List[str]]:
        start_node = self.nodes[self.start_node_name]
        start_edge = start_node.out_edges[0]

        # получаем всевозможные эйлеровы пути в графе
        ordered_paths = [self._unroll_path(start_edge, path) for path in self._paths]
        
        # получаем всевозможные различные упорядоченные комбинации пар геномов
        all_ordered_patterns = []
        for seq in ordered_paths:
            ordered_patterns = list(map(lambda edge_id: self.edges[edge_id].value, seq))
            assert(ordered_patterns[-1] == 'NONE')
            all_ordered_patterns.append(ordered_patterns[:-1])

        return all_ordered_patterns

    def _get_start_vertex(self) -> str:
        for node_name, node in self.nodes.items():
            if len(node.in_edges) == 0:
                return node_name
        raise Exception('Cannot find start vertex')

    def _get_finish_vertex(self) -> str:
        for node_name, node in self.nodes.items():
            if len(node.out_edges) == 0:
                return node_name
        raise Exception('Cannot find finish vertex')

    def _unroll_path(self, start_edge: Edge, path: List[int]):
        edge_id = start_edge.id
        res = []
        for _ in range(len(self.edges)):
            res.append(edge_id)
            edge_id = path[edge_id]
        return res

    def _get_to_node_name(self, edge):
        return edge.get_to_node() if edge.value != self.virtual_edge_name else self.start_node_name
    
    def _get_from_node_name(self, edge):
        return edge.get_from_node() if edge.value != self.virtual_edge_name else self.finish_node_name


    def _print_path(self, path: List[int], start_edge: int):
        print('PATH:')
        id = start_edge
        printed_path = [self.edges[id].value]
        while path[id] != -1:
            printed_path.append(self.edges[path[id]].value)
            id = path[id]
            if id == start_edge:
                print(' => '.join(printed_path))
                return


def main(patterns: List[str], k: int, d: int):
    graph = DeBuijnGraph()
    for pattern in patterns:
        graph.add_edge(get_prefix(pattern), get_suffix(pattern), pattern)
    all_ordered_patterns = graph.find_all_ordered_paths()
    for ordered_patterns in all_ordered_patterns:
        # print(' => '.join(ordered_patterns))
        ans = reconstruct_str_from_read_pairs(ordered_patterns, k, d)
        if ans is not None:
            print(ans)
            return ans


# data = [
#     'GAGA|TTGA',
#     'TCGT|GATG',
#     'CGTG|ATGT',
#     'TGGT|TGAG',
#     'GTGA|TGTT',
#     'GTGG|GTGA',
#     'TGAG|GTTG',
#     'GGTC|GAGA',
#     'GTCG|AGAT'
# ]
# true_ans = 'GTGGTCGTGAGATGTTGA'

f = open('./test.txt')
data = f.read().split()
f.close()

# output_idx = data.index('Output')
# assert(output_idx != -1)

ans = main(data[2:], k=int(data[0]), d=int(data[1]))
# assert(ans == data[output_idx + 1])

# res = main(data[1:])
pyperclip.copy(ans)
