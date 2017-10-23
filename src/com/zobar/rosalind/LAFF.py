'''
Created on Apr 17, 2015

@author: zoya
'''
from time import gmtime, strftime

from rosalind_utils import get_fasta_dna_list
from GLOB import BLOSOM62, BLOSOM62_HEADS
GAP_OPEN_PENALTY = -11
GAP_EXT_PENALTY = -1
ZFILL = 3

def create_local_distance_matrix(string1, string2):
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start creating matrix... ")
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    # matrix[0] = [GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY for i in range(len(matrix[0]))]
    # for i in range(len1 + 1):
    #    matrix[i][0] = GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY 
    # matrix[0][0] = 0
    
    # M=0, T=1, L=2
    matrix_pointer = [[0] * (len2 + 1) for x in range(len1 + 1)]
    y_matrix_pointer = [[1] * (len2 + 1) for x in range(len1 + 1)]
    x_matrix_pointer = [[2] * (len2 + 1) for x in range(len1 + 1)]
    
    max_pointer = 0
    maximum = 0
    max_i = 0
    max_j = 0
    next_x_matrix = [GAP_OPEN_PENALTY for k in range(len2 + 1)]
    prev_x_matrix = [GAP_OPEN_PENALTY for k in range(len2 + 1)]
    for i in range(1, len1 + 1):
        i_index = BLOSOM62_HEADS.index(string1[i - 1])
        prev_y = GAP_OPEN_PENALTY
        
        for j in range(1, len2 + 1):
            j_index = BLOSOM62_HEADS.index(string2[j - 1])
            
            next_x_matrix[j] = prev_x_matrix[j] + GAP_EXT_PENALTY            
            if next_x_matrix[j] < matrix[i - 1][j] + GAP_OPEN_PENALTY:
                next_x_matrix[j] = matrix[i - 1][j] + GAP_OPEN_PENALTY
                x_matrix_pointer[i][j] = 0
            
            next_y = prev_y + GAP_EXT_PENALTY
            if next_y < matrix[i][j - 1] + GAP_OPEN_PENALTY:
                next_y = matrix[i][j - 1] + GAP_OPEN_PENALTY
                y_matrix_pointer[i][j] = 0
            prev_y = next_y  # max(-GAP_EXT_PENALTY, next_y)
            
            matrix[i][j] = max(0, matrix[i - 1][j - 1] + BLOSOM62[i_index][j_index])
            # print (matrix[i][j])
            if next_x_matrix[j] > matrix[i][j]:
                matrix[i][j] = next_x_matrix[j]
                matrix_pointer[i][j] = 2
            if next_y > matrix[i][j]:
                matrix[i][j] = next_y
                matrix_pointer[i][j] = 1

            if matrix[i][j] > maximum:
                maximum = matrix[i][j]
                max_i = i
                max_j = j
                max_pointer = matrix_pointer[i][j]
            
#             if matrix[i][j] < 0 or prev_y < 0 or next_x_matrix[j] < 0:
#                 print ("HERE: i=%d, j=%d" % (i, j))
            
        # prev_x_matrix = [k if k > 0 else -GAP_EXT_PENALTY for k in next_x_matrix]
        prev_x_matrix = next_x_matrix
    print (maximum)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Matrix done.")
    # print_matrix(matrix, string1, string2)
    return [matrix, matrix_pointer, y_matrix_pointer, x_matrix_pointer, max_pointer, maximum, max_i, max_j]

def get_affine_gap_alignement(string1, string2):
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Start alignment...")
    matrix_arr = create_local_distance_matrix(string1, string2)
    matrix = matrix_arr[0]
    matrix_pointer = matrix_arr[1]
    y_matrix_pointer = matrix_arr[2]
    x_matrix_pointer = matrix_arr[3]
    curr_pointer = matrix_arr[4]
    maximum = matrix_arr[5]
    i = matrix_arr[6]
    j = matrix_arr[7]
    result1 = ''
    result2 = ''
    
    while matrix[i][j] > 0 and (i > 0 or j > 0):
#        print curr_pointer
        if curr_pointer == 0 and i > 0 and j > 0:
            curr_pointer = matrix_pointer[i - 1][j - 1]
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif i == 0 or j > 0 and curr_pointer == 1:
            curr_pointer = y_matrix_pointer[i - 1][j - 1]
            # result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        elif j == 0 or i > 0 and curr_pointer == 2:
            curr_pointer = x_matrix_pointer[i - 1][j - 1]
            result1 = string1[i - 1] + result1
            # result2 = '-' + result2
            i -= 1
        else:
            print ("Error! Unable to trace back")
            print ("i=%d, j=%d" % (i, j))
            print ("result1=%s" % result1)
            print ("result2=%s" % result2)
            print ("curr_pointer = %d" % curr_pointer)
            return []
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + result1)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + result2)
#     result1_in_gap = False
#     result2_in_gap = False
#     while result1[0] != result2[0]:
#         if result1[0] == '-':
#             if result1_in_gap:
#                 maximum -= GAP_EXT_PENALTY
#             else:
#                 result1_in_gap = True
#                 maximum -= GAP_OPEN_PENALTY
#         elif result2[0] == '-':
#             if result2_in_gap:
#                 maximum -= GAP_EXT_PENALTY
#             else:
#                 result2_in_gap = True
#                 maximum -= GAP_OPEN_PENALTY
#         else:
#             match_score = BLOSOM62[BLOSOM62_HEADS.index(result1[0])][BLOSOM62_HEADS.index(result2[0])]
#             if match_score < 0:
#                 maximum -= match_score
#             else:
#                 break
#         result1 = result1[1:]
#         result2 = result2[1:]
     
    print (maximum)
    print (result1)
    print (result2)
    print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ' ' + "Strings aligned")
    return ([maximum, result1, result2])

def print_matrix(matrix, string1, string2):
    print ("    " + " "*ZFILL + (" "*ZFILL).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(ZFILL) for x in matrix[i]))
        
def LAFF(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    # create_local_distance_matrix(dnas[0].dna, dnas[1].dna)
    result = get_affine_gap_alignement(dnas[0].dna, dnas[1].dna)
    # check_sum(result[1], result[2])
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in result))

LAFF("data/rosalind_laff.txt", "data/rosalind_laff_result.txt")




            
    
    #     matrix[0] = [GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY for i in range(len(matrix[0]))]
#     for i in range(len1 + 1):
#         matrix[i][0] = GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY 
#     matrix[0][0] = 0
        
#            matrix[i][j] = BLOSOM62[i_index][j_index] + max(matrix[i - 1][j - 1], y_matrix[i - 1][j - 1], x_matrix[i - 1][j - 1])
#            x_matrix[i][j] = max(GAP_OPEN_PENALTY + matrix[i][j - 1], GAP_EXT_PENALTY + x_matrix[i][j - 1], GAP_OPEN_PENALTY + y_matrix[i][j - 1])
#            y_matrix[i][j] = max(GAP_OPEN_PENALTY + matrix[i - 1][j], GAP_EXT_PENALTY + y_matrix[i - 1][j], GAP_OPEN_PENALTY + x_matrix[i - 1][j])
            
#             if x_matrix[i][j] == matrix[i - 1][j] + GAP_OPEN_PENALTY:
#                 x_matrix_pointer[i][j] = 'M'
#             if y_matrix[i][j] == matrix[i][j - 1] + GAP_OPEN_PENALTY:
#                 y_matrix_pointer[i][j] = 'M'
#             if matrix[i][j] == y_matrix[i][j]:
#                 matrix_pointer[i][j] = 'T'
#             elif matrix[i][j] == x_matrix[i][j]:  # next_x:  # 
#                 matrix_pointer[i][j] = 'L'           
    
    
#             if matrix[i][j] > maximum:
#                 maximum = matrix[i][j]
#                 curr_i = i
#                 curr_j = j
#                 curr_pointer = 'M'
#                 if x_matrix[i][j] >= matrix[i][j]:
#                     curr_pointer = 'L'
#                 elif y_matrix[i][j] >= matrix[i][j]:
#                     curr_pointer = 'T'
 
    # print ("\n".join([" ".join([str(x).zfill(ZFILL) for x in x_matrix[i]]) for i in range(len(x_matrix))]))
    # print ("\n".join([" ".join([str(x).zfill(ZFILL) for x in y_matrix[i]]) for i in range(len(y_matrix))]))

    # print ("\n".join([" ".join([str(x) for x in matrix_pointer[i]]) for i in range(len(matrix_pointer))]))
    
    # print ("    " + " "*ZFILL + (" "*ZFILL).join(string2))
#     for i in range(len(matrix)):
#         stri = ' '
#         if i > 0:
#             stri = string1[i - 1]
#         print (stri + " " + " ".join(str(x).zfill(ZFILL) for x in matrix[i]))
