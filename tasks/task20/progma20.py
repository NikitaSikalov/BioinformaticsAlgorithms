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

def expand_candidates(candidates: List[Tuple[int, List[int]]], dict_cycle_spectrum: Dict[int, int], amino_acids = AMINO_ACIDS) -> List[Tuple[int, List[int]]]:
    next_candidates = []
    for _, peptide in candidates:
        for acid in amino_acids:
            candidate_to_append = peptide + [acid]
            score = get_score(candidate_to_append, dict_cycle_spectrum)
            next_candidates.append((score, candidate_to_append))
    return next_candidates

def get_amino_acids(M: int, spectrum: List[int]) -> List[int]:
    upper_bound = 200
    lower_bound = 57
    convolution = [0] * (upper_bound + 1)
    spectrum_with_zero = spectrum + [0]
    for x in spectrum_with_zero:
        for y in spectrum_with_zero:
            if y - x >= 0 and y - x <= upper_bound:
                convolution[y - x] += 1
    
    convolution_pairs = list(enumerate(convolution))
    convolution_pairs = list(filter(lambda x: x[0] <= upper_bound and x[0] >= lower_bound, convolution_pairs))
    convolution_pairs.sort(key=lambda x: x[1], reverse=True)
    
    cut_value = convolution_pairs[M - 1][1]
    convolution_pairs = filter(lambda x: x[1] >= cut_value, convolution_pairs)
    return [pair[0] for pair in convolution_pairs]

def peptide_to_str(peptide: List[int]):
    return SEPARATOR.join([str(x) for x in peptide])

def leaderboard_cyclopeptid_sequencing(N: int, M:int, spectrum: List[int]):
    amino_acids = get_amino_acids(M, spectrum)

    leaderboard: List[Tuple[int, List[int]]] = [(0, [])]
    leader_peptides = []
    leader_score = None
    dict_cycle_spectrum = get_dict_cycle_spectrum(spectrum)
    while len(leaderboard) != 0:
        leaderboard = expand_candidates(leaderboard, dict_cycle_spectrum, amino_acids)
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

def main(N: int, M: int, spectrum: List[int]):
    peptides = leaderboard_cyclopeptid_sequencing(N, M, spectrum)
    res = []
    for peptide in peptides:
        tmp = peptide_to_str(peptide)
        print(tmp)
        res.append(tmp)
    return res


# Example test ----------------------------------------------
# M = 20
# N = 60
# spectrum = [57, 57, 71, 99, 129, 137, 170, 186, 194, 208, 228, 265, 285, 299, 307, 323, 356, 364, 394, 422, 493]
# ans = main(N=N, M=M,spectrum=spectrum)

# true_ans = '99-71-137-57-72-57'
# assert(true_ans in ans)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()

# output_idx = data.index('Output:')
# M = int(data[1])
# N = int(data[2])
# spectrum = [int(x) for x in data[2:output_idx]]
# true_ans = data[output_idx + 1]

# ans = main(N=N, M=M, spectrum=spectrum)

# dict_cycle_spectrum = get_dict_cycle_spectrum(spectrum)
# true_peptide = [int(x) for x in true_ans.split(SEPARATOR)]
# true_ans_score = get_score(true_peptide, dict_cycle_spectrum)

# print('true score: ', true_ans_score)

# assert(true_ans in ans)

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()

M = int(data[0])
N = int(data[1])
spectrum = [int(x) for x in data[2:]]

ans = main(N=N, M=M, spectrum=spectrum)

pyperclip.copy(ans[0])
