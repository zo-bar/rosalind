'''
Created on Oct 6, 2013

@author: Zoya
'''
from math import fabs, factorial

def MMCH(input_file, output_file):
    with open(input_file) as resource_file:
        resource_file.readline()
        next_line = resource_file.readline()
        rna = ''
        while next_line:
            rna += next_line.rstrip()
            next_line = resource_file.readline()            
    print (rna)
    
    As = rna.count('A')
    Us = rna.count('U')
    Cs = rna.count('C')
    Gs = rna.count('G')
    print ("A: %d, U: %d, C: %d, G: %d" % (As, Us, Cs, Gs))
    
    result = (factorial(max(As, Us)) / factorial(fabs(As - Us))) * (factorial(max(Cs, Gs)) / factorial(fabs(Cs - Gs)))
    print (result)
    
MMCH("src/data/rosalind_mmch.txt", "src/data/rosalind_mmch_result.txt")
