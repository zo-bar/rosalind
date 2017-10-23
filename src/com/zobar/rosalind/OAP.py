'''
Created on Jun 7, 2015

@author: zoya
'''
from time import gmtime, strftime

from rosalind_utils import get_fasta_dna_list
GAP_PENALTY = -2
MISMATCH_PENALTY = -2
MATCH_SCORE = 1
ZFILL = 3
 
def find_overlap_alignment(string1, string2):
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Building matrix...")
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match = (MATCH_SCORE if string2[j - 1] == string1[i - 1] else MISMATCH_PENALTY)
            matrix[i][j] = max(matrix[i - 1][j] + GAP_PENALTY, matrix[i][j - 1] + GAP_PENALTY, matrix[i - 1][j - 1] + match)
    # print_matrix(matrix, string1, string2)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Matrix ready")
    result1 = ""
    result2 = ""
    score = max(matrix[-1])
    i = len(matrix) - 1
    j = len(matrix[-1]) - matrix[-1][::-1].index(score) - 1
    while  j > 0:  # (i > 0 or j > 0):
        match = (MATCH_SCORE if string2[j - 1] == string1[i - 1] else MISMATCH_PENALTY)
        # print ("s1[i-1]=%s,s2[j-1]=%s,match=%d,matrix[i-1][j-1]=%d,matrix[i][j]=%d" % (s1[i - 1], s2[j - 1], match, matrix[i - 1][j - 1], matrix[i][j]))
        if i > 0 and matrix[i - 1][j - 1] == matrix[i][j] - match:
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif i > 0 and matrix[i - 1][j] == matrix[i][j] - GAP_PENALTY:
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        elif i == 0 or matrix[i][j - 1] == matrix[i][j] - GAP_PENALTY:
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        else:
            print ("Error! Unable to trace back")
            print (result1)
            print (result2)
            return str(score)

    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Result: score = %d" % score)
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
        
def OAP(input_file, output_file):
    dna_list = get_fasta_dna_list(open(input_file))
    result = find_overlap_alignment(dna_list[0].dna, dna_list[1].dna)
    print (result)
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in result))
    
OAP("data/rosalind_oap.txt", "data/rosalind_oap_result.txt")


# Misunderstand the task
# def build_matrix(string1, string2):
#     print ("Start aligning strings")
#     print ("String1: %s" % string1)
#     print ("String2: %s" % string2)
#     len1 = len(string1)
#     len2 = len(string2)
#     matrix = [[-99] * (len2 + 1) for x in range(len1 + 1)]
#     matrix[0] = [-99 for i in range(len(matrix[0]))]
#     matrix[0][0] = 0
#     
#     for i in range(1, len1 + 1):
#         has_pos = False
#         for j in range(1, len2 + 1):
#             match = (MATCH_SCORE if string2[j - 1] == string1[i - 1] else MISMATCH_PENALTY)
#             matrix[i][j] = max(matrix[i - 1][j] + GAP_PENALTY, matrix[i][j - 1] + GAP_PENALTY, matrix[i - 1][j - 1] + match)
#             has_pos = has_pos or (matrix[i][j] >= 0)
#         if not has_pos:
#             # print_matrix(matrix, string1, string2)
#             return None
#     return matrix
# 
# def find_overlap_alignment(string1, string2):
#     s2prefix = string2[:2]
#     index = string1.find(s2prefix)
#     
#     s1 = string1[index:]
#     s2len = int(1.5 * len(string1[index:])) + 1
#     s2 = string2[:s2len]
#     matrix = build_matrix(s1, s2)
#     while matrix == None and index < len(string1) - 1:
#         # check third symbol
#         # build matrix
#         index = string1.find(s2prefix, index + 1)
#         s1 = string1[index:]
#         s2len = int(1.5 * len(string1[index:])) + 1
#         s2 = string2[:s2len]
#         matrix = build_matrix(string1[index:], string2[:s2len])
#     
#     # print_matrix(matrix, s1, s2)
#     
#     # restore alignment by matrix
#     result1 = ""
#     result2 = ""
#     score = max(matrix[-1])
#     i = len(matrix) - 1
#     j = len(matrix[-1]) - matrix[-1][::-1].index(score) - 1
#     while  (i > 0 or j > 0):
#         match = (MATCH_SCORE if s2[j - 1] == s1[i - 1] else MISMATCH_PENALTY)
#         # print ("s1[i-1]=%s,s2[j-1]=%s,match=%d,matrix[i-1][j-1]=%d,matrix[i][j]=%d" % (s1[i - 1], s2[j - 1], match, matrix[i - 1][j - 1], matrix[i][j]))
#         if i > 0 and j > 0 and matrix[i - 1][j - 1] == matrix[i][j] - match:
#             result1 = s1[i - 1] + result1
#             result2 = s2[j - 1] + result2
#             i -= 1
#             j -= 1
#         elif j == 0 or (i > 0 and matrix[i - 1][j] == matrix[i][j] - GAP_PENALTY):
#             result1 = s1[i - 1] + result1
#             result2 = '-' + result2
#             i -= 1
#         elif i == 0 or (j > 0 and matrix[i][j - 1] == matrix[i][j] - GAP_PENALTY):
#             result1 = '-' + result1
#             result2 = s2[j - 1] + result2
#             j -= 1
#         else:
#             print ("Error! Unable to trace back")
#             print (result1)
#             print (result2)
#             return str(score)
#     print (result1)
#     print (result2)
#     return [score, result1, result2]

