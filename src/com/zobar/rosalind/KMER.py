'''
Created on Jul 25, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

def KMER(input_file, output_file, k):
    dna = get_fasta_dna_list(open(input_file))[0].dna
    dna_letters = ['A', 'C', 'G', 'T']
    result = [0 for x in range(4 ** k)]
    index = 0
    for i, letter in enumerate(dna):
        index = (index << 2 & (4 ** k - 1)) + dna_letters.index(letter) 
        if i >= k - 1:
            result[index] += 1
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(x) for x in result))            

KMER("data/rosalind_kmer.txt", "data/rosalind_kmer_result.txt", 4)
