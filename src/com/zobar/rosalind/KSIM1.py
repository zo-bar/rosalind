'''
Created on Feb 12, 2016

@author: zoya
'''
from time import gmtime, strftime
MATCH_SCORE = 0
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
    print (len1)
    print (len2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    # matrix[0] = [i * MISMATCH_SCORE for i in range(len(matrix[0]))]
    # for i in range(len(matrix)):
    #    matrix[i][0] = i * MISMATCH_SCORE
    print (strftime("%Y-%m-%d %H:%M:%S Motif len:", gmtime()) + str(len1 + 1))
    for i in range(1, len1 + 1):
        if not test_mode and i % 1000 == 0: print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
    
        for j in range(1, len2 + 1):
            matrix[i][j] = max(matrix[i - 1][j] + (MISMATCH_SCORE if j < len2 + 1 else 0), matrix[i][j - 1] + MISMATCH_SCORE, matrix[i - 1][j - 1] + (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE))
    if test_mode: print_matrix(matrix, string1, string2)
    return matrix

def get_alignment_stack(string1, string2, matrix, result1, result2, i, j, result, stack):
    if j <= 0 or i <= 0:
        if i == 0:
            if test_mode: print ("i: %d, j: %d, reslut1: %s, result2: %s, result: %d" % (i, j, result1, result2, len(result2) - result2.count('-')))
            result.append((j + 1, len(result2) - result2.count('-')))
    else:
        if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
            stack.append((string1, string2, matrix, string1[i - 1] + result1, string2[j - 1] + result2, i - 1, j - 1, result, stack))
        if matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE if j > 0 and j < len(string2) + 1 else 0):
            stack.append((string1, string2, matrix, string1[i - 1] + result1, '-' + result2, i - 1, j, result, stack))
        if matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
            stack.append((string1, string2, matrix, '-' + result1, string2[j - 1] + result2, i, j - 1, result, stack))
    
def get_recursive_alignment(string1, string2, matrix, result1, result2, i, j, result):
    if j <= 0 or i <= 0:
        if i == 0:
            print ("i: %d, j: %d, reslut1: %s, result2: %s, result: %d" % (i, j, result1, result2, len(result2) - result2.count('-')))
            result.append((j + 1, len(result2) - result2.count('-')))
        return
    if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
        get_recursive_alignment(string1, string2, matrix, string1[i - 1] + result1, string2[j - 1] + result2, i - 1, j - 1, result)
    if matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE if j > 0 and j < len(string2) + 1 else 0):
        get_recursive_alignment(string1, string2, matrix, string1[i - 1] + result1, '-' + result2, i - 1, j, result)
    if matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
        get_recursive_alignment(string1, string2, matrix, '-' + result1, string2[j - 1] + result2, i, j - 1, result)        

def get_alignement(string1, string2, matrix, j):
    i = len(string1)
    result1 = ''
    result2 = ''
    while (i > 0 and j > 0):
        if matrix[i - 1][j - 1] == matrix[i][j] - (MISMATCH_SCORE if string1[i - 1] != string2[j - 1] else MATCH_SCORE):
            result1 = string1[i - 1] + result1
            result2 = string2[j - 1] + result2
            i -= 1
            j -= 1
        elif matrix[i - 1][j] == matrix[i][j] - (MISMATCH_SCORE if j > 0 and j < len(string2) + 1 else 0):
            result1 = string1[i - 1] + result1
            result2 = '-' + result2
            i -= 1
        elif matrix[i][j - 1] == matrix[i][j] - MISMATCH_SCORE:
            result1 = '-' + result1
            result2 = string2[j - 1] + result2
            j -= 1
        else:
            print ("Error! Unable to trace back")
            print (result1)
            print(result2)
    if test_mode: print ("Aligning start at %d" % j)
    if test_mode: print (result1)
    if test_mode: print (result2)
    return len(result2) - result2.count('-')
    
def KSIM(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S Start KSIM", gmtime())) 
    
    with open(input_file) as resource:
        k = int(resource.readline().rstrip())
        s = resource.readline().rstrip()
        t = resource.readline().rstrip()
    if test_mode: print ("k: %d, s:%s, t:%s" % (k, s, t))
    
    # for test:
    # matrix = create_distance_matrix(t, s)
    matrix = create_distance_matrix(s, t)
    print (strftime("%Y-%m-%d %H:%M:%S Matrix done", gmtime())) 
    
    n = len(s)
    m = len(t)
    result = []
    stack = []
            
    for j in range(n - 2, m + 1):
        if test_mode: print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(j)) 
    
        if matrix[n][j] >= -k:
            # v1
#             str_len = get_alignement(s, t, matrix, j)
#             result.append((j - str_len + 1, str_len))
            
            # v2
            get_recursive_alignment(s, t, matrix, '', '', len(s), j, result)
            
            # v3
#            get_alignment_stack(s, t, matrix, '', '', len(s), j, result, stack)

    counter = 0
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Init stack completed")
    while (len(stack) > 0):
        el = stack.pop()
        get_alignment_stack(el[0], el[1], el[2], el[3], el[4], el[5], el[6], el[7], el[8])
        if not test_mode and counter % 1000000 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Processing stack %d, stack len: %d, i: %d, j:%d, result len: %d" % (counter, len(stack), el[5], el[6], len(result)))
        counter += 1
    
    result = sorted(set(result))    
    if test_mode: print ('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in result))
    with open(output_file, "w") as result_file:
        result_file.write('\n'.join(str(r[0]) + ' ' + str(r[1]) for r in result))
 
# test_mode = False      
KSIM("data/rosalind_ksim_test.txt", "data/rosalind_ksim1_result.txt")
