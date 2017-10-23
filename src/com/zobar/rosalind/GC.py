'''
Created on Feb 28, 2013

@author: Zoya
'''

from __future__ import division
import io

def gcCount(dna):
    stream = io.StringIO(unicode(dna));
    nchar = stream.read(1)
    gc = 0
    total = 0
    while nchar:
        if nchar.upper() == 'C' or nchar.upper() == 'G':
            gc += 1
            total += 1
        elif nchar.upper() == 'A' or nchar.upper() == 'T':
            total += 1
        nchar = stream.read(1)
    
    result = 100 * gc / total
    return result
    
def gcCountLines(fileName):
    bestGCcontent = 0
    bestID = 0

    with open(fileName) as inputFile:
        # skip first >
        inputFile.read(1)
        dnaID = inputFile.readline()
        
        while dnaID:
            char = 'strat'
            dna = ''
            while char:
                char = inputFile.read(1)
                if char == '>':
                    break 
                dna = dna + char  
            gcContent = gcCount(dna)    
            if bestGCcontent < gcContent:
                bestGCcontent = gcContent
                bestID = dnaID
            dnaID = inputFile.readline()
    
    print "%s%f" % (bestID, bestGCcontent)

    

gcCountLines("data/rosalind_gc.txt")
            
            
