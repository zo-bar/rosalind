'''
Created on Nov 9, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

PAM250_HEADS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
PAM250 = [
[ 2, -2, 0, 0, -3, 1, -1, -1, -1, -2, -1, 0, 1, 0, -2, 1, 1, 0, -6, -3],
[-2, 12, -5, -5, -4, -3, -3, -2, -5, -6, -5, -4, -3, -5, -4, 0, -2, -2, -8, 0],
[ 0, -5, 4, 3, -6, 1, 1, -2, 0, -4, -3, 2, -1, 2, -1, 0, 0, -2, -7, -4],
[ 0, -5, 3, 4, -5, 0, 1, -2, 0, -3, -2, 1, -1, 2, -1, 0, 0, -2, -7, -4],
[-3, -4, -6, -5, 9, -5, -2, 1, -5, 2, 0, -3, -5, -5, -4, -3, -3, -1, 0, 7],
[ 1, -3, 1, 0, -5, 5, -2, -3, -2, -4, -3, 0, 0, -1, -3, 1, 0, -1, -7, -5],
[-1, -3, 1, 1, -2, -2, 6, -2, 0, -2, -2, 2, 0, 3, 2, -1, -1, -2, -3, 0],
[-1, -2, -2, -2, 1, -3, -2, 5, -2, 2, 2, -2, -2, -2, -2, -1, 0, 4, -5, -1],
[-1, -5, 0, 0, -5, -2, 0, -2, 5, -3, 0, 1, -1, 1, 3, 0, 0, -2, -3, -4],
[-2, -6, -4, -3, 2, -4, -2, 2, -3, 6, 4, -3, -3, -2, -3, -3, -2, 2, -2, -1],
[-1, -5, -3, -2, 0, -3, -2, 2, 0, 4, 6, -2, -2, -1, 0, -2, -1, 2, -4, -2],
[ 0, -4, 2, 1, -3, 0, 2, -2, 1, -3, -2, 2, 0, 1, 0, 1, 0, -2, -4, -2],
[ 1, -3, -1, -1, -5, 0, 0, -2, -1, -3, -2, 0, 6, 0, 0, 1, 0, -1, -6, -5],
[ 0, -5, 2, 2, -5, -1, 3, -2, 1, -2, -1, 1, 0, 4, 1, -1, -1, -2, -5, -4],
[-2, -4, -1, -1, -4, -3, 2, -2, 3, -3, 0, 0, 0, 1, 6, 0, -1, -2, 2, -4],
[ 1, 0, 0, 0, -3, 1, -1, -1, 0, -3, -2, 1, 1, -1, 0, 2, 1, -1, -2, -3],
[ 1, -2, 0, 0, -3, 0, -1, 0, 0, -2, -1, 0, 0, -1, -1, 1, 3, 0, -5, -3],
[ 0, -2, -2, -2, -1, -1, -2, 4, -2, 2, 2, -2, -1, -2, -2, -1, 0, 4, -6, -2],
[-6, -8, -7, -7, 0, -7, -3, -5, -3, -2, -4, -4, -6, -5, 2, -2, -5, -6, 17, 0],
[-3, 0, -4, -4, 7, -5, 0, -1, -4, -1, -2, -2, -5, -4, -4, -3, -3, -2, 0, 10]]
GAP_PENALTY = -5

def create_local_distance_matrix(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    matrix[0] = [0 for i in range(len(matrix[0]))]
    for i in range(1, len1 + 1):
        i_index = PAM250_HEADS.index(string1[i - 1])
        for j in range(1, len2 + 1):
            j_index = PAM250_HEADS.index(string2[j - 1])
            matrix[i][j] = max(0, matrix[i - 1][j] + GAP_PENALTY, matrix[i][j - 1] + GAP_PENALTY, matrix[i - 1][j - 1] + PAM250[i_index][j_index])
#    print "    " + " "*5 + (" "*5).join(string2)
#    for i in xrange(len(matrix)):
#        stri = ' '
#        if i > 0:
#            stri = string1[i - 1]
#        print stri + " " + " ".join(str(x).zfill(5) for x in matrix[i])
    return matrix

def get_alignement(string1, string2):
    matrix = create_local_distance_matrix(string1, string2)
    maximum = 0  
#    print max([max(i) for i in matrix])
    for k in range(len(matrix)):
        for l in range(len(matrix[k])):
            if string1[k - 1] == string2[l - 1] and matrix[k][l] > maximum:
                maximum = matrix[k][l]
                i = k
                j = l
    print (maximum)
    result1 = ''
    result2 = ''
    while matrix[i][j] > 0  and (i > 0 or j > 0):
        if i > 0 and j > 0 and matrix[i - 1][j - 1] == matrix[i][j] - PAM250[PAM250_HEADS.index(string1[i - 1])][PAM250_HEADS.index(string2[j - 1])]:
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif j == 0 or (i > 0 and matrix[i - 1][j] == matrix[i][j] - GAP_PENALTY):
            result1 = string1[i - 1] + result1
            result2 = result2
            i -= 1
        elif i == 0 or (j > 0 and matrix[i][j - 1] == matrix[i][j] - GAP_PENALTY):
            result1 = result1
            result2 = string2[j - 1] + result2
            j -= 1
        else:
            print ("Error! Unable to trace back")
            return str(maximum)
    while result1[0] != result2[0]:
        maximum -= PAM250[PAM250_HEADS.index(result1[0])][PAM250_HEADS.index(result2[0])]
        result1 = result1[1:]
        result2 = result2[1:]
    print (maximum)
    print (result1)
    print (result2)
    return str(maximum) + "\n" + result1 + "\n" + result2
    
    
def LOCA(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write(str(get_alignement(dnas[0].dna, dnas[1].dna)))
        
# LOCA("src/data/rosalind_loca.txt", "src/data/rosalind_loca_result.txt")
