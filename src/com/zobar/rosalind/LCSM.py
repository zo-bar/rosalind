'''
Created on Jun 26, 2013

@author: Zoya
'''
from com.zobar.rosalind.rosalind_utils import get_fasta_dna_list, function_from_file
from SuffixTree import find_longest_common_substring

def find_longest_common_string(stream):
    dnaList = get_fasta_dna_list(stream)
    return find_longest_common_substring([dna.dna for dna in dnaList])

function_from_file(find_longest_common_string, "data/rosalind_lcsm.txt", "data/rosalind_lcsm_result.txt")
