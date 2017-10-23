'''
Created on Feb 2, 2015

@author: zoya
'''
from rosalind_utils import get_fasta_dna_list
from LCSQ import longest_common_seq

def MGAP(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    long_seq = longest_common_seq(dnas[0].dna, dnas[1].dna)
    print (long_seq)
    result = len(dnas[0].dna) + len(dnas[1].dna) - 2 * len(long_seq)
    print(result)
    
    with open(output_file, "w") as result_file:
        result_file.write(longest_common_seq(dnas[0].dna, dnas[1].dna))
        
MGAP("data/rosalind_mgap.txt", "data/rosalind_mgap_result.txt")
