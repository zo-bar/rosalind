'''
Created on Mar 14, 2013

@author: Zoya
'''

from com.zobar.rosalind.PROT import RNAcodon
from rosalind_utils import modulo
from rosalind_utils import function_from_file

def RNA_to_prot_number(stream):
    protein = stream.read(1)
    result = 1
    while protein:
        if protein != '\n':
            result = result * len([value for value in RNAcodon.values() if value == protein])
        protein = stream.read(1)
    result = result * len([value for value in RNAcodon.values() if value == "Stop"])
    return str(modulo(result, 1000000))

function_from_file(RNA_to_prot_number, "data/rosalind_mrna.txt", "data/rosalind_mrna_result.txt")
