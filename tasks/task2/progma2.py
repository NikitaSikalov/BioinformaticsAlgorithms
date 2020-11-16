#! /usr/bin/env python3

def get_skew_positions(test_str):
    min_skew = None
    prefix_skew = [0]
    for letter in test_str:
        if letter == 'G':
            prefix_skew.append(prefix_skew[-1] + 1)
        elif letter == 'C':
            prefix_skew.append(prefix_skew[-1] - 1)
        else:
            prefix_skew.append(prefix_skew[-1])
        if min_skew is None or prefix_skew[-1] < min_skew:
            min_skew = prefix_skew[-1]
    return [i for i in range(len(prefix_skew)) if prefix_skew[i] == min_skew]


f = open('./test.txt')
file_data = f.read()
test_str = file_data.split()[0]
ans = get_skew_positions(test_str)
print(" ".join(str(x) for x in ans))
f.close()
