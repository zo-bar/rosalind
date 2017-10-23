'''
Created on Jul 28, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

def longest_common_seq(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    for i in range(len1):
        for j in range(len2):
            if string1[i] == string2[j]:
                matrix[i + 1][j + 1] = matrix[i][j] + 1
            else:
                matrix[i + 1][j + 1] = max(matrix[i + 1][j], matrix[i][j + 1])
    
    i = len(string1)
    j = len(string2)
    result = ''
    while i > 0 and j > 0:
        if string1[i - 1] == string2[j - 1]:
            i -= 1
            j -= 1
            result = string1[i] + result
        elif matrix[i][j - 1] > matrix[i - 1][j]:
            j -= 1
        else:
            i -= 1
    return result

def LCSQ(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write(longest_common_seq(dnas[0].dna, dnas[1].dna))
        
# LCSQ("data/rosalind_lcsq.txt", "data/rosalind_lcsq_result.txt")
