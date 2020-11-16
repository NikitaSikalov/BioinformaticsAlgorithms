#! /usr/bin/env python3

# Given: A string Genome, and integers k, L, and t.
# Return: All distinct k-mers forming (L, t)-clumps in Genome.

# Example

# Input
# CGGACTCGACAGATGTGAAGAAATGTGAAGACTGAGTGAAGAGAAGAGGAAACACGACACGACATTGCGACATAATGTACGAATGTAATGTGCCTATGGC
# 5 75 4

# Output
# CGACA GAAGA AATGT

def get_clumps(k, L, t, str):
    # создаем массив ответов
    ans = set()
    if len(str) < k:
        return list(ans)
    # формируем hash таблицу, ключи которой будут
    # подпоследовательности длины k, а значениями кол-во повторений
    # этой подпоследовательности в текущем окне длины L
    hash = dict()
    pointer = 0
    # формируем hash таблицу для начального окна длины L
    for pointer in range(L):
        word = str[pointer:pointer + k]
        hash[word] = hash.get(word, 0) + 1
        if hash[word] == t:
            ans.add(word)
    start_word = str[:k]
    last_word = str[L - k:L]
    # итерируемся до конца строки
    for pointer in range(L, len(str)):
        added_word = str[pointer - k:pointer]
        removed_word = str[pointer - L:pointer - L + k]
        hash[removed_word] = hash[removed_word] - 1
        hash[added_word] = hash.get(added_word, 0) + 1
        if hash[added_word] == t:
            ans.add(added_word)
    return list(ans)


f = open('test.txt')
file_data = f.read()
splited_data = file_data.split()
arr = get_clumps(
    k=int(splited_data[1]),
    L=int(splited_data[2]),
    t=int(splited_data[3]),
    str=splited_data[0]
)
print(' '.join(arr))
