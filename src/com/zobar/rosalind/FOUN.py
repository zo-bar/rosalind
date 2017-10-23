'''
Created on Nov 24, 2014

@author: zoya
'''
from math import log10, factorial
from WFMD import keep_rec_allele_probability

def FOUN(input_file, output_file):
    with open(input_file) as resource_file:
        values = resource_file.readline().split(" ")
        N = int(values[0])
        m = int(values[1])
        arr = [int(x) for x in resource_file.readline().split(" ")]
#     with open(output_file, "w") as result_file:
#         for i in range(1, m + 1):
#             new_arr = [(log10(1 - keep_rec_allele_probability(N, 2 * N - aj, i, 1))) for aj in arr]
#             print (" ".join(str(x) for x in new_arr))
#             result_file.write(" ".join(str(x) for x in new_arr) + "\n")
            # print (" ".join(str(log10(1 - keep_rec_allele_probability(N, 2 * N - aj, 1, 1))) for aj in arr))
    
    result = [[] for t in range(m)]
    for u in range(len(arr)):        
        P = [0.0 for l in range(2 * N + 1)]
        P[arr[u]] = 1.0
        for gen in range(m):
            new_P = [0.0 for l in range(2 * N + 1)]
            for i in range(2 * N + 1):
                for j in range(2 * N + 1):
                    p = (2 * N - j) * 1.0 / (2 * N)
    #                if P[j] > 0:
    #                    print "i=%d, j=%d, P[j]=%f, p=%f" % (i, j, P[j], p)
                    new_P[i] += P[j] * (p ** (2 * N - i)) * ((1 - p) ** i) * (factorial(2 * N) / (factorial(i) * factorial(2 * N - i)))
            P = new_P
            result[u].append(round(log10(1 - (sum(P[n] for n in range(1, 2 * N + 1)))), 12))
    print (result)
    result_line = "\n".join(" ".join(str(result[i][j]) for i in range(len(arr))) for j in range(len(result)))
    with open(output_file, "w") as result_file:
        result_file.write(result_line)
    
FOUN("src/data/rosalind_foun.txt", "src/data/rosalind_foun_result.txt")
