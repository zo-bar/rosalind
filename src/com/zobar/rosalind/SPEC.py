'''
Created on Jul 27, 2013

@author: Zoya
'''
from PRTM import amino_acid_mass

mass_amino_acid = {round(value, 2):key for key, value in amino_acid_mass.items()}
print mass_amino_acid

def SPEC(input_file, output_file):
    result = ''
    with open(input_file) as resource_file:
        mass1 = resource_file.readline().rstrip()
        mass2 = resource_file.readline().rstrip()
        while mass2:
            result += mass_amino_acid[round(float(mass2) - float(mass1), 2)]
            mass1 = mass2
            mass2 = resource_file.readline()
    with open(output_file, "w") as result_file:
        result_file.write(result)

# SPEC("data/rosalind_spec.txt", "data/rosalind_spec_result.txt")
