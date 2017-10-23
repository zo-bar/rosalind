'''
Created on Oct 3, 2013

@author: Zoya
'''
def shortest_common_superseq(string1, string2):
    len1 = len(string1)
    len2 = len(string2)
    matrix = [[0] * (len2 + 1) for x in range(len1 + 1)]
    for i in range(len1):
        for j in range(len2):
            if string1[i] == string2[j]:
                matrix[i + 1][j + 1] = matrix[i][j] + 1
            else:
                matrix[i + 1][j + 1] = max(matrix[i + 1][j], matrix[i][j + 1])
    
    i = len(string1)
    j = len(string2)
    result = ''
    while i > 0 and j > 0:
        if string1[i - 1] == string2[j - 1]:
            i -= 1
            j -= 1
            result = string1[i] + result
        elif matrix[i][j - 1] > matrix[i - 1][j]:
            j -= 1
            result = string2[j] + result
        else:
            i -= 1
            result = string1[i] + result
    while i > 0:
        i -= 1
        result = string1[i] + result
    while j > 0:
        j -= 1
        result = string2[j] + result
    print (result)
    return result

def SCSP(input_file, output_file):
    with open(input_file) as resource_file:
        dnas = resource_file.readlines()
    with open(output_file, "w") as result_file:
        result_file.write(shortest_common_superseq(dnas[0], dnas[1]))
        
SCSP("src/data/rosalind_scsp.txt", "src/data/rosalind_scsp_result.txt")
