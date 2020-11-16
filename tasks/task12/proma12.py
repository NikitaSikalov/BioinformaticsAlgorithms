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


class DeBuijnGraph:
    start_node_name: str
    finish_node_name: str
    nodes: Dict[str, Node] = dict()
    edges: List[Edge] = list()
    unused_edges: Set[int] = set()

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
        number_of_edges = len(self.edges)
        path = [-1] * number_of_edges
        self.unused_edges = set(range(number_of_edges))
        
        while len(self.unused_edges) != 0:
            start_edge_id = self.unused_edges.pop()
            start_edge = self.edges[start_edge_id]
            
            last_edge_id = None

            from_node = self.nodes[start_edge.get_from_node()]
            for to_edge in from_node.in_edges:
                if to_edge.used:
                    last_edge_id = path[to_edge.id]
                    path[to_edge.id] = start_edge_id
                    break

            edge = self.edges[start_edge_id]
            edge.used = True
            last_add_edge_id = self._traverse_graph(edge, path)
            path[last_add_edge_id] = start_edge_id if last_edge_id is None else last_edge_id
                    
        start_edge = self.edges[0]
        
        for edge in self.edges:
            if not '1' in edge.value:
                start_edge = edge

        seq = self._unroll_path(start_edge, path)
        
        ordered_patterns = list(map(lambda edge_id: self.edges[edge_id].value, seq))        
        return ordered_patterns
    
    def _traverse_graph(self, start_edge: Edge, path: List[int]) -> int:
        edge = start_edge
        while True:
            current_edge_id = edge.id
            to_node_name = edge.get_to_node()
            to_node = self.nodes[to_node_name]
            edge = None
            for out_edge in to_node.out_edges:
                if not self.edges[out_edge.id].used:
                    edge = self.edges[out_edge.id]
                    edge.used = True
                    self.unused_edges.remove(edge.id)
                    break
            if edge is None:
                return current_edge_id
            path[current_edge_id] = edge.id

    def _unroll_path(self, start_edge: Edge, path: List[int]):
        edge_id = start_edge.id
        res = []
        for _ in range(len(self.edges)):
            res.append(edge_id)
            edge_id = path[edge_id]
        return res

    def _print_path(self, path: List[int], start_edge: int):
        print('PATH:')
        id = start_edge
        while path[id] != -1:
            print('{} => {}'.format(self.edges[id].value, self.edges[path[id]].value))
            id = path[id]
            if id == start_edge:
                return


def circle_str_from_ordered_patterns(patterns: List[str]) -> str:
    if (len(patterns) <= 1):
        return ''.join(patterns)
    full_str = patterns[0] + ''.join([pattern[-1] for pattern in patterns[1:]])
    for sub_str_len in range(1, len(full_str)):
        if full_str[-sub_str_len:] != full_str[:sub_str_len]:
            return full_str[:-sub_str_len + 1]
    return ''


def get_patterns(k: int) -> List[str]:
    patterns = ['0', '1']
    for _ in range(k - 1):
        next_patterns = []
        for pattern in patterns:
            next_patterns.append(pattern + '0')
            next_patterns.append(pattern + '1')
        patterns = next_patterns
    return patterns


def main(patterns: List[str]):
    graph = DeBuijnGraph()
    for pattern in patterns:
        graph.add_edge(get_prefix(pattern), get_suffix(pattern), pattern)
    ordered_patterns = graph.get_euiler_path()
    # print(ordered_patterns)
    string = circle_str_from_ordered_patterns(ordered_patterns)
    print(string)
    return string
    

def get_all_substrings(s, k):
    """Get all substrings length k from string s

    Args:
        s (str): test string
        k (int): length of substring
    """
    return [s[ptr:ptr + k] for ptr in range(len(s) - k + 1)]


k = 9
patterns = get_patterns(k)
patterns.sort()

assert(len(patterns) == 2 ** k)
assert(len(set(patterns)) == 2 ** k)

correct_str = '||'.join(patterns)

res_str = main(patterns)
patterns_from_str = list(set(get_all_substrings(res_str + res_str, k)))
patterns_from_str.sort()
test_str = '||'.join(patterns_from_str)

assert(test_str == correct_str)


pyperclip.copy(res_str)

# f = open('task12/debug.txt')
# data = f.read().split()
# f.close()
# assert(len(data[3]) == len(res_str))
