'''
Created on Mar 7, 2013

@author: Zoya
'''
class Fasta_DNA:
    name = ''
    dna = ''
    
    def get_suffix(self, length):
        return self.dna[-length:]
    
    def get_prefix(self, length):
        return self.dna[0:length]
    
    def __str__(self):
        return self.name

def get_fasta_dna_list(dnaStream):
    result = []
    dna = ''
    dna_name = ''
    for line in dnaStream.readlines():
        if not line.startswith(">"):
            dna += line.rstrip()
        else:
            if dna:
                fasta_dna = Fasta_DNA()
                fasta_dna.name = dna_name
                fasta_dna.dna = dna
                result.append(fasta_dna)
                dna = ''
            dna_name = line[1:len(line)].rstrip()
    fasta_dna = Fasta_DNA()
    fasta_dna.name = dna_name
    fasta_dna.dna = dna
    result.append(fasta_dna)
    return result

def function_from_file(function, inputFileName, outputFileName):
    with open(outputFileName, 'w') as outputFile:
        outputFile.write(function(open(inputFileName)))

def modulo(number, mod):
    return number % mod
