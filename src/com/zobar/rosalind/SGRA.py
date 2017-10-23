'''
Created on Oct 6, 2013

@author: Zoya
'''
from PRTM import amino_acid_mass
import math

mass_amino_acid = {value:key for key, value in amino_acid_mass.items()}
# print mass_amino_acid

def SGRA(input_file, output_file):
    with open(input_file) as resource_file:
        masses = [float(line.rstrip()) for line in resource_file.readlines()]
    masses.sort(key=float)
    max_peptide_weight = max(mass_amino_acid)
    
    proteins = ['' for i in xrange(len(masses))]
    for i in xrange(len(masses)):
        for j in xrange(i):
            mass_diff = masses[i] - masses[j]
            if mass_diff > max_peptide_weight:
                continue
            for key in mass_amino_acid.iterkeys():            
                if math.fabs(key - mass_diff) < 0.00005:
                    prot = proteins[j] + mass_amino_acid[key]
                    if len(prot) > len(proteins[i]):
                        proteins[i] = prot
    print proteins
    result = max(proteins, key=len)
    print result

SGRA("src/data/rosalind_sgra.txt", "src/data/rosalind_sgra_result.txt")
