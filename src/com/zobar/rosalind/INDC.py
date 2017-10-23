'''
Created on Sep 20, 2013

@author: Zoya
'''
from math import log10, factorial

def probability_of_sharing(n, k):
    result = ((0.5) ** n) * factorial(n) / (factorial(n - k) * factorial(k))  # + probability_of_sharing(n, k + 1)
    return result

def INDC(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    n = 2 * int(lines[0])
    result = [probability_of_sharing(n, k) for k in range(1, n + 1)]
    for i in range(len(result) - 2, -1, -1):
        result[i] += result[i + 1]
    print (result)
    print (" ".join(str(round(log10(x), 3)) for x in result))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(round(log10(x), 3)) for x in result))
            
INDC("src/data/rosalind_indc.txt", "src/data/rosalind_indc_result.txt")

