'''
Created on Aug 13, 2013

@author: Zoya
'''

def CONV(input_file, output_file):
    sets = [line.strip() for line in open(input_file)]
    set1 = sets[0].split(" ")
    set2 = sets[1].split(" ")
#    print set1
#    print set2
    multiset = []
    for val1 in set1:
        for val2 in set2:
            multiset.append(round(round(float(val1), 5) - round(float(val2), 5), 5))
#    multiset.sort()
#    print multiset
    multiplicity = 1
    shift_value = multiset[0]
    for val in multiset:
        count = multiset.count(val)
        if count > multiplicity:
            shift_value = val
            multiplicity = count
#    print multiplicity
    with open(output_file, "w") as result_file:
        result_file.write(str(multiplicity))
        result_file.write("\n")
        result_file.write(str(shift_value))

CONV("src/data/rosalind_conv.txt", "src/data/rosalind_conv_result.txt")
