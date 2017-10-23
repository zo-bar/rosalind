'''
Created on Mar 7, 2013

@author: Zoya
'''
import urllib2
import io
import os

class Fasta_DNA:
    name = ''
    dna = ''
    def __str__(self):
        return self.name
    
def get_dna(uniport_id):
    response = urllib2.urlopen('http://www.uniprot.org/uniprot/' + uniport_id + '.fasta')
    html = response.read()
    dna = Fasta_DNA()
    dna.name = uniport_id
    for line in html.split("\n"):
        if not line.startswith(">"):
            dna.dna += line.rstrip()
    return dna

def find_motif(dna):
    result = []
    stream = io.StringIO(unicode(dna.dna))
    char = stream.read(1)
    while char:  # N{P}[ST]{P}
        if char == 'N':
            pos = stream.tell()
            if stream.read(1) != 'P':
                char = stream.read(1) 
                if char == 'T' or char == 'S':
                    if stream.read(1) != 'P':
                        result.append(pos)
            stream.seek(pos)
        char = stream.read(1)
    return result

def mprt(input_file_name, output_file_name):
    os.remove(output_file_name)
    with open(input_file_name) as input_file:
        line = input_file.readline().rstrip()
        while line:
            dna = get_dna(line)
            motif = find_motif(dna)
            if motif:
                with open(output_file_name, 'a') as output_file:
                    output_file.write(dna.name + '\n')
                    output_file.write(" ".join(str(position) for position in motif) + '\n')
            line = input_file.readline().rstrip()

mprt("data/rosalind_mprt.txt", "data/rosalind_mprt_result.txt")
