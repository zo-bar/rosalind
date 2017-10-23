'''
Created on Dec 16, 2013

@author: Zoya
'''
from math import factorial
def WFMD(input_file, output_file):
    with open(input_file) as resource_file:
        values = resource_file.readline().split(" ")
        N = int(values[0])
        m = int(values[1])
        g = int(values[2])
        k = int(values[3])
    
    with open(output_file, "w") as result_file:
        result_file.write(str(keep_rec_allele_probability(N, m, g, k)))
        
def keep_rec_allele_probability(N, m, g, k):
    P = [0.0 for l in range(2 * N + 1)]
    P[2 * N - m] = 1.0
    for gen in range(g):
        new_P = [0.0 for l in range(2 * N + 1)]
        for i in range(2 * N + 1):
            for j in range(2 * N + 1):
                p = (2 * N - j) * 1.0 / (2 * N)
#                if P[j] > 0:
#                    print "i=%d, j=%d, P[j]=%f, p=%f" % (i, j, P[j], p)
                new_P[i] += P[j] * (p ** (2 * N - i)) * ((1 - p) ** i) * (factorial(2 * N) / (factorial(i) * factorial(2 * N - i)))
        P = new_P
    result = round(sum(P[n] for n in range(k, 2 * N + 1)), 30) 
    print (result)
    return result

#WFMD("src/data/rosalind_wfmd.txt", "src/data/rosalind_wfmd_result.txt")
