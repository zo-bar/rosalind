'''
Created on Jan 16, 2015

@author: zoya
'''
from rosalind_utils import get_fasta_dna_list
# from EDIT import EDIT

MISMATCH = -1
ALL_DIFF3 = 3 * MISMATCH
ONE_PAIR3 = 2 * MISMATCH
ALL_MATCH3 = 0

ALL_DIFF4 = 6 * MISMATCH
ONE_PAIR4 = 5 * MISMATCH
TWO_PAIRS4 = 4 * MISMATCH
TRIPLET4 = 3 * MISMATCH
ALL_MATCH4 = 0


# EQUAL_BONUS = 0

def create_global_distance_matrix4(string1, string2, string3, string4):
    
    o = '-'
    
    str1 = o + string1
    str2 = o + string2
    str3 = o + string3
    str4 = o + string4
    
    len1 = len(str1)
    len2 = len(str2)
    len3 = len(str3)
    len4 = len(str4)

    matrix = [[[[-99] * (len4 + 1) for z in range(len3 + 1)]  for y in range(len2 + 1)] for x in range(len1 + 1)]
    matrix[0][0][0][0] = 0
    
    # print_matrix4(matrix, string1, string2, string3, string4)
    for l in range(1, len4 + 1):
        for k in range(1, len3 + 1):
            for j in range(1, len2 + 1):
                for i in range(1, len1 + 1):
                    a = str1[i - 1]
                    b = str2[j - 1]
                    c = str3[k - 1]
                    d = str4[l - 1]
                    # if i == 1 or j == 1 or k == 1 or l == 1:
                    #    matrix[i][j][k][l] = get_penalty4(a, b, c, d)
                    # else:
                    case1 = matrix[i - 1][j][k][l - 1] + get_penalty4(a, o, o, d)
                    case2 = matrix[i][j - 1][k][l - 1] + get_penalty4(o, b, o, d)
                    case3 = matrix[i][j][k - 1][l - 1] + get_penalty4(o, o, c, d)
                    case4 = matrix[i - 1][j][k - 1][l - 1] + get_penalty4(a, o, c, d)
                    case5 = matrix[i][j - 1][k - 1][l - 1] + get_penalty4(o, b, c, d)
                    case6 = matrix[i - 1][j - 1][k][l - 1] + get_penalty4(a, b, o, d)
                    case7 = matrix[i - 1][j - 1][k - 1][l - 1] + get_penalty4(a, b, c, d)
                    case8 = matrix[i][j][k][l - 1] + get_penalty4(o, o, o, d)
                    case9 = matrix[i - 1][j][k][l] + get_penalty4(a, o, o, o)
                    case10 = matrix[i][j - 1][k][l] + get_penalty4(o, b, o, o)
                    case11 = matrix[i][j][k - 1][l] + get_penalty4(o, o, c, o)
                    case12 = matrix[i - 1][j][k - 1][l] + get_penalty4(a, o, c, o)
                    case13 = matrix[i][j - 1][k - 1][l] + get_penalty4(o, b, c, o)
                    case14 = matrix[i - 1][j - 1][k][l] + get_penalty4(a, b, o, o)
                    case15 = matrix[i - 1][j - 1][k - 1][l] + get_penalty4(a, b, c, o)
                    temp = max(case1, case2, case3, case4, case5, case6, case7, case8, case9, case10, case11, case12, case13, case14, case15)
                    # print("Aligning %s %s %s %s: matrix[%d][%d][%d][%d] = %d" % (a, b, c, d, i, j, k, l, temp))
                    matrix[i][j][k][l] = temp
    # print (matrix)
    matrix = [[[[matrix[i][j][k][l] for l in range(1, len4 + 1)] for k in range(1, len3 + 1)] for j in range(1, len2 + 1)] for i in range(1, len1 + 1)]
    # print (enh_matrix)
    # print_matrix4(matrix, string1, string2, string3, string4)
    return matrix

def get_penalty4(letter1, letter2, letter3, letter4):
    result = ALL_DIFF4
    if letter1 == letter2:
        result += 1
    if letter1 == letter3:
        result += 1
    if letter1 == letter4:
        result += 1
    if letter2 == letter3:
        result += 1
    if letter2 == letter4:
        result += 1
    if letter3 == letter4:
        result += 1
    return result

def print_matrix4(matrix, string1, string2, string3, string4):
    print (matrix)
    for l in range(len(string4) + 1):
        print ("Processing letter %s" % (string4[l - 1] if l > 0 else '-'))
        for k in range(len(string3) + 1):
            letter3 = '-'
            if k > 0: letter3 = string3[k - 1]
            print (letter3 + "  -   " + "   ".join(string2))
            for i in range(len(string1) + 1):
                letter1 = '-'
                if i > 0:
                    letter1 = string1[i - 1]
                print(letter1 + " " + " ".join(str(matrix[i][j][k][l]).zfill(3) for j in range(len(string2) + 1)))
            print ("_" * ((len(string2) + 1) * 3 + 2))

def get_alignment4(matrix, string1, string2, string3, string4):
    result = ["", "", "", ""]
    i = len(string1)
    j = len(string2)
    k = len(string3)
    l = len(string4)
    while i > 0 or j > 0 or k > 0 or l > 0:
        a = string1[i - 1]
        b = string2[j - 1]
        c = string3[k - 1]
        d = string4[l - 1]
        o = '-'
        if i > 0 and j > 0 and k > 0 and l > 0 and matrix[i][j][k][l] == matrix[i - 1][j - 1][k - 1][l - 1] + get_penalty4(a, b, c, d):
            result[0] = a + result[0]
            i -= 1
            result[1] = b + result[1]
            j -= 1
            result[2] = c + result[2]
            k -= 1
            result[3] = d + result[3]
            l -= 1
        elif i > 0 and j > 0 and k > 0 and matrix[i][j][k][l] == matrix[i - 1][j - 1][k - 1][l] + get_penalty4(a, b, c, o):
            result[0] = a + result[0]
            i -= 1
            result[1] = b + result[1]
            j -= 1
            result[2] = c + result[2]
            k -= 1
            result[3] = o + result[3]
        elif i > 0 and j > 0 and l > 0 and matrix[i][j][k][l] == matrix[i - 1][j - 1][k][l - 1] + get_penalty4(a, b, o, d):
            result[0] = a + result[0]
            i -= 1
            result[1] = b + result[1]
            j -= 1
            result[2] = o + result[2]
            result[3] = d + result[3]
            l -= 1            
        elif i > 0 and k > 0 and l > 0 and matrix[i][j][k][l] == matrix[i - 1][j][k - 1][l - 1] + get_penalty4(a, o, c, d):
            result[0] = a + result[0]
            i -= 1
            result[1] = o + result[1]
            result[2] = c + result[2]
            k -= 1
            result[3] = d + result[3]
            l -= 1  
        elif j > 0 and k > 0 and l > 0 and matrix[i][j][k][l] == matrix[i][j - 1][k - 1][l - 1] + get_penalty4(o, b, c, d):
            result[0] = o + result[0]
            result[1] = b + result[1]
            j -= 1
            result[2] = c + result[2]
            k -= 1
            result[3] = d + result[3]
            l -= 1  
        elif i > 0 and l > 0 and matrix[i][j][k][l] == matrix[i - 1][j][k][l - 1] + get_penalty4(a, o, o, d):
            result[0] = a + result[0]
            i -= 1
            result[1] = o + result[1]
            result[2] = o + result[2]
            result[3] = d + result[3]
            l -= 1  
        elif j > 0 and l > 0 and matrix[i][j][k][l] == matrix[i][j - 1][k][l - 1] + get_penalty4(o, b, o, d):
            result[0] = o + result[0]
            result[1] = b + result[1]
            j -= 1
            result[2] = o + result[2]
            result[3] = d + result[3]
            l -= 1  
        elif k > 0 and l > 0 and matrix[i][j][k][l] == matrix[i][j][k - 1][l - 1] + get_penalty4(o, o, c, d):
            result[0] = o + result[0]
            result[1] = o + result[1]
            result[2] = c + result[2]
            k -= 1
            result[3] = d + result[3]
            l -= 1  
        elif i > 0 and j > 0 and matrix[i][j][k][l] == matrix[i - 1][j - 1][k][l] + get_penalty4(a, b, o, o):
            result[0] = a + result[0]
            i -= 1
            result[1] = b + result[1]
            j -= 1
            result[2] = o + result[2]
            result[3] = o + result[3]
        elif i > 0 and k > 0 and matrix[i][j][k][l] == matrix[i - 1][j][k - 1][l] + get_penalty4(a, o, c, o):
            result[0] = a + result[0]
            i -= 1
            result[1] = o + result[1]
            result[2] = c + result[2]
            k -= 1
            result[3] = o + result[3]
        elif j > 0 and k > 0 and matrix[i][j][k][l] == matrix[i][j - 1][k - 1][l] + get_penalty4(o, b, c, o):
            result[0] = o + result[0]
            result[1] = b + result[1]
            j -= 1
            result[2] = c + result[2]
            k -= 1
            result[3] = o + result[3]
        elif i > 0 and matrix[i][j][k][l] == matrix[i - 1][j][k][l] + get_penalty4(a, o, o, o):
            result[0] = a + result[0]
            i -= 1
            result[1] = o + result[1]
            result[2] = o + result[2]
            result[3] = o + result[3]
        elif j > 0 and matrix[i][j][k][l] == matrix[i][j - 1][k][l] + get_penalty4(o, b, o, o):
            result[0] = o + result[0]
            result[1] = b + result[1]
            j -= 1
            result[2] = o + result[2]
            result[3] = o + result[3]
        elif k > 0 and matrix[i][j][k][l] == matrix[i][j][k - 1][l] + get_penalty4(o, o, c, o):
            result[0] = o + result[0]
            result[1] = o + result[1]
            result[2] = c + result[2]
            k -= 1
            result[3] = o + result[3]
        elif l > 0 and matrix[i][j][k][l] == matrix[i][j][k][l - 1] + get_penalty4(o, o, o, d):
            result[0] = o + result[0]
            result[1] = o + result[1]
            result[2] = o + result[2]
            result[3] = d + result[3]
            l -= 1
        else:
            print ("ERROR!")
            print ("No back movement found for i=%d, j=%d, k=%d, l=%d \nresult: \n%s" % (i, j, k, l, "\n".join(result)))
            return result
    return result

def MULT(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    matrix = create_global_distance_matrix4(dnas[0].dna, dnas[1].dna, dnas[2].dna, dnas[3].dna)
    result = get_alignment4(matrix, dnas[0].dna, dnas[1].dna, dnas[2].dna, dnas[3].dna)
    print(str(matrix[len(dnas[0].dna)][len(dnas[1].dna)][len(dnas[2].dna)][len(dnas[3].dna)]))
    print('\n'.join(result))
    
    with open(output_file, "w") as result_file:
        result_file.write(str(matrix[len(dnas[0].dna)][len(dnas[1].dna)][len(dnas[2].dna)][len(dnas[3].dna)]) + '\n')
        result_file.write("\n".join(result))
        
MULT("data/rosalind_mult.txt", "data/rosalind_mult_result.txt")

# def create_global_distance_matrix3(string1, string2, string3):
#     len1 = len(string1)
#     len2 = len(string2)
#     len3 = len(string3)
# 
#     matrix = [[[0] * (len3 + 1) for y in range(len2 + 1)] * (len2 + 1) for x in range(len1 + 1)]
#     
#     a = 'a'
#     o = "-"
#     
#     for k in range(len3 + 1):
#         matrix[0][0][k] = k * get_penalty3(o, o, a)
#     for j in range(len2 + 1):
#         matrix[0][j][0] = j * get_penalty3(o, a, o)
#     for i in range(len1 + 1):
#         matrix[i][0][0] = i * get_penalty3(a, o, o)
#     for i in range(1, len1 + 1):
#         for j in range(1, len2 + 1):
#             matrix[i][j][0] = max(matrix[i - 1][j][0] + get_penalty3(a, o, o), matrix[i][j - 1][0] + get_penalty3(o, a, o), matrix[i - 1][j - 1][0] + get_penalty3(string1[i - 1], string2[j - 1], o))            
#     for k in range(1, len3 + 1):
#         for i in range(1, len1 + 1):
#             matrix[i][0][k] = max(matrix[i - 1][0][k] + get_penalty3(a, o, o), matrix[i][0][k - 1] + get_penalty3(o, o, a), matrix[i - 1][0][k - 1] + get_penalty3(string1[i - 1], o, string3[k - 1]))
#         for j in range(1, len2 + 1):
#             matrix[0][j][k] = max(matrix[0][j - 1][k] + get_penalty3(o, o, a), matrix[0][j][k - 1] + get_penalty3(o, a, o), matrix[0][j - 1][k - 1] + get_penalty3(o, string2[j - 1], string3[k - 1]))
#     
#     # print_matrix3(matrix, string1, string2, string3)
#     
#     for i in range(1, len1 + 1):
#         for j in range(1, len2 + 1):
#             for k in range(1, len3 + 1):
#                 a = string1[i - 1]
#                 b = string2[j - 1]
#                 c = string3[k - 1]
#                 o = "-"
#                 val = matrix[i - 1][j - 1][k - 1] + get_penalty3(a, b, c)
#                 val = max(val, matrix[i - 1][j - 1][k] + get_penalty3(a, b, o))
#                 val = max(val, matrix[i - 1][j][k - 1] + get_penalty3(a, o, c))
#                 val = max(val, matrix[i][j - 1][k - 1] + get_penalty3(o, b, c))
#                 val = max(val, matrix[i - 1][j][k] + get_penalty3(a, o, o))
#                 val = max(val, matrix[i][j - 1][k] + get_penalty3(o, b, o))
#                 val = max(val, matrix[i][j][k - 1] + get_penalty3(o, o, c))
#                 matrix[i][j][k] = val
#     print_matrix3(matrix, string1, string2, string3)
#     return matrix
# 
# def get_penalty3(letter1, letter2, letter3):
#     if letter1 == letter2:
#         if letter2 == letter3:
#             return ALL_MATCH3
#         else:
#             return ONE_PAIR3
#     elif letter1 == letter3 or letter2 == letter3:
#         return ONE_PAIR3
#     return ALL_DIFF3
# 
# def print_matrix3(matrix, string1, string2, string3):
#     print (matrix)
#     for k in range(len(string3) + 1):
#         letter3 = '-'
#         if k > 0: letter3 = string3[k - 1]
#         print (letter3 + "  -   " + "   ".join(string2))
#         for i in range(len(string1) + 1):
#             letter1 = '-'
#             if i > 0:
#                 letter1 = string1[i - 1]
#             print(letter1 + " " + " ".join(str(matrix[i][j][k]).zfill(3) for j in range(len(string2) + 1)))
#         print ("_" * ((len(string2) + 1) * 3 + 2))
# 
# def get_alignment3(matrix, string1, string2, string3):
#     result = ["", "", ""]
#     i = len(string1)
#     j = len(string2)
#     k = len(string3)
#     while i > 0 or j > 0 or k > 0:
#         a = string1[i - 1]
#         b = string2[j - 1]
#         c = string3[k - 1]
#         o = '-'
#         if i > 0 and j > 0 and k > 0 and matrix[i][j][k] == matrix[i - 1][j - 1][k - 1] + get_penalty3(a, b, c):
#             result[0] = a + result[0]
#             i -= 1
#             result[1] = b + result[1]
#             j -= 1
#             result[2] = c + result[2]
#             k -= 1
#         elif i > 0 and j > 0 and matrix[i][j][k] == matrix[i - 1][j - 1][k] + get_penalty3(a, b, o):
#             result[0] = a + result[0]
#             i -= 1
#             result[1] = b + result[1]
#             j -= 1
#             result[2] = o + result[2]
#         elif i > 0 and k > 0 and matrix[i][j][k] == matrix[i - 1][j][k - 1] + get_penalty3(a, o, c):
#             result[0] = a + result[0]
#             i -= 1
#             result[1] = o + result[1]
#             result[2] = c + result[2]
#             k -= 1
#         elif j > 0 and k > 0 and matrix[i][j][k] == matrix[i][j - 1][k - 1] + get_penalty3(o, b, c):
#             result[0] = o + result[0]
#             result[1] = b + result[1]
#             j -= 1
#             result[2] = c + result[2]
#             k -= 1
#         elif i > 0 and matrix[i][j][k] == matrix[i - 1][j][k] + get_penalty3(a, o, o):
#             result[0] = a + result[0]
#             i -= 1
#             result[1] = o + result[1]
#             result[2] = o + result[2]
#         elif j > 0 and matrix[i][j][k] == matrix[i][j - 1][k] + get_penalty3(o, b, o):
#             result[0] = o + result[0]
#             result[1] = b + result[1]
#             j -= 1
#             result[2] = o + result[2]
#         elif k > 0 and matrix[i][j][k] == matrix[i][j][k - 1] + get_penalty3(o, o, c):
#             result[0] = o + result[0]
#             result[1] = o + result[1]
#             result[2] = c + result[2]
#             k -= 1
#         else:
#             print ("ERROR!")
#             print ("No back movement found for i=%d, j=%d, k=%d, result: %s" % (i, j, k, result))
#             print (string3
#                    )
#             return result
#     return result
# 
# def MULT3(string1, string2, string3):
#     matrix = create_global_distance_matrix3(string1, string2, string3)
#     result = get_alignment3(matrix, string1, string2, string3)
#     print ("\n".join(result))
#     return result
#
# EDIT("data/rosalind_edit_test.txt", "data/rosalind_edit_test_result.txt")




    
#     a = 'a'
#     o = "-"
#     
#     for i in range(len1 + 1):
#         matrix[i][0][0][0] = i * get_penalty4(a, o, o, o)
#     for j in range(len2 + 1):
#         matrix[0][j][0][0] = j * get_penalty4(o, a, o, o)
#     for k in range(len3 + 1):
#         matrix[0][0][k][0] = k * get_penalty4(o, o, a, o)
#     for l in range(len4 + 1):
#         matrix[0][0][0][l] = l * get_penalty4(o, o, o, a)
#     
#     for i in range(1, len1 + 1):
#         for j in range(1, len2 + 1):
#             matrix[i][j][0][0] = max(matrix[i - 1][j][0][0] + get_penalty4(a, o, o, o), matrix[i][j - 1][0][0] + get_penalty4(o, a, o, o), matrix[i - 1][j - 1][0][0] + get_penalty4(string1[i - 1], string2[j - 1], o, o))            
#     for k in range(1, len3 + 1):
#         for i in range(1, len1 + 1):
#             matrix[i][0][k][0] = max(matrix[i - 1][0][k][0] + get_penalty4(a, o, o, o), matrix[i][0][k - 1][0] + get_penalty4(o, o, a, o), matrix[i - 1][0][k - 1][0] + get_penalty4(string1[i - 1], o, string3[k - 1], o))
#         for j in range(1, len2 + 1):
#             matrix[0][j][k][0] = max(matrix[0][j - 1][k][0] + get_penalty4(o, o, a, o), matrix[0][j][k - 1][0] + get_penalty4(o, a, o, o), matrix[0][j - 1][k - 1][0] + get_penalty4(o, string2[j - 1], string3[k - 1], o))
#     for i in range(1, len1 + 1):
#         for j in range(1, len2 + 1):
#             for k in range(1, len3 + 1):
#                 a = string1[i - 1]
#                 b = string2[j - 1]
#                 c = string3[k - 1]
#                 case1 = matrix[i - 1][j][k][0] + get_penalty4(a, o, o, o)
#                 case2 = matrix[i][j - 1][k][0] + get_penalty4(o, b, o, o)
#                 case3 = matrix[i][j][k - 1][0] + get_penalty4(o, o, c, o)
#                 case4 = matrix[i - 1][j][k - 1][0] + get_penalty4(a, o, c, o)
#                 case5 = matrix[i][j - 1][k - 1][0] + get_penalty4(o, b, c, o)
#                 case6 = matrix[i - 1][j - 1][k][0] + get_penalty4(a, b, o, o)
#                 case7 = matrix[i - 1][j - 1][k - 1][0] + get_penalty4(a, b, c, o)
#                 matrix[i][j][k][0] = max(case1, case2, case3, case4, case5, case6, case7)            
#     
#     
#     str1 = string1+'-'
#     str2 = string2+'-'
#     str3 = string3+'-'
#     str4 = string4+'-'
#     
#     for i in range(1, len(str1)+1):
#         for j in range(1, len(str2)+1):
#             for k in range(1, len(str3)+1):
#                 for l in range(1, len(str4)+1):
#                     if i==0 or j==0 or k==0 or l==0:
#                         a=str1[i-1]
#                         b=str2[j-1]
#                         c=str3[k-1]
#                         d=str4[l-1]
#                         
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,o,o,o)
#                         case2=matrix[i-1][j][k][l] + get_penalty4(o,b,o,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(o,o,c,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(o,o,o,d)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,b,o,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,o,c,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,o,o,d)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(o,b,c,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(o,b,o,d)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(o,o,c,d)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,b,c,o)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,b,o,d)
#                         case1=matrix[i-1][j][k][l] + get_penalty4(a,o,c,d)
#                         
#                         
#                         
#                         
#                         
#                         matrix[i][j][k][l] = max(case1, case2)
#     
#     
#     
# #     
# #     for l in range(1, len4 + 1):
# #         for k in range(1, len3 + 1):
# #             for i in range(1, len1 + 1):
# #                 a = string1[i - 1]
# #                 c = string3[k - 1]
# #                 d = string4[l - 1]
# #                 
# #                 matrix[i][0][k][0] = max(matrix[i - 1][0][k][0] + get_penalty4(a, o, o, o), matrix[i][0][k - 1][0] + get_penalty4(o, o, a, o), matrix[i - 1][0][k - 1][0] + get_penalty4(string1[i - 1], o, string3[k - 1], o))
# #             for j in range(1, len2 + 1):
# #                 b = string2[j - 1]
# #                 c = string3[k - 1]
# #                 d = string4[l - 1]
# #                 
# #                 matrix[0][j][k][0] = max(matrix[0][j - 1][k][0] + get_penalty4(o, o, a, o), matrix[0][j][k - 1][0] + get_penalty4(o, a, o, o), matrix[0][j - 1][k - 1][0] + get_penalty4(o, string2[j - 1], string3[k - 1], o))
# #                 i - 0 - 0 - l
# #                 0 - j - 0 - l
# #                 ...
# #         for i in range(1, len1 + 1):
# #             for j in range(1, len2 + 1):
# #                 pass
#     
#     print_matrix4(matrix, string1, string2, string3, string4)
#     
#     for i in range(1, len1 + 1):
#         for j in range(1, len2 + 1):
#             for k in range(1, len3 + 1):
#                 a = string1[i - 1]
#                 b = string2[j - 1]
#                 c = string3[k - 1]
#                 o = "-"
#                 val = matrix[i - 1][j - 1][k - 1] + get_penalty3(a, b, c)
#                 val = max(val, matrix[i - 1][j - 1][k] + get_penalty3(a, b, o))
#                 val = max(val, matrix[i - 1][j][k - 1] + get_penalty3(a, o, c))
#                 val = max(val, matrix[i][j - 1][k - 1] + get_penalty3(o, b, c))
#                 val = max(val, matrix[i - 1][j][k] + get_penalty3(a, o, o))
#                 val = max(val, matrix[i][j - 1][k] + get_penalty3(o, b, o))
#                 val = max(val, matrix[i][j][k - 1] + get_penalty3(o, o, c))
#                 matrix[i][j][k] = val
#     print_matrix3(matrix, string1, string2, string3)
#     return matrix

