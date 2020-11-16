#!/usr/bin/env python3

from typing import List, Dict, Set
import sys
import pyperclip

SEPARATOR = '|'

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


# Example test ----------------------------------------------
# data = [
#     'GACC|GCGC',
#     'ACCG|CGCC',
#     'CCGA|GCCG',
#     'CGAG|CCGG',
#     'GAGC|CGGA'
# ]
# k = 4
# d = 2
# ans = reconstruct_str_from_read_pairs(data, k=k, d=d)

# true_ans = 'GACCGAGCGCCGGA'
# print(ans)
# assert(ans == true_ans)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()

# output_idx = data.index('Output')
# ans = reconstruct_str_from_read_pairs(data[3:output_idx], k=int(data[1]), d=int(data[2]))

# true_ans = data[-1]

# print(ans)
# assert(ans == true_ans)

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()

ans = reconstruct_str_from_read_pairs(data[2:], k=int(data[0]), d=int(data[1]))
print(ans)

pyperclip.copy(ans)
