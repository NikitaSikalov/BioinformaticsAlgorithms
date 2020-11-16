#! /usr/bin/env python3

from typing import List
import re
import pyperclip

def permutation_to_str(arr: List[int]):
    return "(" + ' '.join(["+" + str(x) if x > 0 else str(x) for x in arr]) + ")"

def gridy_reversal_permutation(arr: List[int]):
    pointer = 0
    n = len(arr)
    permuations = []
    tmp = arr.copy()
    while pointer != n:
        if tmp[pointer] != pointer + 1:
            j = pointer
            while abs(tmp[j]) != pointer + 1:
                j += 1
            tmp = tmp[:pointer] + [-x for x in reversed(tmp[pointer:j + 1])] + (tmp[j + 1:] if j + 1 < n else [])
            permuations.append(tmp)
        else:
            pointer += 1   
    
    for i in range(n):
        assert(permuations[-1][i] == i + 1)
    ans = "\n".join([permutation_to_str(permutation) for permutation in permuations])
    print(ans)
    return ans

def prepare_arr(s: str):
    patterns = re.split(r'[()\s]', s)
    patterns = filter(lambda x: bool(x), patterns)
    return [int(x) for x in patterns]

def main(s: str):
    arr = prepare_arr(s)
    return gridy_reversal_permutation(arr)

# Example test ----------------------------------------------
# sample = '(-3 +4 +1 +5 -2)'
# ans = main(sample)

# true_ans = "(-1 -4 +3 +5 -2)\n(+1 -4 +3 +5 -2)\n(+1 +2 -5 -3 +4)\n(+1 +2 +3 +5 +4)\n(+1 +2 +3 -4 -5)\n(+1 +2 +3 +4 -5)\n(+1 +2 +3 +4 +5)"
# assert(ans == true_ans)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split("\n")
# f.close()

# ans = main(data[1])

# true_ans = "\n".join(data[3:]).strip()

# assert(ans == true_ans)

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split("\n")
f.close()

ans = main(data[0])

pyperclip.copy(ans)
