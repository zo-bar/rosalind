'''
Created on Mar 15, 2013

@author: Zoya
'''
from com.zobar.rosalind.PROT import RNAcodon
from com.zobar.rosalind.RNA import convertDNAtoRNAfromFile
from com.zobar.rosalind.REVC import REVCfromFile
import os

from com.zobar.rosalind.rosalind_utils import get_fasta_dna_list

def orf(file_name, output_file_name):
    dna_list = get_fasta_dna_list(open(file_name))
    with open(file_name, 'w') as file_dna:
        file_dna.write(dna_list[0].dna)
        
    temp_rna_file = "data/temp_rna.txt"
    convertDNAtoRNAfromFile(file_name, temp_rna_file)
    temp_rna_revc_file = "data/temp_rna_revc.txt"
    REVCfromFile(file_name, temp_rna_revc_file)
    convertDNAtoRNAfromFile(temp_rna_revc_file, temp_rna_revc_file)
    
    proteins = set(get_proteins(temp_rna_file) + get_proteins(temp_rna_revc_file))
    
    with open(output_file_name, 'w') as proteins_file:
        proteins_file.write("\n".join(proteins))
    
    os.remove(temp_rna_file)
    os.remove(temp_rna_revc_file)
    
def get_proteins(file_name):
    result = []
    with open(file_name) as rna:
        codon = rna.read(3)
        frames = [[] for tuit in xrange(3)]
        k = rna.read(1)
        i = 0
        while k:
            codon = codon[1:] + k
            if RNAcodon[codon] == 'Stop':
                result.extend(frames[i % 3])
                frames[i % 3] = []
            else:
                for j, protein in enumerate(frames[i % 3]):
                    frames[i % 3][j] = protein + RNAcodon[codon]
                if RNAcodon[codon] == 'M':
                    frames[i % 3].append(RNAcodon[codon])
            k = rna.read(1)
            i = i + 1
    return result

orf("data/rosalind_orf.txt", "data/rosalind_orf_result.txt")
