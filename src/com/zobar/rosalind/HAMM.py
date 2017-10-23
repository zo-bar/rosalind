'''
Created on Feb 28, 2013

@author: Zoya
'''

import io

def hamm(dna1, dna2):
    # print dna1
    # print dna2
    count = 0
    
    stream1 = io.StringIO(unicode(dna1))
    stream2 = io.StringIO(unicode(dna2))
    chr1 = stream1.read(1)
    chr2 = stream2.read(1)
    
    while chr1 and chr2:
        if chr1 != chr2:
            count += 1
        chr1 = stream1.read(1)
        chr2 = stream2.read(1)
    
    # print count
    return count
        
def countHamm(fileName):
    with open(fileName) as inputFile:
        char = inputFile.read(1)
        dna1 = ''
        dna2 = ''
        while char != "\n":
            dna1 = dna1 + char
            char = inputFile.read(1)
        char = inputFile.read(1)
        while char:
            dna2 = dna2 + char
            char = inputFile.read(1)
        
    hamm(dna1, dna2)

countHamm("data/rosalind_hamm.txt")
