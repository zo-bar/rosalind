'''
Created on Nov 7, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from GLOB import BLOSOM62, BLOSOM62_HEADS, GAP_VALUE

def create_global_distance_matrix(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    matrix[0] = [GAP_VALUE for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        matrix[i][0] = GAP_VALUE
    matrix[0][0] = 0
    i_gap_matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    j_gap_matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    j_gap_matrix[0] = [-1000 for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        i_gap_matrix[i][0] = -1000
    
    for i in range(1, len1 + 1):
        i_index = BLOSOM62_HEADS.index(string1[i - 1])
        for j in range(1, len2 + 1):
            j_index = BLOSOM62_HEADS.index(string2[j - 1])
            j_gap_matrix[i][j] = max(j_gap_matrix[i - 1][j], matrix[i - 1][j] + GAP_VALUE)
            i_gap_matrix[i][j] = max(i_gap_matrix[i][j - 1], matrix[i][j - 1] + GAP_VALUE)
            matrix[i][j] = max(matrix[i - 1][j - 1] + BLOSOM62[i_index][j_index], i_gap_matrix[i][j], j_gap_matrix[i][j]) 
    print ("    " + " "*5 + (" "*5).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(5) for x in matrix[i]))
    return matrix

def edit_distance(string1, string2):
    matrix = create_global_distance_matrix(string1, string2)
    result = matrix[len(string1)][len(string2)]
    print (result)
    return result

def GCON(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write(str(edit_distance(dnas[0].dna, dnas[1].dna)))
        
GCON("src/data/rosalind_gcon.txt", "src/data/rosalind_gcon_result.txt")
