'''
Created on Sep 28, 2013

@author: Zoya
'''
from math import sqrt
def AFRQ(input_file, output_file):
    with open(input_file) as resource_file:
        lines = resource_file.readlines()
    qqs = []
    for line in lines:
        qqs.extend(line.split(" "))
    print (qqs)
    result = [2 * sqrt(float(q)) - float(q) for q in qqs]
    print (" ".join(str(round(qq, 3)) for qq in result))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(round(qq, 3)) for qq in result))
        
AFRQ("src/data/rosalind_afrq.txt", "src/data/rosalind_afrq_result.txt")
