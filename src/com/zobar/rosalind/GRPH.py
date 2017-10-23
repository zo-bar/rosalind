'''
Created on Mar 6, 2013

@author: Zoya
'''
class Fasta_DNA:
    name = ''
    dna = ''
    
    def get_suffix(self):
        return self.dna[len(self.dna) - 3:len(self.dna)]
    
    def get_prefix(self):
        return self.dna[0:3]
    
    def __str__(self):
        return self.name

def read_input(file_name):
    result = []
    dna = ''
    dna_name = ''
    with open(file_name) as dnafile:
        for line in dnafile.readlines():
            if not line.startswith(">"):
                dna += line.rstrip()
            else:
                if dna:
                    fasta_dna = Fasta_DNA()
                    fasta_dna.name = dna_name
                    fasta_dna.dna = dna
                    result.append(fasta_dna)
                    dna = ''
                dna_name = line[1:len(line)].rstrip()
    fasta_dna = Fasta_DNA()
    fasta_dna.name = dna_name
    fasta_dna.dna = dna
    result.append(fasta_dna)
    return result
                    

def get_pref_suff_list(file_name):
    result = []
    dna_list = read_input(file_name)
    for dnapref in dna_list:
        for dnasuff in dna_list:
            if dnapref != dnasuff and dnapref.get_prefix() == dnasuff.get_suffix():
                result.append(dnasuff.name + " " + dnapref.name)
    return result

def make_pref_suff_list(input_file_name, output_file_name):
    pref_suff_list = get_pref_suff_list(input_file_name)
    with open(output_file_name, "w") as output:
        for s in pref_suff_list:
            output.write(s + "\n")
    
make_pref_suff_list("data/rosalind_grph.txt", "data/rosalind_grph_result.txt")    


# for dna in dna_list:
#    print dna.name + ":" + dna.dna + " - prefix: " + dna.get_prefix() + ", suffix: " + dna.get_suffix()
