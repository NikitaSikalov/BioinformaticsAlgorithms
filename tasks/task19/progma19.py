#!/usr/bin/env python3

from typing import Dict, List, Tuple
import pyperclip


AMINO_ACIDS = [
    57, 71, 87, 97,
    99, 101, 103, 113,
    114, 115, 128, 129,
    131, 137, 147, 156,
    163, 186
]

SEPARATOR = '-'

def parent_mass(spectrum: List[int]):
    return max(spectrum)

def peptide_mass(peptide: List[int]):
    return sum(peptide)

def get_dict_cycle_spectrum(cycle_spectrum: List[int]):
    dict_cycle_spectrum = dict()
    for x in cycle_spectrum:
        if x in dict_cycle_spectrum:
            dict_cycle_spectrum[x] += 1
        else:
            dict_cycle_spectrum[x] = 1
    return dict_cycle_spectrum

def linear_spectrum(peptide: List[int]):
    peptide_size = len(peptide)
    spectrum = [0]
    for i in range(1, peptide_size):
        for j in range(peptide_size - i + 1):
            spectrum.append(sum(peptide[j:j + i]))
    spectrum.append(sum(peptide))
    return spectrum

def cyclospectrum(peptide: List[int]):
    peptide_size = len(peptide)
    cycle_peptide = peptide + peptide
    spectrum = [0]
    for i in range(1, peptide_size):
        for j in range(peptide_size):
            spectrum.append(sum(cycle_peptide[j:j + i]))
    spectrum.append(sum(peptide))
    return spectrum

def get_score(peptide: List[int], dict_cycle_spectrum: Dict[int, int]):
    peptide_spectrum = cyclospectrum(peptide)
    copied_dict = dict_cycle_spectrum.copy()
    score = 0
    for amino in peptide_spectrum:
        if amino in copied_dict and copied_dict[amino] >= 1:
            copied_dict[amino] -= 1
            score += 1
    return score

def trim_leaderboard(leaderboard: List[Tuple[int, List[int]]], N: int):
    if len(leaderboard) == 0:
        return leaderboard
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[0], reverse=True)
    cut_index = min(N, len(sorted_leaderboard))
    cut_score = sorted_leaderboard[cut_index - 1][0]
    return filter(lambda x: x[0] >= cut_score, leaderboard)

def expand_candidates(candidates: List[Tuple[int, List[int]]], dict_cycle_spectrum: Dict[int, int]) -> List[Tuple[int, List[int]]]:
    next_candidates = []
    for _, peptide in candidates:
        for acid in AMINO_ACIDS:
            candidate_to_append = peptide + [acid]
            score = get_score(candidate_to_append, dict_cycle_spectrum)
            next_candidates.append((score, candidate_to_append))
    return next_candidates

def peptide_to_str(peptide: List[int]):
    return SEPARATOR.join([str(x) for x in peptide])

def leaderboard_cyclopeptid_sequencing(N: int, spectrum: List[int]):
    leaderboard: List[Tuple[int, List[int]]] = [(0, [])]
    leader_peptides = []
    leader_score = None
    dict_cycle_spectrum = get_dict_cycle_spectrum(spectrum)
    while len(leaderboard) != 0:
        leaderboard = expand_candidates(leaderboard, dict_cycle_spectrum)
        peptides_to_remove = []
        
        for score, peptide in leaderboard:
            if peptide_mass(peptide) == parent_mass(spectrum):
                if leader_score is None or score > leader_score:
                    leader_peptides = [peptide.copy()]
                    leader_score = score
                elif score == leader_score:
                    leader_peptides.append(peptide.copy())
            elif peptide_mass(peptide) > parent_mass(spectrum):
                peptides_to_remove.append(peptide)
            
        leaderboard = list(filter(lambda x: x[1] not in peptides_to_remove, leaderboard))
        leaderboard = list(trim_leaderboard(leaderboard, N))

    print('leader_score: ', leader_score)
    return leader_peptides

def main(N: int, spectrum: List[int]):
    peptides = leaderboard_cyclopeptid_sequencing(N, spectrum)
    res = []
    for peptide in peptides:
        tmp = peptide_to_str(peptide)
        print(tmp)
        res.append(tmp)
    return res


# Example test ----------------------------------------------
# spectrum = [0, 71, 113, 129, 147, 200, 218, 260, 313, 331, 347, 389, 460]
# N = 10
# ans = main(N=N, spectrum=spectrum)

# true_ans = '113-147-71-129'
# assert(true_ans in ans)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()

# output_idx = data.index('Output:')
# N = int(data[1]) + 200
# print('N:', N)
# spectrum = [int(x) for x in data[2:output_idx]]
# true_ans = data[output_idx + 1]

# ans = main(N=N, spectrum=spectrum)

# dict_cycle_spectrum = get_dict_cycle_spectrum(spectrum)
# true_peptide = [int(x) for x in true_ans.split(SEPARATOR)]
# true_ans_score = get_score(true_peptide, dict_cycle_spectrum)

# print('true score: ', true_ans_score)

# assert(true_ans in ans)

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()

N = int(data[0])
spectrum = [int(x) for x in data[1:]]

ans = main(N=N, spectrum=spectrum)

pyperclip.copy(ans[0])
