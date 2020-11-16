#! /usr/bin/env python3

from typing import Tuple
import numpy as np
import pyperclip

SKIP_LETTER = "-"

def get_score(letter1: str, letter2: str, letter3: str) -> int:
    if SKIP_LETTER in (letter1, letter2, letter3):
        return 0
    else:
        return int(letter1 == letter2 and letter3 == letter2)

def get_score_of_strings(str1: str, str2: str, str3: str) -> int:
    ans = 0
    triples = zip(list(str1), list(str2), list(str3))
    for triple in triples:
        ans += get_score(triple[0], triple[1], triple[2])
    return ans

def find_LCS(seq1: str, seq2: str, seq3: str) -> Tuple[int, str, str, str]:
    res_seq1, res_seq2, res_seq3 = [], [], []
    dim1, dim2, dim3 = len(seq1) + 1, len(seq2) + 1, len(seq3) + 1
    current_score = np.zeros((dim1, dim2, dim3), dtype=int)
    
    # fill rest matrix
    for i in range(1, dim1):
        for j in range(1, dim2):
            for k in range(1, dim3):
                current_score[i, j, k] = max(
                    current_score[i - 1, j, k],
                    current_score[i, j - 1, k],
                    current_score[i, j, k - 1],
                    current_score[i - 1, j - 1, k],
                    current_score[i - 1, j, k - 1],
                    current_score[i, j - 1, k - 1],
                    current_score[i - 1, j - 1, k - 1] + get_score(seq1[i - 1], seq2[j - 1], seq3[k - 1])
                )
    
    # get seq-es
    i, j, k = dim1 - 1, dim2 - 1, dim3 - 1
    while i != 0 or j != 0 or k != 0:
        if i > 0 and j > 0 and k > 0 \
            and current_score[i - 1, j - 1, k - 1] + get_score(seq1[i - 1], seq2[j - 1], seq3[k - 1]) == current_score[i, j, k]:
            res_seq1.append(seq1[i - 1])
            res_seq2.append(seq2[j - 1])
            res_seq3.append(seq3[k - 1])
            i -= 1
            j -= 1
            k -= 1
            continue
        idx_seq = [
            (max(i - 1, 0), j, k),
            (i, max(j - 1, 0), k),
            (i, j, max(k - 1, 0)),
            (max(i - 1, 0), max(j - 1, 0), k),
            (max(i - 1, 0), j, max(k - 1, 0)),
            (i, max(j - 1, 0), max(k - 1, 0))
        ]
        idx_seq = list(filter(lambda seq: seq[0] != i or seq[1] != j or seq[2] != k, idx_seq))
        for idx in idx_seq:
            if current_score[idx] == current_score[i, j, k]:
                I, J, K = idx
                x1 = seq1[I] if I != i else SKIP_LETTER
                x2 = seq2[J] if J != j else SKIP_LETTER
                x3 = seq3[K] if K != k else SKIP_LETTER
                res_seq1.append(x1)
                res_seq2.append(x2)
                res_seq3.append(x3)
                i, j, k = I, J, K
                break

    score = current_score[dim1 - 1, dim2 - 1, dim3 - 1]
    res_seq1.reverse()
    res_seq2.reverse()
    res_seq3.reverse()
    ans_str1 = ''.join(res_seq1)
    ans_str2 = ''.join(res_seq2)
    ans_str3 = ''.join(res_seq3)
    print(score)
    print(ans_str1)
    print(ans_str2)
    print(ans_str3)
    assert(get_score_of_strings(ans_str1, ans_str2, ans_str3) == score)

    return (score, ans_str1, ans_str2, ans_str3)


# Example test ----------------------------------------------
# str1 = "ATATCCG"
# str2 = "TCCGA"
# str3 = "ATGTACTG"
# find_LCS(str1, str2, str3)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()
# score, _, _ = find_LCS(data[1], data[2], data[3])

# assert(score == int(data[5]))

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()
score, str1, str2, str3 = find_LCS(data[0], data[1], data[2])
pyperclip.copy("\n".join([str(score), str1, str2, str3]))
