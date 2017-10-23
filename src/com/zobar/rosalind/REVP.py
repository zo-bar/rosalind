'''
Created on Jul 1, 2013

@author: Zoya
'''

from com.zobar.rosalind.rosalind_utils import get_fasta_dna_list
from REVC import reverse_char

def revp(file_name, output_file_name):
    dna_list = get_fasta_dna_list(open(file_name))
    with open(file_name, 'w') as file_dna:
        file_dna.write(dna_list[0].dna)
    palindroms = get_reverse_palindroms(file_name)
    with open(output_file_name, 'w') as proteins_file:
        proteins_file.write("\n".join(palindroms))

def get_reverse_palindroms(file_name):
    result = []
    reflect_sites = []
    with open(file_name) as rna:
        k = rna.read(1)
        i = 1
        reverse_complement = ''
        while k:
            reverse_complement = (reverse_char(k) + reverse_complement)[:12]            
            for reflect_site in reflect_sites[:]:
                palindrome_len = (i - reflect_site) * 2
                if palindrome_len > 12:
                    reflect_sites.remove(reflect_site)
                    add_result(result, reflect_site, palindrome_len)
                elif len(reverse_complement) < palindrome_len or k != reverse_complement[palindrome_len - 1]:
                    reflect_sites.remove(reflect_site)
                    if (palindrome_len > 4):
                        add_result(result, reflect_site, palindrome_len)
            if (k == reverse_complement[1:2]):
                reflect_sites.append(i - 1) 
            k = rna.read(1)
            i = i + 1
        for reflect_site in reflect_sites:
            add_result(result, reflect_site, (i - reflect_site) * 2)
    return result

def add_result(result, reflect_site, max_len):
    for j in xrange(2, max_len / 2):
        result.append(str(reflect_site - j + 1) + " " + str(j * 2))

revp("data/rosalind_revp.txt", "data/rosalind_revp_result.txt")
