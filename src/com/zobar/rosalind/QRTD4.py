'''
Created on Jan 16, 2016

@author: zoya
'''
# Works great, but slow)) takes about an hour to complete on full set
# Defines crosses for each pair in format 11100001100, puts to matrix where ij is the pair
# then compairs pair by pair. Each quartet is counted twice, once per each pair. 

from time import gmtime, strftime
import time

class Edge:
    def __init__(self, fingerprint, l):
        self.f = fingerprint
        self.edge_list = []
        for i in range(l):
            if (fingerprint & 2 ** i) == 2 ** i:
                self.edge_list.append(i)
        
def count_ones(num, l):
#     res = 0
#     while num > 0:
#         num = num / 2
#         if num % 2 == 1:
#             res += 1
#     return res
    return (bin(num).count('1'))

def print_pairs(matrix, taxa):
    l = len(taxa)
    for i in range(l):
        for j in range(i):
            c = matrix[i][j]
            taxas = ''
            for c1 in c:
                for k in range(l):
                    if c1 & 2 ** k == 2 ** k:
                        taxas += taxa[k]
                taxas += ','
            print ("Pair %s%s crosses %s" % (taxa[j], taxa[i], taxas))
    
def get_pairs_fingerprints(e1, e2, result, l):
    # print ("Get pairs fingerprints for merging %s and %s" % (bin(e1)[2:], bin(e2)[2:]))
    fingerprint = 2 ** l - 1 - e1.f - e2.f
    for t1 in e1.edge_list:
        for t2 in e2.edge_list:
            # if not result.has_key(t1 + t2):
            # result[t1 + t2] = [fingerprint]
            # else:
            # result[2 ** t1 + 2 ** t2].append(fingerprint)
            if t1 > t2:
                result[t1][t2].append(fingerprint)
            else:
                result[t2][t1].append(fingerprint)
                
def get_pairs_fingerprints_add(e1, e2, result, l):                
    add_list = [j for j in range(l) if j not in e1.edge_list and j not in e2.edge_list]
    if len(e2.edge_list) > 1:
        for t1 in e1.edge_list:
            for j in add_list:
                # if not result.has_key(t1 + j):
                # result[t1 + j] = [e2.f]
                # else:
                # result[2 ** t1 + 2 ** j].append(e2.f)
                if t1 > j:
                    result[t1][j].append(e2.f)
                elif t1 < j:
                    result[j][t1].append(e2.f)
    if len(e1.edge_list) > 1:
        for t2 in e2.edge_list:
            for j in add_list:
                # if not result.has_key(t2 + j):
                # result[t2 + j] = [e1.f]
                # else:
                # result[2 ** t2 + 2 ** j].append(e1.f)
                if t2 > j:
                    result[t2][j].append(e1.f)
                elif t2 < j:
                    result[j][t2].append(e1.f)
            
def check_duplicates(matrix):
    for i in range(len(matrix)):
        if i % 100 == 0:
            print ("Next %d" % i)
        for j in range(len(matrix[i])):
            for k, t1 in enumerate(matrix[i][j]):
                for t2 in matrix[i][j][k + 1:]:
                    if count_ones(t1 & t2, len(matrix)) > 0:
                        print ("HERE")
                        print (bin(t1))
                        print (bin(t2))
                        print (i)
                        print (j)
                
    
def get_pairs_list(taxa, tree):
    print (strftime("%Y-%m-%d %H:%M:%S Start next tree", gmtime()))  # + "Start processing %s" % tree)
    last_symbol = ''
    taxon = ''
    edge_stack = []
    
    counter = 0
    
    l = len(taxa)
    result = [[[] for i in range(l)] for j in range(l)] 
    # result = dict()  # [[[] for i in range(l)] for j in range(l)] 
#     for i in range(l):
#         if i % 100 == 0:
#             print (i)
#         for j in range(i + 1, l):
#             result[2 ** i + 2 ** j] = []
#             
#     print (strftime("%Y-%m-%d %H:%M:%S Dict created", gmtime()))
    
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    edge_stack.append(Edge(2 ** (taxa.index(taxon)), l))
                      
                    counter += 1
                    if counter % 100 == 0:
                        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
                    # print ("Add to edge_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                e1 = edge_stack.pop()
                e2 = edge_stack.pop()
                
                get_pairs_fingerprints(e1, e2, result, l)
                get_pairs_fingerprints_add(e1, e2, result, l)
                
                # print_pairs(result, taxa)
                
                edge_stack.append(Edge(e1.f + e2.f, l))
                
            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
                
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
    e1 = edge_stack.pop()
    e2 = edge_stack.pop()
    e3 = edge_stack.pop()
    get_pairs_fingerprints(e1, e2, result, l)
    get_pairs_fingerprints(e1, e3, result, l)                
    get_pairs_fingerprints(e2, e3, result, l)  
    
    # print_pairs(result, taxa)
             
    # check_duplicates(result)
         
    return result
    
def count_shared_quartets(taxa, fps1, fps2):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start counting shared quartets count...")
    # print (sorted(fps1.keys()))
    # print (sorted(fps2.keys()))
    
    l = len(taxa)
    shared_quartets_count = 0
#     for f1_key in fps1.keys():
#         for f1 in fps1[f1_key]:
#             for f2 in fps2[f1_key]:
#                 cross = count_ones(f1 & f2, l)
#                 if cross > 1:
#                     s = cross * (cross - 1) / 2
#                         # print ("%s and %s have %d pair(s) in common" % (taxa[i], taxa[j], s))
#                     shared_quartets_count += cross * (cross - 1) / 2
#     counter = 0
    cross_time = 0
    cross_time_plus = 0
    for i in range(l):
        if i % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "i: %d, result:%d " % (i, shared_quartets_count))
            print (cross_time)
        for j in range(i):
            if i % 100 == 0 and j % 100 == 0:
                print (strftime("%Y-%m-%d %H:%M:%S j:", gmtime()) + str(j))
            # if len(fps1[i][j]) > 5:
            #    print ("len f1 = %d" % len(fps1[i][j]))
            # if len(fps2[i][j]) > 5:
            #    print ("len f2 = %d" % len(fps2[i][j]))
    
            for f1 in fps1[i][j]:
                for f2 in fps2[i][j]:
                    cur_time = time.time()
                    cross = count_ones(f1 & f2, l)
                    cross_time += time.time() - cur_time
                    if cross > 1:
                        # counter += 1
                        # if counter % 100 == 0:
                        #    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "%d crosses" % cross)
                        s = cross * (cross - 1) / 2
                        # print ("%s and %s have %d pair(s) in common" % (taxa[i], taxa[j], s))
                        shared_quartets_count += s  # cross * (cross - 1) / 2
    print (cross_time)
    shared_quartets_count = shared_quartets_count / 2
    print ("Total shared quartets count:%d" % shared_quartets_count)
    return shared_quartets_count
    
def QRTD(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    tree1 = lines[1]
    tree2 = lines[2]
    
    fps1 = get_pairs_list(taxa, tree1)
    fps2 = get_pairs_list(taxa, tree2)
    
    tsum = count_shared_quartets(taxa, fps1, fps2)

    total = 0
    for k in range(len(taxa) - 2):
        # print (result)
        total += (k + 1) * (len(taxa) - k - 3) * (len(taxa) - k - 2) / 2
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Total quartetes: %d" % total)
    
    result = int(2 * total - 2 * tsum)
    
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Result: %d" % result)

    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

QRTD("data/rosalind_qrtd_test.txt", "data/rosalind_qrtd_result.txt")
