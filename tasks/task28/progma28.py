#! /usr/bin/env python3

import re
from typing import List, Dict, Set
import pyperclip

def prepare_samples(sample: str):
    genomes = re.split(r'\)\(', sample)
    ans = []
    for genome in genomes:
        patterns = re.split(r'[()\s]', genome)
        patterns = list(map(int, filter(lambda x: bool(x), patterns)))
        ans.append(patterns)
    return ans

def add_edges_to_breakpoint_graph(seq: List[int], graph: Dict[int, Set[int]]):
    pairs = []
    for v in seq:
        v1, v2 = 2 * (abs(v) - 1), 2 * (abs(v) - 1) + 1
        if v > 0:
            pairs.append((v1, v2))
        else:
            pairs.append((v2, v1))
    
    for pair1, pair2 in zip(pairs, pairs[1:] + [pairs[0]]):
        _, v1 = pair1
        v2, _ = pair2
        
        if v1 not in graph:
            graph[v1] = {v2}
        else:
            graph[v1].add(v2)
        
        if v2 not in graph:
            graph[v2] = {v1}
        else:
            graph[v2].add(v1)

def get_circles_number(graph: Dict[int, Set[int]]):
    used = set()
    graph_size = len(graph)
    circles_number = 0
    
    while len(used) != graph_size:
        start_vertex = None
        for v in graph:
            if v not in used:
                start_vertex = v
        assert(start_vertex is not None)
        
        v = start_vertex
        while True:
            used.add(v)
            neighbours = list(filter(lambda v: v not in used, graph[v]))
            if len(neighbours) == 0:
                circles_number += 1
                break
            else:
                v = neighbours[0]
    return circles_number

def main(sample1: str, sample2: str):
    samples = prepare_samples(sample1)
    samples.extend(prepare_samples(sample2))
    
    graph = dict()
    for sample in samples:
        add_edges_to_breakpoint_graph(sample, graph)
    
    circles_count = get_circles_number(graph)
    blocks_count = len(graph) // 2
    ans = blocks_count - circles_count
    print(ans)
    return ans


# Example test ----------------------------------------------
# sample1 = "(+1 +2 +3 +4 +5 +6)"
# sample2 = "(+1 -3 -6 -5)(+2 -4)"

# main(sample1, sample2)

# Example test 2 ----------------------------------------------
# sample1 = "(+1 +2 +3 +4 +5 +6)"
# sample2 = "(+1 +2 +3 +4 +5 +6)"

# main(sample1, sample2)


# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split("\n")
# f.close()

# main(data[1], data[2])

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split("\n")
f.close()

ans = main(data[0], data[1])

pyperclip.copy(ans)
