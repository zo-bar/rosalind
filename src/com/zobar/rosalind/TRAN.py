'''
Created on Jul 26, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

def TRAN(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    dna1 = dnas[0].dna
    dna2 = dnas[1].dna
    transitions = 0.0;
    transversions = 0.0
    for i, letter in enumerate(dna1):
        letter2 = dna2[i]
        if (letter != letter2):
            if letter == 'A' or letter == 'G':
                if letter2 == 'A' or letter2 == 'G':
                    transitions += 1
                else:
                    transversions += 1
            else:
                if letter2 == 'A' or letter2 == 'G':
                    transversions += 1
                else:
                    transitions += 1
    print transitions / transversions

TRAN("data/rosalind_tran.txt", "data/rosalind_tran_result.txt")
                
