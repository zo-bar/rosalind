'''
Created on Jul 11, 2013

@author: Zoya
'''
amino_acid_mass = {
               "A":   71.03711,
               "C":   103.00919,
               "D":   115.02694,
               "E":   129.04259,
               "F":   147.06841,
               "G":   57.02146,
               "H":   137.05891,
               "I":   113.08406,
               "K":   128.09496,
               "L":   113.08406,
               "M":   131.04049,
               "N":   114.04293,
               "P":   97.05276,
               "Q":   128.05858,
               "R":   156.10111,
               "S":   87.03203,
               "T":   101.04768,
               "V":   99.06841,
               "W":   186.07931,
               "Y":   163.06333
               }

h2o_mass = 18.01056

def get_protein_mass(stream):
    protein_mass = 0
    protein_len = 0
    peptide = stream.read(1)
    while peptide:
        if (peptide != "\n"):
                protein_mass = protein_mass + amino_acid_mass[peptide]
                protein_len = protein_len + 1
        # print "Next peptide: %s - %d. Total mass: %d, length: %d" % (peptide, amino_acid_mass[peptide], protein_mass, protein_len)
        peptide = stream.read(1)
    # protein_mass = protein_mass - (h2o_mass * (protein_len - 1))
    return protein_mass

def prtm(input_file, output_file):
    with open(input_file) as protein:
        with open(output_file, "w") as result_file:
            result_file.write(str(get_protein_mass(protein)))
    
# prtm("data/rosalind_prtm.txt", "data/rosalind_prtm_result.txt")
