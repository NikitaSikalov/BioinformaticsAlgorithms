#!/usr/bin/env python3

import pyperclip

def get_amin_from_dna_pattern(dna_pattern):
    assert(len(dna_pattern) % 3 == 0)

    rna_pattern = ''.join([letter if letter != 'T' else 'U' for letter in dna_pattern])
    RnaCodonToAminDict = dict(
        AAA='K', AAC='N', AAG='K', AAU='N',
        ACA='T', ACC='T', ACG='T', ACU='T',
        AGA='R', AGC='S', AGG='R', AGU='S',
        AUA='I', AUC='I', AUG='M', AUU='I',

        CAA='Q', CAC='H', CAG='Q', CAU='H',
        CCA='P', CCC='P', CCG='P', CCU='P',
        CGA='R', CGC='R', CGG='R', CGU='R', 
        CUA='L', CUC='L', CUG='L', CUU='L',
        
        GAA='E', GAC='D', GAG='E', GAU='D',
        GCA='A', GCC='A', GCG='A', GCU='A',
        GGA='G', GGC='G', GGG='G', GGU='G',
        GUA='V', GUC='V', GUG='V', GUU='V',
        
        UAA='*', UAC='Y', UAG='*', UAU='Y',
        UCA='S', UCC='S', UCG='S', UCU='S',
        UGA='*', UGC='C', UGG='W', UGU='C',
        UUA='L', UUC='F', UUG='L', UUU='F'
    )
    return ''.join([RnaCodonToAminDict[rna_pattern[i:i+3]] for i in range(0, len(rna_pattern), 3)])

def get_all_substrings(s, k):
    return [s[ptr:ptr + k] for ptr in range(len(s) - k + 1)]

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


def main(text, amin_acid):
    k = 3 * len(amin_acid)

    res = []
    for dna_pattern in get_all_substrings(s=text, k=k):
        if amin_acid == get_amin_from_dna_pattern(dna_pattern):
            res.append(dna_pattern)
            continue
        complementory_dna_pattern = get_reverse_complement_word(dna_pattern)
        if amin_acid == get_amin_from_dna_pattern(complementory_dna_pattern):
            res.append(dna_pattern)
    
    res.sort()
    print('\n'.join(res))
    return '\n'.join(res)
    

# Example test ----------------------------------------------
# Text = 'ATGGCCATGGCCCCCAGAACTGAGATCAATAGTACCCGTATTAACGGGTGA
# amin = 'MA
# ans = main(Text, amin)

# true_ans = 'ATGGCC\nGGCCAT\nATGGCC'
# assert(ans == true_ans)

# Debug test ----------------------------------------------
# f = open('./debug.txt')
# data = f.read().split()
# f.close()

# ans = main(text=data[1], amin_acid=data[2])

# true_ans = '\n'.join(sorted(data[4:]))

# assert(len(ans) == len(true_ans))
# assert(ans == true_ans)

# Final test ----------------------------------------------
f = open('./test.txt')
data = f.read().split()
f.close()

ans = main(text=data[0], amin_acid=data[1])
print(ans)

pyperclip.copy(ans)
