'''
Created on Mar 4, 2013

@author: Zoya
'''
import io

def subs(dna1, dna2):    
    stream1 = io.StringIO(unicode(dna1))
    stream2 = io.StringIO(unicode(dna2))
    chr1 = stream1.read(1)
    chr2 = stream2.read(1)
    
    result = []
    
    while chr1:
        if chr1 == chr2:
            pos = stream1.tell()
            
            while chr1 and chr2 and chr1 == chr2:
                chr1 = stream1.read(1)
                chr2 = stream2.read(1)
            
            if not chr2:
                result.append(pos)
            
            stream1.seek(pos)
            
            stream2.seek(0)
            chr2 = stream2.read(1)
            
        chr1 = stream1.read(1)
    
    return result
                

def findSubs(fileName):
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
        
    return subs(dna1, dna2)

print ' '.join(str(num) for num in findSubs("data/rosalind_subs.txt"))
