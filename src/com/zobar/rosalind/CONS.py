'''
Created on Mar 5, 2013

@author: Zoya
'''

def getDNAlist(file_name):
    result = []
    dna = ''
    with open(file_name) as dnafile:
        for line in dnafile.readlines():
            if not line.startswith(">"):
                if line:
                    dna += line.rstrip()
            elif dna:
                result.append(dna)
                dna = ''
    result.append(dna)
    return result

def get_matrix(list_dna):
    result = []
    for dna in list_dna:
        if not result:
            for i in range(len(dna)):
                result.append([0, 0, 0, 0])
        for i in range(len(dna)):
            if dna[i] == 'A':
                result[i][0] += 1
            elif dna[i] == 'C':
                result[i][1] += 1
            elif dna[i] == 'G':
                result[i][2] += 1
            elif dna[i] == 'T':
                result[i][3] += 1
    return result

def printMatrix(matrix):
    consensus = ''
    As = "A:"
    Cs = "C:"
    Gs = "G:"
    Ts = "T:"
    for freq in matrix:
        max_freq = freq[0]
        s = 'A'
        if freq[1] > max_freq:
            max_freq = freq[1]
            s = 'C'
        if freq[2] > max_freq:
            max_freq = freq[2]
            s = 'G'
        if freq[3] > max_freq:
            max_freq = freq[3]
            s = 'T'
        consensus += s
        As += " %d" % freq[0]
        Cs += " %d" % freq[1]
        Gs += " %d" % freq[2]
        Ts += " %d" % freq[3]
    with open("data/rosalind_cons_result.txt", "w") as output:
        output.write(consensus + "\n")
        output.write(As + "\n")
        output.write(Cs + "\n")
        output.write(Gs + "\n")
        output.write(Ts + "\n")
    print (consensus)
    print (As)
    print (Cs)
    print (Gs)
    print (Ts)
    
matrix = get_matrix(getDNAlist("data/rosalind_cons.txt"))
printMatrix(matrix)



