'''
Created on Mar 5, 2013

@author: Zoya
'''

RNAcodon = {
          "UUU": "F",
          "UUC": "F",
          "UUA": "L",
          "UUG": "L",
          "UCU": "S",
          "UCC": "S",
          "UCA": "S",
          "UCG": "S",
          "UAU": "Y",
          "UAC": "Y",
          "UAA": "Stop",
          "UAG": "Stop",
          "UGU": "C",
          "UGC": "C",
          "UGA": "Stop",
          "UGG": "W",
          
          "CUU": "L",
          "CUC": "L",
          "CUA": "L",
          "CUG": "L",
          "CCU": "P",
          "CCC": "P",
          "CCA": "P",
          "CCG": "P",
          "CAU": "H",
          "CAC": "H",
          "CAA": "Q",
          "CAG": "Q",
          "CGU": "R",
          "CGC": "R",
          "CGA": "R",
          "CGG": "R",
          
          "AUU": "I",
          "AUC": "I",
          "AUA": "I",
          "AUG": "M",
          "ACU": "T",
          "ACC": "T",
          "ACA": "T",
          "ACG": "T",
          "AAU": "N",
          "AAC": "N",
          "AAA": "K",
          "AAG": "K",
          "AGU": "S",
          "AGC": "S",
          "AGA": "R",
          "AGG": "R",
          
          "GUU": "V",
          "GUC": "V",
          "GUA": "V",
          "GUG": "V",
          "GCU": "A",
          "GCC": "A",
          "GCA": "A",
          "GCG": "A",
          "GAU": "D",
          "GAC": "D",
          "GAA": "E",
          "GAG": "E",
          "GGU": "G",
          "GGC": "G",
          "GGA": "G",
          "GGG": "G"
          } 

def prot(stream):
    s = ''
    codon = stream.read(3)
    while codon:
        rnacodon = RNAcodon[codon]
        if rnacodon == "Stop":
            break
        s = s + rnacodon
        codon = stream.read(3)
    return s

def rna_to_protein(input_file, output_file):
    with open(input_file) as rna:
        with open(output_file, "w") as result_file:
            result_file.write(prot(rna))
    
    
# rna_to_protein("data/rosalind_prot.txt", "data/rosalind_prot_result.txt")

# import io
# print prot(io.StringIO(unicode("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA")))
