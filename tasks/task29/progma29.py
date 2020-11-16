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
    # i1, i2, i3, i4 = map(lambda x: x - 1, idxes)
    i1, i2, i3, i4 = idxes
    
    if i1 in graph:
        graph[i1].remove(i2)
        graph[i1].add(i4)
    else:
        graph[i1] = {i4}
    
    if i2 in graph:
        graph[i2].remove(i1)
        graph[i2].add(i3)
    else:
        graph[i2] = {i3}
    
    if i3 in graph:
        graph[i3].remove(i4)
        graph[i3].add(i2)
    else:
        graph[i3] = {i2}

    if i4 in graph:
        graph[i4].remove(i3)
        graph[i4].add(i1)
    else:
        graph[i4] = {i1}

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

def get_colored_circles(graph: Dict[int, Set[int]]):
    used = set()
    graph_size = len(graph)
    circles = []
    
    while len(used) != graph_size:
        unused = set(graph.keys()) - used
        v = min(unused)
        circle = []
        while True:
            used.add(v)
            circle.append(v)
            neighbours = list(filter(lambda v: v not in used, graph[v]))
            if len(neighbours) == 0:
                circles.append(circle)
                break
            else:
                v = neighbours[0]
    return circles

def merge_graphs(blue_graph: Dict[int, Set[int]], red_graph: Dict[int, Set[int]]):
    graph = {}
    vertecies = set(list(blue_graph.keys()) + list(red_graph.keys()))
    for v in vertecies:
        if v not in blue_graph:
            blue_graph[v] = set()
        if v not in red_graph:
            red_graph[v] = set()
        graph[v] = blue_graph[v].union(red_graph[v])
    return graph

def breakpoint_graph_to_str(graph: Dict[int, Set[int]]) -> str:
    circles = get_circle_genomes(graph)
    return circles_to_str(circles)

def get_blue_edge_in_non_trivial_circle(blue_graph: Dict[int, Set[int]], circles: List[List[int]]):
    for circle in circles:
        # trivial circle => skip
        if len(circle) == 2:
            continue
        edges = zip(circle, circle[1:] + [circle[0]]) 
        for v1, v2 in edges:
            if v1 in blue_graph and v2 in blue_graph[v1]:
                return (v1, v2)
    return None

def main(samples1_str: str, samples2_str: str):
    samples1 = prepare_samples(samples1_str)
    samples2 = prepare_samples(samples2_str) 
    steps = []
    
    red_graph = dict()
    blue_graph = dict()
    for genome in samples1:
        add_edges_to_breakpoint_graph(genome, red_graph)
    for genome in samples2:
        add_edges_to_breakpoint_graph(genome, blue_graph)
    
    graph = merge_graphs(blue_graph, red_graph)
    blocks_count = len(graph) // 2
    colored_circles = get_colored_circles(graph)
    steps.append(breakpoint_graph_to_str(red_graph))
    while len(colored_circles) != blocks_count:
        blue_edge = get_blue_edge_in_non_trivial_circle(blue_graph, colored_circles)
        assert(blue_edge is not None)

        i2, i3 = blue_edge
        i1 = list(red_graph[i2])[0]
        i4 = list(red_graph[i3])[0]
        break_2_on_genome_graph(red_graph, (i1, i2, i3, i4))
        graph = merge_graphs(blue_graph, red_graph)
        steps.append(breakpoint_graph_to_str(red_graph))
        colored_circles = get_colored_circles(graph)

    ans = "\n".join(steps)
    print(ans)
    return ans


# Example test ----------------------------------------------
# sample1 = "(+1 +2 +3 +4)"
# sample2 = "(+1 +2 +3 +4)"

# main(sample1, sample2)


# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split("\n")
# f.close()

# ans = main(data[1], data[2])

# assert(len(ans.split("\n")) == len(list(filter(lambda s: s.strip() != "", data[4:]))))

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split("\n")
f.close()

ans = main(data[0], data[1])

pyperclip.copy(ans)
