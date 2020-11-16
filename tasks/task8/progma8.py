import random
import pyperclip
from operator import itemgetter


ALPHABET = ['A', 'T', 'G', 'C']


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


def get_word_prob(profile, word):
    columns_number = len(word)
    probe = 1
    for column in range(columns_number):
        letter = word[column]
        probe *= profile.get(letter, [0] * columns_number)[column]
    return probe


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


def get_motifs_from_profile(profile, Dna, k):
    motifs = list()
    for row_string in Dna:
        motifs.append(most_probable_word_from_str(profile, row_string, k))
    return motifs


def randomized_motif_search(Dna, k, t):
    random_sets = list()
    ITERATIONS_NUMBER = 400
    for row_str in Dna:
        words = get_all_substrings(row_str, k)
        random_sets.append(random.choices(words, k=ITERATIONS_NUMBER))
    global_best_motifs = list()
    global_min_score = k * t
    for next_random_motifs in map(list, zip(*random_sets)):
        best_motifs = next_random_motifs.copy()
        motifs = best_motifs.copy()
        min_score = get_score_from_matif_matrix(best_motifs)
        while True:
            profile = form_profile(motifs)
            motifs = get_motifs_from_profile(profile, Dna, k)
            score = get_score_from_matif_matrix(motifs)
            if score < min_score:
                min_score = score
                best_motifs = motifs.copy()
            else:
                if min_score < global_min_score or min_score == global_min_score and Dna[0].index(best_motifs[0]) < Dna[0].index(global_best_motifs[0]):
                    global_best_motifs = best_motifs.copy()
                    global_min_score = min_score
                    print('score: ', global_min_score)
                break
    return global_best_motifs


f = open('task8/rosalind_ba2f.txt')
data = f.read().split()
res = randomized_motif_search(
    Dna=data[2:],
    k=int(data[0]),
    t=int(data[1])
)
print('\n'.join(res))
pyperclip.copy('\n'.join(res))
f.close()
