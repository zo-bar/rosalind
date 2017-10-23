'''
Created on Aug 30, 2013

@author: Zoya
'''
from PRTM import amino_acid_mass
import math

mass_amino_acid = {value:key for key, value in amino_acid_mass.items()}
print mass_amino_acid

def FULL(input_file, output_file):
    with open(input_file) as resource_file:
        peptide_mass = float(resource_file.readline().rstrip())
        masses = [float(line.rstrip()) for line in resource_file.readlines()]
    masses.sort(key=float)
    print masses
    count = (len(masses) - 2) / 2
    result = ''
    last_mass = masses[0]
    for i in range(1, len(masses) / 2):
        mass_diff = masses[i] - last_mass
        for key in mass_amino_acid.iterkeys():            
            if math.fabs(key - mass_diff) < 0.00001:
                result += mass_amino_acid[key]
                for key1 in masses:
                    if math.fabs(key1 - peptide_mass + last_mass) < 0.00001:
                        masses.remove(key1)
                        break
                last_mass = masses[i]
                break
    for i in range(masses.index(last_mass) + 1, len(masses)):
        mass_diff = masses[i] - last_mass
        for key in mass_amino_acid.iterkeys():            
            if math.fabs(key - mass_diff) < 0.00001:
                result += mass_amino_acid[key]
                last_mass = masses[i]
                break
    print result
    print len(result) - count
    with open(output_file, "w") as result_file:
        result_file.write(result)

FULL("data/rosalind_full.txt", "data/rosalind_full_result.txt")
