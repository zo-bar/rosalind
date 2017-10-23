'''
Created on Jul 29, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

def create_distance_matrix(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    matrix[0] = [i for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        matrix[i][0] = i
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if string1[i - 1] == string2[j - 1]:
                matrix[i][j] = matrix[i - 1][j - 1]
            else:
                matrix[i][j] = min(matrix[i - 1][j], matrix[i][j - 1], matrix[i - 1][j - 1]) + 1
    print ("     " + "  ".join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print(stri + " " + " ".join(str(x).zfill(2) for x in matrix[i]))
    return matrix

def edit_distance(string1, string2):
    matrix = create_distance_matrix(string1, string2)
    result = matrix[len(string1)][len(string2)]
    print (result)
    return result

def EDIT(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write(str(edit_distance(dnas[0].dna, dnas[1].dna)))
        
# EDIT("data/rosalind_edit.txt", "data/rosalind_edit_result.txt")
