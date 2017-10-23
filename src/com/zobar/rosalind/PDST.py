'''
Created on Jul 26, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from HAMM import hamm

def PDST(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    result = [[0 for y in xrange(len(dnas))] for x in xrange(len(dnas))]
    dna_len = len(dnas[0].dna) + 0.0
    for i, dna1 in enumerate(dnas):
        for j, dna2 in enumerate(dnas):
            if result[j][i] != 0:
                result[i][j] = result[j][i]
            else:
                result[i][j] = round(hamm(dna1.dna, dna2.dna) / dna_len, 3)
    print result
    with open(output_file, "w") as result_file:
        for i in xrange(len(result)):
            result_file.write(" ".join(str(x) for x in result[i]) + "\n")

PDST("data/rosalind_pdst.txt", "data/rosalind_pdst_result.txt")
