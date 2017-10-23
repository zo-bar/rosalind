'''
Created on Aug 16, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from EDIT import create_distance_matrix

def get_augment(string1, string2):
    matrix = create_distance_matrix(string1, string2)
    i = len(matrix) - 1
    j = len(matrix[i - 1]) - 1
    result1 = ''
    result2 = ''
#    cur_val = matrix[len(string1)][len(string2)]
    while i > 0 or j > 0:
        if i > 0 and j > 0 and matrix[i - 1][j - 1] < matrix[i][j]:
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif j == 0 or (i > 0 and matrix[i - 1][j] < matrix[i][j]):
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        elif i == 0 or (j > 0 and matrix[i][j - 1] < matrix[i][j]):
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        else:
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
    print (matrix[len(string1)][len(string2)])
    print (result1)
    print (result2)
    return([matrix[len(string1)][len(string2)], result1, result2])

def EDTA(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in get_augment(dnas[0].dna, dnas[1].dna)))
        
EDTA("data/rosalind_edta1.txt", "data/rosalind_edta_result1.txt")
