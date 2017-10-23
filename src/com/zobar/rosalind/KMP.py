'''
Created on Jul 23, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from time import gmtime, strftime

def KMP(input_file, output_file):
    dna = get_fasta_dna_list(open(input_file))[0].dna
    motifs = []
    result = [0 for i in range(len(dna))]
    for i, letter in enumerate(dna):
        for motif in motifs[:]:
            motifs.remove(motif)
            if letter != dna[motif]:
                for j in range(motif):
                    if result[i - j - 1] < motif - j:
                        result[i - j - 1] = motif - j 
            else:
                motifs.append(motif + 1)
        if i > 0 and letter == dna[0]:
            motifs.append(1)
        print (strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Letter %s (%d) done" % (letter, i))
    print (" ".join(str(x) for x in result))
    with open(output_file, "w") as result_file:
        result_file.write(" ".join(str(x) for x in result))

#    T_start_points = []
#    A_start_points = []
#    C_start_points = []
#    G_start_points = []
#    motifs = []
#    result = [0 for i in xrange(len(dna))]
#    for i, letter in enumerate(dna):
#        for motif in motifs[:]:
#            if (len(motif) < 1):
#                motifs.remove(motif)
#            elif letter != dna[motif[0] + motif[1]]:
#                if motif[1] > 1:
#                    for j in xrange(motif[1]):
#                        if result[i - j - 1] < motif[1] - j:
#                            result[i - j - 1] = motif[1] - j 
#                motifs.remove(motif)
#            else:
#                motif[1] = motif[1] + 1
#        if letter == 'T':
#            motifs.extend([[x, 1] for x in T_start_points])
#            T_start_points.append(i)
#        elif letter == 'A':
#            motifs.extend([[x, 1] for x in A_start_points])
#            A_start_points.append(i)
#        elif letter == 'C':
#            motifs.extend([[x, 1] for x in C_start_points])
#            C_start_points.append(i)
#        elif letter == 'G':
#            motifs.extend([[x, 1] for x in G_start_points])
#            G_start_points.append(i)
#        print strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " Letter %s (%d) done" % (letter, i)
#    print " ".join(str(x) for x in result)
#    with open(output_file, "w") as result_file:
#        result_file.write(" ".join(str(x) for x in result))

KMP("data/rosalind_kmp.txt", "data/rosalind_kmp_result.txt")
