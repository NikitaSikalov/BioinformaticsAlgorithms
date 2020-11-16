from typing import List, Dict, Set
import pyperclip

def get_prefix(s: str):
    return s[:-1]

def get_suffix(s: str):
    return s[1:]

class Edge(object):
    def __init__(self, edge_name: str, id: int):
        self.used: bool = False
        self.value: str = edge_name
        self.id: int = id

    def get_from_node(self):
        return get_prefix(self.value)

    def get_to_node(self):
        return get_suffix(self.value)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return str(self.__dict__)


class Node(object):
    def __init__(self):
        self.in_edges: List[Edge] = list()
        self.out_edges: List[Edge] = list()

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.__dict__)


class EdgeIterator(object):
    def __init__(self):
        self._list: List[int] = list()
        self._iterator: int = 0

    def push(self, item: int):
        self._list.append(item)
    
    def next(self) -> int:
        next_item = self._list[self._iterator]
        self._iterator += 1
        if self._iterator == len(self._list):
            self._iterator = 0
        return next_item

    def reset(self):
        self._iterator = 0

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return str(self.__dict__)


class DeBuijnGraph:
    start_node_name: str
    finish_node_name: str
    nodes: Dict[str, Node] = dict()
    edges: List[Edge] = list()
    unused_edges: Set[int] = set()
    virtual_edge_name: str = 'NONE'

    def add_edge(self, from_node_name: str, to_node_name: str, edge: str):
        edge_id = len(self.edges)
        new_edge = Edge(edge, edge_id)

        self.edges.append(new_edge)
        
        node_from = self.nodes.get(from_node_name, Node())
        node_from.out_edges.append(new_edge)
        self.nodes[from_node_name] = node_from
        
        node_to = self.nodes.get(to_node_name, Node())
        node_to.in_edges.append(new_edge)
        self.nodes[to_node_name] = node_to

    def get_euiler_path(self) -> List[str]:
        self._add_virtual_edge()
        # print('nodes: ', self.nodes)

        number_of_edges = len(self.edges)
        path = [EdgeIterator() for _ in range(number_of_edges)]
        self.unused_edges = set(range(number_of_edges))
        
        while True:
            start_edge_id = self.unused_edges.pop()
            edge = self.edges[start_edge_id]
            edge.used = True
            last_add_edge_id = self._traverse_graph(edge, path)
            if len(self.unused_edges) is 0:
                path[last_add_edge_id].push(start_edge_id)
                break
        
        start_node = self.nodes[self.start_node_name]
        start_edge = start_node.out_edges[0]
        # print('edges: ', self.edges)
        # print('path: ', path)
        seq = self._unroll_path(start_edge, path)
        # print('seq: ', seq)
        
        ordered_patterns = list(map(lambda edge_id: self.edges[edge_id].value, seq))
        # print('ordered_patterns: ', ordered_patterns)
        assert(ordered_patterns[-1] == 'NONE')
        
        return ordered_patterns[:-1]

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
    
    def _traverse_graph(self, start_edge: Edge, path: List[EdgeIterator]) -> int:
        edge = start_edge
        while True:
            current_edge_id = edge.id
            to_node_name = edge.get_to_node() if edge.value != self.virtual_edge_name else self.start_node_name
            to_node = self.nodes[to_node_name]
            edge = None
            for out_edge in to_node.out_edges:
                if not self.edges[out_edge.id].used:
                    edge = self.edges[out_edge.id]
                    edge.used = True
                    self.unused_edges.remove(edge.id)
                    continue
            if edge is None:
                return current_edge_id
            path[current_edge_id].push(edge.id)

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

    def _unroll_path(self, start_edge: Edge, path: List[EdgeIterator]):
        edge_id = start_edge.id
        res = []
        for _ in range(len(self.edges)):
            res.append(edge_id)
            edge_id = path[edge_id].next()
        return res


def reconstruct_str_from_ordered_patterns(patterns: List[str]) -> str:
    if (len(patterns) <= 1):
        return ''.join(patterns)
    return patterns[0] + ''.join([pattern[-1] for pattern in patterns[1:]])


def main(patterns: List[str]):
    graph = DeBuijnGraph()
    for pattern in patterns:
        graph.add_edge(get_prefix(pattern), get_suffix(pattern), pattern)
    ordered_patterns = graph.get_euiler_path()
    string = reconstruct_str_from_ordered_patterns(ordered_patterns)
    print(string)
    return string
    


f = open('task11/test.txt')
data = f.read().split()
f.close()

res = main(data[1:])
pyperclip.copy(res)

# assert(res == data[-1])
