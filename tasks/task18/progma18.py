#!/usr/bin/env python3

from typing import Dict, List
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

def is_spectrum_consistent(linear_spectrum: List[int], dict_cycle_spectrum: Dict[int, int]):
    copy_dict = dict_cycle_spectrum.copy()
    for x in linear_spectrum:
        if x not in copy_dict:
            return False
        copy_dict[x] -= 1
        if copy_dict[x] < 0:
            return False
    return True

def get_dict_cycle_spectrum(cycle_spectrum: List[int]):
    dict_cycle_spectrum = dict()
    for x in cycle_spectrum:
        if x in dict_cycle_spectrum:
            dict_cycle_spectrum[x] += 1
        else:
            dict_cycle_spectrum[x] = 1
    return dict_cycle_spectrum

def cyclospectrum(peptide: List[int]):
    peptide_size = len(peptide)
    cycle_peptide = peptide + peptide
    spectrum = [0]
    for i in range(1, peptide_size):
        for j in range(peptide_size):
            spectrum.append(sum(cycle_peptide[j:j + i]))
    spectrum.append(sum(peptide))
    return spectrum

def linear_spectrum(peptide: List[int]):
    peptide_size = len(peptide)
    spectrum = [0]
    for i in range(1, peptide_size):
        for j in range(peptide_size - i + 1):
            spectrum.append(sum(peptide[j:j + i]))
    spectrum.append(sum(peptide))
    return spectrum

def expand_candidates(candidates: List[List[int]]):
    next_candidates = []
    for x in candidates:
        for acid in AMINO_ACIDS:
            next_candidates.append(x + [acid])
    return next_candidates

def are_spectrums_equals(spectrum1: List[int], spectrum2: List[int]):
    return SEPARATOR.join([str(x) for x in sorted(spectrum1)]) == SEPARATOR.join([str(x) for x in sorted(spectrum2)])

def peptide_to_str(peptide: List[int]):
    return SEPARATOR.join([str(x) for x in peptide])

def str_to_peptide(string: str):
    return [int(x) for x in string.split(SEPARATOR)]

def cyclopeptid_sequencing(spectrum: List[int]):
    candidate_peptides = [[]]
    final_peptides = set()
    dict_cycle_spectrum = get_dict_cycle_spectrum(spectrum)
    while len(candidate_peptides) != 0:
        candidate_peptides = expand_candidates(candidate_peptides)
        cadidates_to_remove = []
        
        for peptide in candidate_peptides:
            if peptide_mass(peptide) == parent_mass(spectrum):
                cycled_spectrum = cyclospectrum(peptide)
                if are_spectrums_equals(cycled_spectrum, spectrum):
                    final_peptides.add(peptide_to_str(peptide))
                
                cadidates_to_remove.append(peptide)
            elif not is_spectrum_consistent(linear_spectrum(peptide), dict_cycle_spectrum):
                cadidates_to_remove.append(peptide)
        
        for candidate_to_remove in cadidates_to_remove:
            candidate_peptides.remove(candidate_to_remove)

    return final_peptides

def main(spectrum: List[int]):
    peptides = cyclopeptid_sequencing(spectrum)
    res = ' '.join(peptides)
    print(res)
    return res


# Example test ----------------------------------------------
# spectrum = [0, 113, 128, 186, 241, 299, 314, 427]
# ans = main(spectrum)

# true_ans = '186-128-113 186-113-128 128-186-113 128-113-186 113-186-128 113-128-186'
# assert(' '.join(sorted(ans.split(' '))) == ' '.join(sorted(true_ans.split(' '))))

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()

# output_idx = data.index('Output')
# spectrum = [int(x) for x in data[1:output_idx]]
# true_ans = sorted(data[output_idx + 1:])

# ans = main(spectrum)

# assert(' '.join(sorted(ans.split(' '))) == ' '.join(true_ans))

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()

spectrum = [int(x) for x in data]

ans = main(spectrum)

pyperclip.copy(ans)
