'''
Created on Feb 6, 2016

@author: zoya
'''
from time import gmtime, strftime
from rosalind_utils import get_fasta_dna_list

MATCH_SCORE = 1
MISMATCH_SCORE = -1

test_mode = True

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
    matrix[0] = [-i for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        matrix[i][0] = -i
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            matrix[i][j] = max(matrix[i - 1][j] + (MISMATCH_SCORE if j > 0 and j < len2 + 1 else 0), matrix[i][j - 1] + MISMATCH_SCORE, matrix[i - 1][j - 1] + (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE))
    if test_mode: print_matrix(matrix, string1, string2)
    return matrix

def OSYM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start OSYM", gmtime()))
    dnas = get_fasta_dna_list(open(input_file))
    s1 = dnas[0].dna
    s2 = dnas[1].dna
    left_matrix = create_distance_matrix(dnas[0].dna, dnas[1].dna)
    right_matrix = create_distance_matrix(dnas[0].dna[::-1], dnas[1].dna[::-1])
    
    print (strftime("%Y-%m-%d %H:%M:%S Matrix done", gmtime()))
    
    M = []
    l1 = len(s1)
    l2 = len(s2)
    for i in range(len(s1)):
        next_line = []
        M.append(next_line)
        for j in range(len(s2)):
            cross = MATCH_SCORE if s1[i] == s2[j] else MISMATCH_SCORE
            left = left_matrix[i][j]
            right = right_matrix[l1 - i - 1][l2 - j - 1]
            score = left + right + cross
            if test_mode: print ("i: %d (%s), j: %d (%s), left: %d, right: %d, cross:%d, result:%d" % (i, s1[i], j, s2[j], left, right, cross, score))
            next_line.append(score)
    
    print (strftime("%Y-%m-%d %H:%M:%S Result matrix done", gmtime()))
          
    if test_mode: print ("          Result matrix:")
    if test_mode: print ('\n'.join([' '.join(str(x).zfill(3) for x in y) for y in M]))
    
    alignment_score = left_matrix[l1][l2]
    matrix_sum = sum([sum(x) for x in M])
    print ("Alignment score: %d" % alignment_score)
    print (right_matrix[l1][l2])
    print ("Matrix sum: %d" % matrix_sum)
    with open(output_file, "w") as result_file:
        result_file.write(str(alignment_score) + "\n" + str(matrix_sum))
    print (strftime("%Y-%m-%d %H:%M:%S Finished", gmtime()))
    
test_mode = False       
OSYM("data/rosalind_osym.txt", "data/rosalind_osym_result.txt")

