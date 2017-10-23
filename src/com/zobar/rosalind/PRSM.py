'''0
Created on Oct 3, 2013

@author: Zoya
'''
from PRTM import amino_acid_mass
from time import gmtime, strftime

def get_multiplicity(set1, set2):
    multiset = []
    for val1 in set1:
        for val2 in set2:
            multiset.append(round(round(float(val1), 5) - round(float(val2), 5), 5))
    multiplicity = 1
#    shift = 0
    for val in multiset:
        count = multiset.count(val)
        if count > multiplicity:
#            print "Val %f counts %d times " % (val, count)
            multiplicity = count
#            shift = val
#    if multiplicity > 20:
#        set3 = []
#        for mass in set1:
#            set3.append(mass - shift)
#        set2.sort()
#        set3.sort()
#        print set2
#        print set3
    return multiplicity

def PRSM(input_file, output_file):
    with open(input_file) as resource_file:
        lines = resource_file.readlines()
    n = int(lines[0])
    proteins = [line.rstrip() for line in lines[1:n]]
    set1 = [float(line.rstrip()) for line in lines[n + 1:]]
    max_multiplicity = 1
    best_protein = proteins[0]
    for protein in proteins:
        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Start protein: %s" % protein
        set2 = []
        val = 0
        for peptide in protein:
            set2.append(amino_acid_mass[peptide] + val)
            val = set2[-1]
        set2.pop()
        for i in xrange(len(protein) - 1):
            set2.append(val - amino_acid_mass[protein[i]])
            val = set2[-1]
                        
        multiplicity = get_multiplicity(set1, set2)
        print multiplicity
        if multiplicity > max_multiplicity:
            max_multiplicity = multiplicity
            best_protein = protein
    
    print max_multiplicity
    print best_protein
    
    with open(output_file, "w") as result_file:
        result_file.write(str(max_multiplicity))
        result_file.write("\n")
        result_file.write(str(best_protein))

PRSM("src/data/rosalind_prsm.txt", "src/data/rosalind_prsm_result.txt")