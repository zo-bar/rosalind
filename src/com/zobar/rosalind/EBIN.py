'''
Created on Nov 6, 2014

@author: zoya
'''
import os

print(os.path.abspath("yyy"))
def EBIN(input_file, output_file):
    with open(input_file) as resource_file:
        values = resource_file.readlines()
        N = int(values[0])
        m = [float(x) for x in values[1].split(" ")]
    print(N)
    print(m)
    result=[round(N*y, 3) for y in m]
    print (" ".join(str(x) for x in result))
        
EBIN("data/rosalind_ebin.txt", "src/data/rosalind_ebin_result.txt")