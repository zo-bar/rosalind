'''
Created on Feb 6, 2015

@author: zoya
'''
MASK = 2 << 11
import random


# def get_fingerprint(taxa, taxon):
#     result = (taxa.index(taxon) + 1) * 13  # | MASK  # * 13 * 17
#     return result

def cross_fingerprints(fing1, fing2):
    # print ("fing %s, with MASK %s" % (bin(fing1)[2:], bin(fing1 | MASK)[2:]))
    # print ("Crossing %d and %d - in binary: %s and %s - with MASK: %s and %s - result: %s" % (fing1, fing2, bin(fing1)[2:], bin(fing2)[2:], bin(fing1 | MASK)[2:], bin(fing2 | MASK)[2:], ((fing1 | MASK) ^ (fing2 | MASK))))
    return fing1 ^ fing2  # ((fing1 | MASK) ^ (fing2 | MASK))  # - MASK  # str(fing1).zfill(5) ^ str(fing2).zfill(5)

def get_fingerprints_list(taxa, taxa_dict, tree):
    # print ("Start processing %s" % tree)
    result = []
    last_symbol = ''
    taxon = ''
    taxa_stack = []
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    taxa_stack.append(taxa_dict[taxon])  # get_fingerprint(taxa, taxon))
                    # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                t1 = taxa_stack.pop()
                t2 = taxa_stack.pop()
                res = cross_fingerprints(t1, t2)  
                # print ("Cross top two fingerprints: %d and %d = %d" % (t1, t2, res))
                t = res
                result.append(t)
                taxa_stack.append(t)
            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
#     while (len(taxa_stack) > 1):
#         t = cross_fingerprints(taxa_stack.pop(), taxa_stack.pop())  
#         result.append(t)
#         taxa_stack.append(t)
    return result

def find_split_distance(taxa, tree1, tree2):
    # print (str(len(taxa)) + ' ' + ",".join(taxa))
    taxa_dict = {taxon:random.randint(0, 2 << 11) for taxon in taxa}
    # print(taxa_dict)
    
    
    fingerprints1 = sorted(get_fingerprints_list(taxa, taxa_dict, tree1))
    # print(fingerprints1)
    fingerprints2 = sorted(get_fingerprints_list(taxa, taxa_dict, tree2))
    # print(fingerprints2)

    
#     for fing1 in fingerprints1[:]:
#         if fingerprints2.count(fing1) > 0:
#             fingerprints2.remove(fing1)
#             fingerprints1.remove(fing1)
#     for fing2 in fingerprints2[:]:
#         if fingerprints1.count(fing2) > 0:
#             fingerprints1.remove(fing2)
#             fingerprints2.remove(fing2)
    # print (fingerprints1)
    # print (fingerprints2)    
#     result = len(fingerprints2)
#     result += len(fingerprints1)

#     shared = len([x for x in fingerprints1 if x in fingerprints2])
#     print ("Shared splits: %d" % shared)
#     result = 2 * (len(taxa) - 3) - 2 * shared
#     print ("Split distance: %d" % result)
#     
#     
#     print ("List diff test: %s" % ",".join(str(x) for x in [1,2,3,3]^[1,3]))
#     
#     print (len(fingerprints1))
#     print (len(fingerprints2))
#     other_way = len([x for x in fingerprints1 if x not in fingerprints2])
#     print (other_way)
#     other_way += len([x for x in fingerprints2 if x not in fingerprints1])
#     print (len([x for x in fingerprints2 if x not in fingerprints1]))
#     print ("Other way: %d" % other_way)

    shared = 0
    i = len(fingerprints1) - 1
    j = len(fingerprints2) - 1
    while i > -1 and j > -1:
        if fingerprints1[i] == fingerprints2[j]:
            # print ("Shared: %d" % fingerprints1[i])
            i -= 1
            j -= 1
            shared += 1
        elif  fingerprints1[i] > fingerprints2[j]:
            i -= 1
        elif fingerprints1[i] < fingerprints2[j]:
            j -= 1
    # print ("Shared %d" % shared)
    # print (i)
    # print(j)
    result = 2 * (len(taxa) - 3) - 2 * shared
    # print (result)
    return result

def SPTD(input_file, output_file):
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    # print (len(taxa))
    # print (MASK)
    # for i in range(len(taxa)):
    #    for j in range(i, len(taxa)):
    #        cross_fingerprints(get_fingerprint(taxa, taxa[i]), get_fingerprint(taxa, taxa[j]))
    tree1 = lines[1]
    tree2 = lines[2]
    max_result = 0
    for i in range (500):
        result = find_split_distance(taxa, tree1, tree2)
        if result > max_result:
            print ("Update result from %d to %d" % (max_result, result))
            max_result = result
    result = max_result
    
    shared = (len(taxa) - 3) - result / 2
    print (shared)
    
    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

SPTD("data/rosalind_qrtd1.txt", "data/rosalind_sptd_result.txt")



# tt = dict()
# def cross_fingerprints(fing1, fing2):
#     result = (fing1 + 10000000) ^ (fing2 + 10000000)
#     val = str(fing1) + ' ' + str(fing2)
#     if tt.get(result) and tt[result] != [val]:
#         tt[result].append(val)
#         print (format(fing1 + 1000000, 'b'))
#         print (format(fing2 + 1000000, 'b'))
#         
#         val1 = tt[result][0].split(' ')
#         print (format(int(val1[0]) + 1000000, 'b'))
#         print (format(int(val1[1]) + 1000000, 'b'))
#         
#         print(format(result, 'b'))
#         print (str(result) + ' ' + ",".join(tt[result]))
#     else:
#         tt[result] = [val]
#     return result

