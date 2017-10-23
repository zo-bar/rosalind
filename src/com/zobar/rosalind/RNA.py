'''
Created on Feb 26, 2013

@author: Zoya
'''
import io

def convertDNAtoRNAfromFile (inputFileName, outputFileName):
    with open(inputFileName) as dna:
        convertDNAtoRNA(dna, outputFileName)

def convertDNAtoRNAfromString(cons, outputFileName):
    dna = io.StringIO(cons);
    convertDNAtoRNA(dna)

def convertDNAtoRNA (stream, output_file_name):
    nchar = stream.read(1)
    with open(output_file_name, "w") as rna:
        while nchar:
            if nchar.upper() == 'T':
                nchar = 'U'
            rna.write(nchar)
            nchar = stream.read(1)

def convert_dna_rna(stream):
    nchar = stream.read(1)
    s = ''
    while nchar:
        if nchar.upper() == 'T':
            nchar = 'U'
        s += nchar
        nchar = stream.read(1)
    return s

def function_file(function, inputFileName, outputFileName):
    with open(outputFileName, "w") as outputFile:
        outputFile.write(function(open(inputFileName)))

# convertDNAtoRNAfromFile("data/rosalind_rna.txt", "data/rosalind_rna_result.txt")
# function_file(convert_dna_rna, "data/rosalind_rna.txt", "data/rosalind_rna_result.txt")
