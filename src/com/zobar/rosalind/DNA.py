'''
Created on Feb 26, 2013

@author: Zoya
'''
import io

def countDNAfromFile (fileName):
    with open(fileName) as dna:
        countDNA(dna)

def countDNAfromString(cons):
    dna = io.StringIO(cons);
    countDNA(dna)

def countDNA (stream):
    nchar = stream.read(1)
    a, c, t, g = 0, 0, 0, 0
    while nchar:
        if nchar.upper() == 'A':
            a += 1
        elif nchar.upper() == 'C':
            c += 1
        elif nchar.upper() == 'T':
            t += 1
        elif nchar.upper() == 'G':
            g += 1
        nchar = stream.read(1)
    stream.close()
    print ("A: %d" % a)
    print ("C: %d" % c)
    print ("T: %d" % t)
    print ("G: %d" % g)
    print ("%d %d %d %d" % (a, c, g, t))


