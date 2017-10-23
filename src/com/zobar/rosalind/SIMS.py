'''
Created on Jan 31, 2015

@author: zoya
'''
from rosalind_utils import get_fasta_dna_list
MATCH_SCORE = 1
MISMATCH_SCORE = -1

def print_matrix(matrix, string1, string2):
    print ("    " + " "*3 + (" "*3).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(3) for x in matrix[i]))
        
def create_distance_matrix(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    # matrix[0] = [0 for i in range(len(matrix[0]))]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            matrix[i][j] = max(matrix[i - 1][j] + (MISMATCH_SCORE if j > 0 and j < len2 + 1 else 0), matrix[i][j - 1] + MISMATCH_SCORE, matrix[i - 1][j - 1] + (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE))
    # print_matrix(matrix, string1, string2)
    return matrix

def get_alignement(string1, string2):
    matrix = create_distance_matrix(string1, string2)
    maximum = 0  
#    print max([max(i) for i in matrix])
    l = len(matrix[0]) - 1        
    for k in range(len(matrix)):
        if string1[k - 1] == string2[l - 1] and matrix[k][l] > maximum:
            maximum = matrix[k][l]
            i = k
            j = l
    print (maximum)
    result1 = ''
    result2 = ''
    while (i > 0 and j > 0):
        if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE if j > 0 and j < len(string2) + 1 else 0):
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        elif matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        else:
            print ("Error! Unable to trace back")
            print (result1)
            print(result2)
    print (result1)
    print (result2)
    return str(maximum) + "\n" + result1 + "\n" + result2
    
def SIMS(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write(str(get_alignement(dnas[0].dna, dnas[1].dna)))
        
SIMS("src/data/rosalind_sims.txt", "src/data/rosalind_sims_result.txt")
