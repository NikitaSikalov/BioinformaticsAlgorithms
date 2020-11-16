import pyperclip


def get_all_substrings(s, k):
    """Get all substrings length k from string s

    Args:
        s (str): test string
        k (int): length of substring
    """
    return [s[ptr:ptr + k] for ptr in range(len(s) - k + 1)]


def get_distance(str1, str2):
    """Сalculate distance betwreen strings"""
    if len(str1) != len(str2):
        raise Exception('Two string have different lengths')
    return sum([letter1 != letter2 for letter1, letter2 in zip(str1, str2)])


def distance_between_pattern_and_strings(pattern, dna):
    k = len(pattern)
    distance = 0
    for text in dna:
        hamming_distance = k
        for substring in get_all_substrings(text, k):
            d = get_distance(pattern, substring)
            if d < hamming_distance:
                hamming_distance = d
        distance += hamming_distance
    return distance


# test_dna = [
#     "AAATTTT",
#     "AAACCCC",
#     "AAAGGGG"
# ]
# test_pattern = "AAA"

f = open('task10/test.txt')
data = f.read().split()
res = distance_between_pattern_and_strings(
    dna=data[1:],
    pattern=data[0],
)
print(res)
pyperclip.copy(res)
f.close()
