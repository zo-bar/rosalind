'''
Created on Apr 30, 2014

@author: zoya
'''
from EDIT import create_distance_matrix
from rosalind_utils import get_fasta_dna_list

def get_optimal_allignment_count(string1, string2):
    matrix = create_distance_matrix(string1, string2)
    
#     i = len(matrix) - 1
#     j = len(matrix[i - 1]) - 1
#     result = [0]
#     dyn_result = {}
#     recursive_count(matrix, string1, string2, i, j, result, dyn_result)
#     print(result)
    # return result[0]
    return direct_paths_count(matrix, string1, string2)


def recursive_count(matrix, string1, string2, i, j, result, dyn_result):
    if i == 0 and j == 0:
        result[0] += 1
        # print("Result++")
        return
    # print ("i=%d, j=%d, matrix[i-1][j-1]=%d,matrix[i][j]=%d, string1[i-1]=%s, string2[j-1]=%s" % (i, j, matrix[i - 1][j - 1], matrix[i][j], string1[i - 1], string2[j - 1]))
    if i > 0 and j > 0 and matrix[i - 1][j - 1] == matrix[i][j] and string1[i - 1] == string2[j - 1]:
        recursive_count(matrix, string1, string2, i - 1, j - 1, result, dyn_result)
    if j == 0 or (i > 0 and matrix[i - 1][j] + 1 == matrix[i][j]):
        recursive_count(matrix, string1, string2, i - 1, j, result, dyn_result)
    if i == 0 or (j > 0 and matrix[i][j - 1] + 1 == matrix[i][j]):
        recursive_count(matrix, string1, string2, i, j - 1, result, dyn_result)
    if i > 0 and j > 0 and matrix[i - 1][j - 1] + 1 == matrix[i][j]:
        recursive_count(matrix, string1, string2, i - 1, j - 1, result, dyn_result)
        
def direct_paths_count(matrix, string1, string2):
    n = len(string1) 
    m = len(string2) 
    path = {n:1}
    result = 0
    for j in range(m, -1, -1):
        new_path = {}
        for i in range(n, -1, -1):
            if i > 0 and matrix[i - 1][j] + 1 == matrix[i][j]:
                path[i - 1] = path.get(i - 1, 0) + path.get(i, 0) 
            if j > 0 and matrix[i][j - 1] + 1 == matrix[i][j]:
                new_path[i] = new_path.get(i, 0) + path.get(i, 0) 
            if i > 0 and j > 0 and (matrix[i - 1][j - 1] == matrix[i][j] and string1[i - 1] == string2[j - 1] \
                    or matrix[i - 1][j - 1] + 1 == matrix[i][j]):
                new_path[i - 1] = new_path.get(i - 1, 0) + path.get(i, 0) 
                    
        result = path.get(0)
        path = new_path 
        # print ("j=%d, path=%s" % (j, path))
        
    return result 
            
def CTEA(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    result = get_optimal_allignment_count(dnas[0].dna, dnas[1].dna)
    print(result)
    print(result % (2 ** 27 - 1))
    with open(output_file, "w") as result_file:
        result_file.write(str(result % 134217727))
        
CTEA("data/rosalind_ctea.txt", "data/rosalind_ctea_result.txt")
# get_optimal_allignment_count("PLEASANTLY", "MEANLY")
