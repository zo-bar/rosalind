'''
Created on Jan 13, 2016

@author: zoya
'''

from time import gmtime, strftime

class Edge:
    def __init__(self, fingerprint, left_pairs, right_pairs):
        self.f = fingerprint
        self.left_pairs = left_pairs
        self.right_pairs = right_pairs
   
def cross_left_right_pairs(left_pairs, right_pairs, result):
    for l in left_pairs:
        for r in right_pairs:
#             print (bin(l + r)[2:])
#             if bin(l + r).count('1') != 4:
#                 print (bin(l))
#                 print (bin(r))
#                 print("HERE")
            if l > r:
                result[l + r] = l
            else:
                result[l + r] = r
 
def cross_pairs(e1, e2, taxa, result, l):
    print ("Cross edges %d and %d" % (e1.f, e2.f))
    left_pairs = get_new_left_pairs(e1, e2, l)
    left_pairs.extend(e1.left_pairs)
    left_pairs.extend(e2.left_pairs)
    print ("all new left pairs: " + ",".join(bin(x)[2:] for x in left_pairs))
    right_pairs = get_right_pairs(e1, e2, l)
    print ("all new right pairs: " + ",".join(bin(x)[2:] for x in right_pairs))
    
    cross_left_right_pairs(left_pairs, right_pairs, result)
    
    e = Edge (e1.f + e2.f, left_pairs, right_pairs)
    
    return e

def get_all_pairs(l):
    all_pairs = []
#     for i in range(1, l + 1):
#         if bin(i).count('1') == 1:
#             for j in range(i+1, l + 1):
#                 if bin(j).count('1') == 1:
#                     all_pairs.append(i + j)
#     print (",".join(bin(x)[2:] for x in all_pairs))
#     return all_pairs
    for i in range(2 ** l):
        if bin(i).count('1') == 2:
            all_pairs.append(i)
    #print (",".join(bin(x)[2:] for x in all_pairs))
    return all_pairs

def get_new_left_pairs(e1, e2, l):
    new_left = []
    t1_list = []
    t2_list = []
    for i in range(1, l + 1):
        if (e1.f & i) == i:
            t1_list.append(i)
            for j in t2_list:
                new_left.append(i + j)
        elif (e2.f & i) == i:
            t2_list.append(i)
            for j in t1_list:
                new_left.append(i + j)
    print ("New left pairs (merging edges %s and %s): " % (bin(e1.f)[2:], bin(e2.f)[2:]) + ",".join(bin(x)[2:] for x in new_left))
    return new_left

def get_right_pairs(e1, e2, l):
    exclude_right = []
    old_right = set(e1.right_pairs + e2.right_pairs)
    for i in range(1, l + 1):
        # if i was in either t1 or t2, exclude all right pairs containing i
        if e2.f & i == i or e2.f & i == i:
            for right in old_right:
                if right & i == i:
                    exclude_right.append(right)
    new_right = [x for x in old_right if x not in exclude_right]
    return new_right

def get_pairs_list(taxa, tree):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing %s" % tree)
    print (len(taxa))
    last_symbol = ''
    taxon = ''
    edge_stack = []
    
    counter = 0
    
    result = dict()
    
    l = len(taxa)
    all_right_pairs = get_all_pairs(l)
    
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    # still includes right pairs containing taxa, but will exclude them with the first cross
                    e = Edge(taxa.index(taxon) + 1, [], all_right_pairs)
                    
                    edge_stack.append(e)
                      
                    counter += 1
                    if counter % 100 == 0:
                        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
                    # print ("Add to edge_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                e1 = edge_stack.pop()
                e2 = edge_stack.pop()
                
                e = cross_pairs(e1, e2, taxa, result, l)
                
                edge_stack.append(e)
                
            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
    
    return result

def count_ones(num, l):
    return (bin(num).count('1'))
    
def add_shared_quart(f1, f2, shared_quartets, l):
    group1 = 2 ** l - 1 - (f1 | f2)
    group2 = (f1 & f2)
    
    if count_ones(group1, l) > 1 and count_ones(group2, l) > 1:
    
        # print ("Start pairing %d and %d" % (group1, group2))
        
        pairs1 = get_pairs_list(group1, l)
        pairs2 = get_pairs_list(group2, l)
        
        shared_quartets.extend([p1 + p2 for p1 in pairs1 for p2 in pairs2])
        # print (len(shared_quartets))
    return
    
def count_shared_quartets(taxa, fps1, fps2):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start counting shared quartets count...")
    shared_quartets_count = 0
    print ("Total shared quartets count:%d" % shared_quartets_count)
    return shared_quartets_count
    
def QRTD(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    tree1 = lines[1]
    tree2 = lines[2]
    # print (tree1)
    # print (tree2)
    
    fps1 = get_pairs_list(taxa, tree1)
    print(sorted(fps1))
    fps2 = get_pairs_list(taxa, tree2)
    print(sorted(fps2))
    
    tsum = count_shared_quartets(taxa, fps1, fps2)

    total = 0
    for k in range(len(taxa) - 2):
        # print (result)
        total += (k + 1) * (len(taxa) - k - 3) * (len(taxa) - k - 2) / 2
    print ("Total quartetes: %d" % total)
    
    result = int(2 * total - 2 * tsum)
    
    print ("Result: %d" % result)

    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

QRTD("data/rosalind_qrtd_test.txt", "data/rosalind_qrtd_result.txt")
