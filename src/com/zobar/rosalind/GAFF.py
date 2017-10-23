'''
Created on Nov 12, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from GLOB import BLOSOM62, BLOSOM62_HEADS
GAP_OPEN_PENALTY = -11
GAP_EXT_PENALTY = -1
ZFILL = 3

def create_global_distance_matrix(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    matrix[0] = [GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        matrix[i][0] = GAP_OPEN_PENALTY + (i - 1) * GAP_EXT_PENALTY 
    matrix[0][0] = 0
    y_matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    x_matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    x_matrix[0] = [GAP_OPEN_PENALTY for i in range(len(matrix[0]))]
    for i in range(len1 + 1):
        y_matrix[i][0] = GAP_OPEN_PENALTY
    matrix_pointer = [['M'] * (len2 + 1) for x in range(len1 + 1)]
    y_matrix_pointer = [['T'] * (len2 + 1) for x in range(len1 + 1)]
    x_matrix_pointer = [['L'] * (len2 + 1) for x in range(len1 + 1)]
    
    for i in range(1, len1 + 1):
        i_index = BLOSOM62_HEADS.index(string1[i - 1])
        for j in range(1, len2 + 1):
            j_index = BLOSOM62_HEADS.index(string2[j - 1])
            
            x_matrix[i][j] = max(x_matrix[i - 1][j] + GAP_EXT_PENALTY, matrix[i - 1][j] + GAP_OPEN_PENALTY)
            y_matrix[i][j] = max(y_matrix[i][j - 1] + GAP_EXT_PENALTY, matrix[i][j - 1] + GAP_OPEN_PENALTY)
            matrix[i][j] = max(matrix[i - 1][j - 1] + BLOSOM62[i_index][j_index], y_matrix[i][j], x_matrix[i][j])
#            matrix[i][j] = BLOSOM62[i_index][j_index] + max(matrix[i - 1][j - 1], y_matrix[i - 1][j - 1], x_matrix[i - 1][j - 1])
#            x_matrix[i][j] = max(GAP_OPEN_PENALTY + matrix[i][j - 1], GAP_EXT_PENALTY + x_matrix[i][j - 1], GAP_OPEN_PENALTY + y_matrix[i][j - 1])
#            y_matrix[i][j] = max(GAP_OPEN_PENALTY + matrix[i - 1][j], GAP_EXT_PENALTY + y_matrix[i - 1][j], GAP_OPEN_PENALTY + x_matrix[i - 1][j])
            
            if x_matrix[i][j] == matrix[i - 1][j] + GAP_OPEN_PENALTY:
                x_matrix_pointer[i][j] = 'M'
            if y_matrix[i][j] == matrix[i][j - 1] + GAP_OPEN_PENALTY:
                y_matrix_pointer[i][j] = 'M'
            if matrix[i][j] == y_matrix[i][j]:
                matrix_pointer[i][j] = 'T'
            elif matrix[i][j] == x_matrix[i][j]:
                matrix_pointer[i][j] = 'L'           
    
    curr_pointer = 'M'
    if x_matrix[i][j] >= matrix[i][j]:
        curr_pointer = 'L'
    elif y_matrix[i][j] >= matrix[i][j]:
        curr_pointer = 'T'

    print ("\n".join([" ".join([str(x).zfill(ZFILL) for x in x_matrix[i]]) for i in range(len(x_matrix))]))
    print ("\n".join([" ".join([str(x).zfill(ZFILL) for x in y_matrix[i]]) for i in range(len(y_matrix))]))

    print ("\n".join([" ".join([str(x) for x in matrix_pointer[i]]) for i in range(len(matrix_pointer))]))
    
    print ("    " + " "*ZFILL + (" "*ZFILL).join(string2))
    for i in range(len(matrix)):
        stri = ' '
        if i > 0:
            stri = string1[i - 1]
        print (stri + " " + " ".join(str(x).zfill(ZFILL) for x in matrix[i]))

    return [matrix, matrix_pointer, y_matrix_pointer, x_matrix_pointer, curr_pointer]

def get_affine_gap_alignement(string1, string2):
    matrix_arr = create_global_distance_matrix(string1, string2)
    matrix = matrix_arr[0]
    matrix_pointer = matrix_arr[1]
    y_matrix_pointer = matrix_arr[2]
    x_matrix_pointer = matrix_arr[3]
    
    i = len(matrix) - 1
    j = len(matrix[i - 1]) - 1
    result1 = ''
    result2 = ''
    curr_pointer = matrix_arr[4]
    while i > 0 or j > 0:
#        print curr_pointer
        if curr_pointer == 'M' and i > 0 and j > 0:
            curr_pointer = matrix_pointer[i - 1][j - 1]
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif i == 0 or j > 0 and curr_pointer == 'T':
            curr_pointer = y_matrix_pointer[i - 1][j - 1]
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        elif j == 0 or i > 0 and curr_pointer == 'L':
            curr_pointer = x_matrix_pointer[i - 1][j - 1]
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        else:
            print ("Error! Unable to trace back")
            print ("i=%d, j=%d" % (i, j))
            print ("result1=%s" % result1)
            print ("result2=%s" % result2)
            print ("curr_pointer = %d" % curr_pointer)
            return []
    print (matrix[len(string1)][len(string2)])
    print (result1)
    print (result2)
    return([matrix[len(string1)][len(string2)], result1, result2])

def check_sum(string1, string2):
    result = 0
    i_gap = 0
    j_gap = 0
    trace = ''
    for i in range(len(string1)):
        next_add = 0
        if string1[i] != '-' and string2[i] != '-':
            next_add = BLOSOM62[BLOSOM62_HEADS.index(string1[i])][BLOSOM62_HEADS.index(string2[i])]
            i_gap = 0
            j_gap = 0
        elif string1[i] == '-':
            if i_gap == 0:
                i_gap = 1
                next_add = GAP_OPEN_PENALTY
            else:
                next_add = GAP_EXT_PENALTY
        elif string2[i] == '-':
            if j_gap == 0:
                j_gap = 1
                next_add = GAP_OPEN_PENALTY
            else:
                next_add = GAP_EXT_PENALTY
        result += next_add
        trace += ' ' + str(next_add).zfill(3)
    print ("Check sum:")
    print (" " + " ".join(letter.zfill(3) for letter in string1))
    print (" " + " ".join(letter.zfill(3) for letter in string2))
    print (trace)
    print (result)
    return result

def GAFF(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    result = get_affine_gap_alignement(dnas[0].dna, dnas[1].dna)
    check_sum(result[1], result[2])
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(str(x) for x in result))
        
GAFF("src/data/rosalind_laff.txt", "src/data/rosalind_laff_gaff_result.txt")


