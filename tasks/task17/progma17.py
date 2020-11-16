#!/usr/bin/env python3

import pyperclip
from functools import reduce
from math import factorial

numbers_set = [
    57, 71, 87, 97, 99,
    101, 103, 113, 114, 115,
    128, 129, 131, 137, 147, 
    156, 163, 186
]

def calculate_multinomial_coef(arr):
    n = sum(arr)
    return int(reduce(lambda prev, curr: prev / factorial(curr), arr, factorial(n)))

def main(target):
    numbers_count = len(numbers_set)
    dp = [[[0] * numbers_count]] + [[] for _ in range(target)]
    for i in range(numbers_count):
        for j in range(target - numbers_set[i] + 1):
            for arr in dp[j]:
                tmp = arr.copy()
                tmp[i] += 1
                dp[j + numbers_set[i]].append(tmp)
    
    ans = 0
    for arr in dp[target]:
        ans += calculate_multinomial_coef(arr)
    print(ans)
    return ans



# Example test ----------------------------------------------
# assert(main(1024) == 14712706211)

# Debug test ----------------------------------------------
# assert(main(1307) == 34544458837656)

# Final test
main(1212)
