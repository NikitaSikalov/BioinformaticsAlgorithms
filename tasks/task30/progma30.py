#! /usr/bin/env python3

import re
from typing import List, Dict, Set, Tuple
import pyperclip

def prepare_samples(sample: str):
    genomes = re.split(r'\)\(', sample)
    ans = []
    for genome in genomes:
        patterns = re.split(r'[()\s]', genome)
        patterns = list(map(int, filter(lambda x: bool(x), patterns)))
        ans.append(patterns)
    return ans

def prepare_idxes(s: str) -> Tuple[int, ...]:
    res =  tuple(map(int, s.strip().split(", ")))
    assert(len(res) == 4)
    return res

def circles_to_str(circles: List[List[int]]):
    ans = []
    for circle in circles:
        tmp = "(" + " ".join([str(x) if x < 0 else "+%d" % x for x in circle]) + ")"
        ans.append(tmp)
    return "".join(ans)

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

def break_2_on_genome_graph(graph: Dict[int, Set[int]], idxes: Tuple[int, ...]):
    assert(len(idxes) == 4)
    i1, i2, i3, i4 = map(lambda x: x - 1, idxes)
    
    if i1 in graph:
        graph[i1].remove(i2)
        graph[i1].add(i3)
    else:
        graph[i1] = {i3}
    
    if i2 in graph:
        graph[i2].remove(i1)
        graph[i2].add(i4)
    else:
        graph[i2] = {i4}
    
    if i3 in graph:
        graph[i3].remove(i4)
        graph[i3].add(i1)
    else:
        graph[i3] = {i1}

    if i4 in graph:
        graph[i4].remove(i3)
        graph[i4].add(i2)
    else:
        graph[i4] = {i2}

def get_circle_genomes(graph: Dict[int, Set[int]]):
    used = set()
    graph_size = len(graph)
    circles = []
    
    while len(used) != graph_size:
        unused = set(graph.keys()) - used
        v = min(unused)
        circle = []
        
        while True:
            used.add(v)
            n = v // 2 + 1
            if v % 2 == 0:
                used.add(v + 1)
                circle.append(n)
                v = v + 1
            else:
                used.add(v - 1)
                circle.append(-n)
                v = v - 1
            neighbours = list(filter(lambda v: v not in used, graph[v]))
            if len(neighbours) == 0:
                circles.append(circle)
                break
            else:
                v = neighbours[0]
    return circles
    
def main(sample: str, str_idxes: str):
    samples = prepare_samples(sample)
    idxes = prepare_idxes(str_idxes)
    
    graph = dict()
    for genome in samples:
        add_edges_to_breakpoint_graph(genome, graph)
    break_2_on_genome_graph(graph, idxes)
    circles = get_circle_genomes(graph)
    ans = circles_to_str(circles)
    print(ans)
    return ans


# Example test ----------------------------------------------
# sample = "(+1 -2 -4 +3)"
# idxes = "1, 6, 3, 8"

# main(sample, idxes)


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
