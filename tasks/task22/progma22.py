#! /usr/bin/env python3

from typing import List
import pyperclip

def longest_path(down_matrix: List[List[int]], right_matrix: List[List[int]]) -> int:
    rows_number = len(down_matrix) + 1
    columns_number = len(right_matrix[0]) + 1
    longest_paths = [[0] * columns_number for _ in range(rows_number)]
    # fill first column
    for row in range(1, rows_number):
        longest_paths[row][0] = longest_paths[row - 1][0] + down_matrix[row - 1][0]
    
    # fill first row
    for column in range(1, columns_number):
        longest_paths[0][column] = longest_paths[0][column - 1] + right_matrix[0][column - 1]

    # fill rest table
    for i in range(1, rows_number):
        for j in range(1, columns_number):
            longest_paths[i][j] = max(longest_paths[i - 1][j] + down_matrix[i - 1][j], longest_paths[i][j - 1] + right_matrix[i][j - 1])

    ans = longest_paths[rows_number - 1][columns_number - 1]
    print(ans)
    return ans


# Example test ----------------------------------------------
# down_matrix = [
#     [1, 0, 2, 4, 3],
#     [4, 6, 5, 2, 1],
#     [4, 4, 5, 2, 1],
#     [5, 6, 8, 5, 3,]
# ]

# right_matrix = [
#     [3, 2, 4, 0],
#     [3, 2, 4, 2],
#     [0, 7, 3, 3],
#     [3, 3, 0, 2],
#     [1, 3, 2, 2]
# ]

# ans = longest_path(down_matrix, right_matrix)
# assert(ans == 34)

# Debug test ----------------------------------------------
# f = open('./debug.txt')

# down_matrix = []
# right_matrix = []
# is_filled_down_matrix = False
# for line in f:
#     line = line.strip()
#     if "Input" in line:
#         continue
#     elif line == "-":
#         is_filled_down_matrix = True
#         continue
#     args = line.split()
#     if len(args) <= 2:
#         continue
#     elif not is_filled_down_matrix:
#         down_matrix.append([int(x) for x in args])
#     else:
#         right_matrix.append([int(x) for x in args])

# f.close()

# ans = longest_path(down_matrix, right_matrix)

# assert(ans == 84)

# Final test ----------------------------------------------
f = open('./test.txt')

down_matrix = []
right_matrix = []
is_filled_down_matrix = False
for line in f:
    line = line.strip()
    if line == "-":
        is_filled_down_matrix = True
        continue
    args = line.split()
    if len(args) <= 2:
        continue
    elif not is_filled_down_matrix:
        down_matrix.append([int(x) for x in args])
    else:
        right_matrix.append([int(x) for x in args])

f.close()

ans = longest_path(down_matrix, right_matrix)
pyperclip.copy(ans)
