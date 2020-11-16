
#! /usr/bin/env python3

import pyperclip


def get_distance(str1, str2):
    if len(str1) != len(str2):
        raise Exception('Two string have different lengths')
    return sum([letter1 != letter2 for letter1, letter2 in zip(str1, str2)])


def get_occurrences_positions(pattern, test_str, max_d):
    ans = list()
    pattern_len = len(pattern)
    test_str_len = len(test_str)
    for pointer in range(test_str_len):
        if pointer + pattern_len > test_str_len:
            return ans
        word = test_str[pointer:pointer + pattern_len]
        if get_distance(word, pattern) <= max_d:
            ans.append(pointer)
    return ans


f = open('approximate_occurrences/rosalind_ba1h.txt')
data = f.read().split()
ans = get_occurrences_positions(
    pattern=data[0],
    test_str=data[1],
    max_d=int(data[2])
)
# For test dataset
# right_str = ' '.join(data[5:])
# our_str = ' '.join(str(x) for x in ans)
# assert right_str == our_str
pyperclip.copy(' '.join(str(x) for x in ans))
f.close()
