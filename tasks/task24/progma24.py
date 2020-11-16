#! /usr/bin/env python3

from typing import Tuple
import numpy as np
import pyperclip

SKIP_LETTER = "-"
LETTERS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
# read score matrix from file
SCORE_MATRIX = np.loadtxt("./scoring_matrix", dtype=int)
SIGMA = 5

def get_score(letter1: str, letter2: str) -> int:
    if letter1 == SKIP_LETTER or letter2 == SKIP_LETTER:
        return -SIGMA
    else:
        letter1_idx = LETTERS.index(letter1)
        letter2_idx = LETTERS.index(letter2)

        return SCORE_MATRIX[letter1_idx, letter2_idx]

def get_score_of_strings(str1: str, str2: str) -> int:
    ans = 0
    pairs = zip(list(str1), list(str2))
    for pair in pairs:
        ans += get_score(pair[0], pair[1])
    return ans

def find_LCS(seq1: str, seq2: str) -> Tuple[int, str, str]:
    res_seq1 = []
    res_seq2 = []
    if len(seq1) > len(seq2):
        seq1, seq2 = seq2, seq1
    columns_count = len(seq1) + 1
    rows_count = len(seq2) + 1
    current_score = [[0] * columns_count for _ in range(rows_count)]
    
    # fill first column
    for i in range(1, rows_count):
        current_score[i][0] = current_score[i - 1][0] - SIGMA
    # fill first row
    for i in range(1, columns_count):
        current_score[0][i] = current_score[0][i - 1] - SIGMA
    
    # fill rest matrix
    for i in range(1, rows_count):
        for j in range(1, columns_count):
            current_score[i][j] = max(
                0,
                current_score[i - 1][j] - SIGMA,
                current_score[i][j - 1] - SIGMA,
                current_score[i - 1][j - 1] + get_score(seq1[j - 1], seq2[i - 1])
            )
    
    # find sink
    sink = (0, 0)
    for i in range(rows_count):
        for j in range(columns_count):
            if current_score[i][j] > current_score[sink[0]][sink[1]]:
                sink = (i, j)
    current_score[rows_count - 1][columns_count - 1] = current_score[sink[0]][sink[1]]

    # get seq-es
    i, j = sink
    while i != 0 or j != 0:
        if j == 0 or current_score[i][j] + SIGMA == current_score[i - 1][j]:
            # deletion -> up
            res_seq1.append(SKIP_LETTER)
            res_seq2.append(seq2[i - 1])
            i -= 1
        elif i == 0 or current_score[i][j] + SIGMA == current_score[i][j - 1]:
            # insertion -> left
            res_seq1.append(seq1[j - 1])
            res_seq2.append(SKIP_LETTER)
            j -= 1
        elif current_score[i][j] - get_score(seq1[j - 1], seq2[i - 1]) == current_score[i - 1][j - 1]:
            res_seq1.append(seq1[j - 1])
            res_seq2.append(seq2[i - 1])
            i -= 1
            j -= 1
        else:
            break

    score = current_score[rows_count - 1][columns_count - 1]
    res_seq1.reverse()
    res_seq2.reverse()
    ans_str1 = ''.join(res_seq1)
    ans_str2 = ''.join(res_seq2)
    print(score)
    print(ans_str1)
    print(ans_str2)
    assert(get_score_of_strings(ans_str1, ans_str2) == score)

    return (score, ans_str1, ans_str2)


# Example test ----------------------------------------------
# str1 = "MEANLY"
# str2 = "PENALTY"
# find_LCS(str1, str2)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()
# score, _, _ = find_LCS(data[1], data[2])

# assert(score == int(data[4]))

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()
score, str1, str2 = find_LCS(data[0], data[1])
pyperclip.copy("\n".join([str(score), str1, str2]))
