'''
Created on Jul 27, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list
from REVC import REVCfromString, reverse_char

def check_equal(dna1, dna2, max_errors):
    result = True
    error_count = 0
    for i, letter in enumerate(dna1):
        if letter != dna2[i]:
            error_count += 1
            if error_count > max_errors:
                result = False
                break        
    return result

def check_reverse_equal(dna1, dna2, max_errors):
    error_count = 0
    result = True
    for i, letter in enumerate(dna1):
        reverce_letter = dna2[-1:]
        if i > 0:
            reverce_letter = dna2[-i - 1:-i]
        if letter != reverse_char(reverce_letter):
            error_count += 1
            if (error_count > max_errors):
                result = False
                break        
    return result

def CORR(input_file, output_file):
    dnas = get_fasta_dna_list(open(input_file))
    correct_reads = []
    in_work_reads = []
    for dna in dnas:
        found = False
        for read in correct_reads:
            if check_equal(dna.dna, read, 0) or check_reverse_equal(dna.dna, read, 0):
                found = True
                break
        if found:
            continue     
        for read in in_work_reads:
            if check_equal(dna.dna, read, 0) or check_reverse_equal(dna.dna, read, 0):
                correct_reads.append(dna.dna)
                in_work_reads.remove(read)
                found = True
                break
        if found:
            continue
        in_work_reads.append(dna.dna)
    result = []
    for in_work_read in in_work_reads:
        for correct_read in correct_reads:
            if check_equal(in_work_read, correct_read, 1):
                result.append(str(in_work_read) + "->" + str(correct_read))
                break
            if check_reverse_equal(in_work_read, correct_read, 1):
                result.append(str(in_work_read) + "->" + REVCfromString(unicode(str(correct_read))))
                break
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(result))
            
CORR("data/rosalind_corr.txt", "data/rosalind_corr_result.txt")
