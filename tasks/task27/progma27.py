#! /usr/bin/env python3 

import re
from typing import List
import pyperclip

def get_number_of_breakpoints(arr: List[int]) -> int:
    tmp = [0] + arr + [len(arr) + 1]
    ans = 0
    # print(tmp)
    for i in range(1, len(tmp)):
        ans += int(tmp[i] - tmp[i - 1] != 1)
        # if tmp[i] - tmp[i - 1] == 1:
            # print("%d %d" % (tmp[i], tmp[i - 1]))
    print(ans)
    return ans

def prepare_arr(sample: str):
    patterns = re.split(r'[()\s]', sample)
    patterns = filter(lambda x: bool(x), patterns)
    return [int(x) for x in patterns]

def main(sample: str) -> int:
    arr = prepare_arr(sample)
    return get_number_of_breakpoints(arr)


# Example test ----------------------------------------------
# sample = "(+3 +4 +5 -12 -8 -7 -6 +1 +2 +10 +9 -11 +13 +14)"
# main(sample)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split("\n")
# f.close()

# main(data[1])

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split("\n")
f.close()

ans = main(data[0])

pyperclip.copy(ans)
