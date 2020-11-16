#! /usr/bin/env python3

import pyperclip


def get_reverse_complement_word(word):
    complemetory_table = dict(
        A='T',
        G='C',
        C='G',
        T='A'
    )
    word_list = list(word)
    word_list.reverse()
    complementory_word_list = map(lambda x: complemetory_table[x], word_list)
    return ''.join(complementory_word_list)


def get_all_variants(word, start, depth):
    letters = ['A', 'G', 'C', 'T']
    res = list()
    for i in range(start + 1, len(word)):
        splited_word = list(word)
        for letter in letters:
            splited_word[i] = letter
            new_word = ''.join(splited_word)
            res.append(new_word)
            if depth != 1:
                res.extend(get_all_variants(new_word, i, depth - 1))
    return list(set(res))


def similar_words(word, max_d):
    if max_d == 0:
        return [word]
    return get_all_variants(word, -1, max_d)


def get_frequent_words(test_str, k, max_d):
    hash = dict()
    frequent_words = set()
    max_count = 0
    for pointer in range(k, len(test_str) + 1):
        word = test_str[pointer - k:pointer]
        same_words = similar_words(word, max_d)
        complementory_word = get_reverse_complement_word(word)
        same_words.extend(similar_words(complementory_word, max_d))
        for similar_word in same_words:
            hash[similar_word] = hash.get(similar_word, 0) + 1
            if hash[similar_word] == max_count:
                frequent_words.add(similar_word)
            elif hash[similar_word] > max_count:
                max_count = hash[similar_word]
                frequent_words.clear()
                frequent_words.add(similar_word)
    return list(frequent_words)


f = open('./test.txt')
data = f.read().split()
ans = get_frequent_words(
    test_str=data[0],
    k=int(data[1]),
    max_d=int(data[2])
)
pyperclip.copy(' '.join(ans))
print(' '.join(ans))
f.close()
