'''
Created on Aug 13, 2013

@author: Zoya
'''
'''
Created on Aug 12, 2013

@author: Zoya
'''
from REVC import reverse_char

def add_complement(dnas):
    result = set()
    for dna in dnas:
        reversed_dna = ''
        for letter in reversed(dna):
            reversed_dna += reverse_char(letter)
        result.add(reversed_dna)
    result.update(dnas)
    return list(result)

def DBRU(input_file, output_file):
    result = [line.strip() for line in open(input_file)]
    result = add_complement(result)
    result.sort()
    with open(output_file, "w") as result_file:
        result_file.write("\n".join("(" + x[:-1] + ", " + x[1:] + ")" for x in result))
            
DBRU("src/data/rosalind_dbru.txt", "src/data/rosalind_dbru_result.txt")


# def get_edges(dna, result):
#    result.append([dna[:len(dna) - 1], dna[1:]])
#    reversed_dna = ''
#    for letter in reversed(dna):
#        reversed_dna += reverse_char(letter)
#    result.append([reversed_dna[:len(dna) - 1], reversed_dna[1:]])

#    result.sort()
#    for i, dna in enumerate(result):
#        if i > 0 and result[i - 1] == dna:
#            result.remove(dna)
