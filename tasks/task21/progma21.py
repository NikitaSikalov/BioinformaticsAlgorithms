#!/usr/bin/env python3

from typing import List
import math
import pyperclip


def min_number_with_particular_sum(seq: List[int], N: int) -> int:
    counts = [math.inf] * (N + 1)
    for n in seq:
        if n > N:
            continue
        counts[n] = 1
    
    for n in seq:
        for i in range(N + 1 - n):
            counts[i + n] = min(counts[i] + 1, counts[i + n])
    
    ans = counts[N]
    print(ans)
    return ans

# Example test ----------------------------------------------
# N = 40
# seq = [1, 5, 10, 20, 25, 50]
# ans = min_number_with_particular_sum(seq, N)

# assert(ans == 2)

# Debug test ----------------------------------------------
# N = 8074
# seq = [24, 13, 12, 7, 5, 3, 1]
# ans = min_number_with_particular_sum(seq, N)

# assert(ans == 338)

# Final test ----------------------------------------------
N = 16062
seq = [1, 3, 5, 16]
ans = min_number_with_particular_sum(seq, N)

pyperclip.copy(ans)
