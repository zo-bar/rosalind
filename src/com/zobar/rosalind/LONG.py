'''
Created on Jul 20, 2013

@author: Zoya
'''
from rosalind_utils import get_fasta_dna_list

def find_overlap(string1, string2):
    distances = []
    for i, k in enumerate(string1):
        for distance in distances[:]:
            if k != string2[i - distance]:
                distances.remove(distance)
        if k == string2[0]:
            distances.append(i)
    if len(distances) > 0:
        return len(string1) - distances[0]
    return 0

def find_superstring(dna_list):
    start_points = []
    end_points = []
    for fasta_dna1 in dna_list:
        isFirst = True
        for fasta_dna2 in dna_list:
            if fasta_dna1 != fasta_dna2:
                distance = find_overlap(fasta_dna2.dna, fasta_dna1.dna)
                if (distance > (len(fasta_dna1.dna) / 2)):
                    start_points.append(fasta_dna2)
                    end_points.append([fasta_dna1, distance])
                    isFirst = False
                    break
        if isFirst:
            first = fasta_dna1

    superstring = first.dna
    end_point = [first, 0]
    while (start_points.count(end_point[0]) > 0):
        end_point = end_points[start_points.index(end_point[0])]
        superstring = superstring + end_point[0].dna[end_point[1]:]
    return superstring

def LONG(input_file, output_file):
    dna_list = get_fasta_dna_list(open(input_file))
    with open(output_file, "w") as result_file:
        result_file.write("".join(find_superstring(dna_list)))
    
# LONG("data/rosalind_long.txt", "data/rosalind_long_result.txt")

# def find_overlap(string1, string2):
#    distances = []
#    for i, k in enumerate(string1):
#        for distance in distances[:]:
#            if (len(string2) <= (i - distance)):
#                return len(string2)
#            if k != string2[i - distance]:
#                distances.remove(distance)
#        if k == string2[0]:
#            distances.append(i)
#    if len(distances) > 0:
#        return len(string1) - distances[0]
#    return 0
#
# def append_next_string(superstring, dna_list):
#    if len(dna_list) == 0:
#        return True
#    for dna in dna_list:
#        overlap = find_overlap("".join(superstring), dna.dna)
#        if  overlap > len(dna.dna) / 2:
#            if (overlap < len(dna.dna)):
#                superstring.append(dna.dna[overlap:].rstrip())
#            # print "Appended %s. Superstring - %s" % (dna.dna, "".join(superstring))
#            if (append_next_string(superstring, [x for x in dna_list if x != dna])):
#                return True
#    # print "Unable to add to %s any of DNA" % ("".join(superstring)) 
#    return False
#
# def LONG(input_file, output_file):
#    dna_list = get_fasta_dna_list(open(input_file))
#    for dna in dna_list:
#        # print "Process next dna  - %s" % dna.dna
#        superstring = [dna.dna.rstrip()]
#        if append_next_string(superstring, [x for x in dna_list if x != dna]):
#            break
#    with open(output_file, "w") as result_file:
#        result_file.write("".join(superstring))

# def find_shortest_distance(input_file):
#    pass
#
# def find_distance(string1, string2):
#    distances = []
#    for i, k in enumerate(string1):
#        for distance in distances[:]:
#            if k != string2[i - distance]:
#                distances.remove(distance)
#        if k == string2[0]:
#            distances.append(i)
#    if len(distances) > 0:
#        return distances[0]
#    return len(string1)
#
# def find_distances(dna_list, output_file):
#    with open(output_file, "w") as temp_file:
#        for fasta_dna1 in dna_list:
#            for fasta_dna2 in dna_list:
#                if fasta_dna1 != fasta_dna2:
#                    temp_file.write(fasta_dna1.name + " " + fasta_dna2.name + " " + str(find_distance(fasta_dna1.dna, fasta_dna2.dna)) + "\n")
#
# def LONG(input_file, output_file):
#    dna_list = get_fasta_dna_list(open(input_file))
#    temp_file = output_file + "t"
#    find_distances(dna_list, temp_file)
