'''
Created on Jul 17, 2013

@author: Zoya
'''
from com.zobar.rosalind.rosalind_utils import get_fasta_dna_list

def find_motif(sequence, motif):
    motifs = []
    for i, k in enumerate(sequence):
        for mot in motifs:
            if motif[len(mot)] == k:
                mot.append(str(i + 1))
                if len(mot) == len(motif):
                    return mot
        if k == motif[0]:
            motifs.append([str(i + 1)])

def sseq(input_file, output_file):
    dna_list = get_fasta_dna_list(open(input_file))
    sequence = dna_list[0].dna
    motif = dna_list[1].dna
    result = find_motif(sequence, motif)
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(result))
            
sseq("data/rosalind_sseq.txt", "data/rosalind_sseq_result.txt")

