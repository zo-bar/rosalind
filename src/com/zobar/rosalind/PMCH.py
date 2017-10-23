'''
Created on Aug 12, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
import math

def PMCH(input_file, output_file):
    dna = get_fasta_dna_list(open(input_file))[0].dna
    aus = 0
    cgs = 0
    for letter in dna:
        if letter == 'A' or letter == 'U':
            aus += 1
        else:
            cgs += 1
    print aus
    print cgs
    result = math.factorial((aus / 2)) * math.factorial((cgs / 2))
    print result
    with open(output_file, "w") as result_file:
        result_file.write(str(result))

PMCH("data/rosalind_pmch.txt", "data/rosalind_pmch_result.txt")

