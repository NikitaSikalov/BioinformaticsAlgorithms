import pyperclip
from operator import itemgetter


def get_distance(str1, str2):
    """Сalculate distance betwreen strings"""
    if len(str1) != len(str2):
        raise Exception('Two string have different lengths')
    return sum([letter1 != letter2 for letter1, letter2 in zip(str1, str2)])


def get_all_substrings(s, k):
    """Get all substrings length k from string s

    Args:
        s (str): test string
        k (int): length of substring
    """
    return [s[ptr:ptr + k] for ptr in range(len(s) - k + 1)]


ALPHABET = ['A', 'T', 'G', 'C']


def form_profile(strings):
    """Calculate profile matrix for array of strings

    Args:
        strings (str[]): strings set

    Returns:
        dict: profile matrix
    """
    profile = dict(zip(ALPHABET, map(lambda _: list(), ALPHABET)))
    if len(strings) < 1:
        return profile
    columns_number = len(strings[0])
    row_numbers = len(strings)
    for column in range(columns_number):
        column_profile = dict.fromkeys(ALPHABET, 1 / row_numbers)
        for row in strings:
            letter = list(row)[column]
            column_profile[letter] += 1 / row_numbers
        for letter in ALPHABET:
            profile[letter].append(column_profile[letter])
    return profile


def get_most_probable_word(profile):
    ans = list()
    profile_values = list(profile.values())
    if len(profile_values) == 0:
        return ''
    columns_number = len(profile_values[0])
    for column in range(columns_number):
        tmp_max = 0
        choosing_letter = ALPHABET[0]
        for letter in ALPHABET:
            letter_prob = profile.get(letter, [0] * columns_number)[column]
            if letter_prob > tmp_max:
                tmp_max = letter_prob
                choosing_letter = letter
        ans.append(choosing_letter)
    return ''.join(ans)


def get_word_prob(profile, word):
    columns_number = len(word)
    probe = 1
    for column in range(columns_number):
        letter = word[column]
        probe *= profile.get(letter, [0] * columns_number)[column]
    return probe


def most_probable_word_from_str(profile, string, k):
    """Get most probable substring with length k via progile matrix"""
    return max(map(
        lambda s: (s, get_word_prob(profile, s)),
        get_all_substrings(string, k)),
        key=itemgetter(1)
    )[0]


def get_score_from_matif_matrix(matif_matrix):
    profile = form_profile(matif_matrix)
    most_prob_word = get_most_probable_word(profile)
    ans = 0
    for matif in matif_matrix:
        ans += get_distance(matif, most_prob_word)
    return ans


def greedy_motif_search(Dna, k, t):
    best_motifs = list()
    min_score = t * k
    if len(Dna) == 0:
        return best_motifs
    if t != len(Dna):
        raise TypeError(
            'Number of strings in Dna {} not equal t {}'.format(len(Dna), t)
        )
    motifs = [None] * t
    for motif in get_all_substrings(Dna[0], k):
        motifs[0] = motif
        for row in range(1, t):
            profile = form_profile([s for s in motifs[0:row]])
            motifs[row] = most_probable_word_from_str(profile, Dna[row], k)
        score = get_score_from_matif_matrix(motifs)
        if score < min_score:
            min_score = score
            best_motifs = motifs.copy()
    return best_motifs


f = open('task7/rosalind_ba2e.txt')
data = f.read().split()
res = greedy_motif_search(
    Dna=data[2:],
    k=int(data[0]),
    t=int(data[1])
)
print('\n'.join(res))
pyperclip.copy('\n'.join(res))
f.close()
