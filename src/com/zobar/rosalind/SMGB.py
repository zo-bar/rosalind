'''
Created on Aug 9, 2015

@author: zoya
'''
from time import gmtime, strftime

from rosalind_utils import get_fasta_dna_list
GAP_PENALTY = -1
MISMATCH_PENALTY = -1
MATCH_SCORE = 1
ZFILL = 3
 
def find_semiglobal_alignment(string1, string2):
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Building matrix...")
    
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2):
            match = (MATCH_SCORE if string2[j - 1] == string1[i - 1] else MISMATCH_PENALTY)
            matrix[i][j] = max(matrix[i - 1][j] + GAP_PENALTY, matrix[i][j - 1] + GAP_PENALTY, matrix[i - 1][j - 1] + match)
        matrix[i][len2] = max(matrix[i - 1][len2], matrix[i][len2 - 1] + GAP_PENALTY, matrix[i - 1][len2 - 1] + (MATCH_SCORE if string2[len2 - 1] == string1[i - 1] else MISMATCH_PENALTY))

    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Matrix ready")
    # print_matrix(matrix, string1, string2)
    
    result1 = ''
    result2 = ''
    score = max(matrix[-1])
    i = len(matrix) - 1
    j = len(matrix[-1]) - 1
    while (i > 0 or j > 0):
        match = (MATCH_SCORE if string2[j - 1] == string1[i - 1] else MISMATCH_PENALTY)
        # print ("s1[i-1]=%s,s2[j-1]=%s,match=%d,matrix[i-1][j-1]=%d,matrix[i][j]=%d" % (string1[i - 1], string2[j - 1], match, matrix[i - 1][j - 1], matrix[i][j]))
        if j == len2 and matrix[i - 1][j] == matrix[i][j]:
            # print ("Go up")
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        elif i > 0 and j > 0 and matrix[i - 1][j - 1] == matrix[i][j] - match:
            # print ("Go up-left")
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif (i == 0) or (j > 0 and matrix[i][j - 1] == matrix[i][j] - GAP_PENALTY):
            # print ("Go left")
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        elif (j == 0) or (i > 0 and matrix[i - 1][j] == matrix[i][j] - GAP_PENALTY):
            # print ("Go up")
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        else:
            print ("Error! Unable to trace back")
            print (result1)
            print (result2)
            return str(score)

    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Result:\nscore = %d" % score)
    print (result1)
    print (result2)
    return [score, result1, result2]
   
def print_matrix(matrix, string1, string2):
    print ("    " + " "*ZFILL + (" "*ZFILL).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(ZFILL) for x in matrix[i]))
        
def SMGB(input_file, output_file):
    dna_list = get_fasta_dna_list(open(input_file))
    result = find_semiglobal_alignment(dna_list[0].dna, dna_list[1].dna)
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in result))
    
SMGB("data/rosalind_smgb.txt", "data/rosalind_smgb_result.txt")
