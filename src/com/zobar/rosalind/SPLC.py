'''
Created on Mar 11, 2013

@author: Zoya
'''

import io
from com.zobar.rosalind.rosalind_utils import get_fasta_dna_list, function_from_file
from com.zobar.rosalind.SUBS import subs
from com.zobar.rosalind.PROT import prot
from com.zobar.rosalind.RNA import convert_dna_rna

def remove_introns(stream):
    dnaList = get_fasta_dna_list(stream)
    dna = dnaList[0].dna
    protList = [protein for protein in dnaList if protein.dna != dna]
    for protein in protList:
        positions = subs(dna, protein.dna)
        for pos in positions:
            dna = dna[0:pos - 1] + dna[pos + len(protein.dna) - 1 :]
    return dna
    
def get_protein(stream):
    dna = remove_introns(stream)
    rna = convert_dna_rna(io.StringIO(unicode(dna)))
    protein = prot(io.StringIO(unicode(rna)))
    return protein

function_from_file(get_protein, "data/rosalind_splc.txt", "data/rosalind_splc_result.txt")
