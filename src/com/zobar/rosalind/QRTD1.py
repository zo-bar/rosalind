'''
Created on Nov 12, 2015

@author: zoya
'''
from time import gmtime, strftime
# import gmpy

def cross_pairs(taxa1, taxa2, taxa, result):
    # print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start crossing pairs for %s and %s" % (",".join(taxa1), ",".join(taxa2)))
    res = 0
    for t in taxa1:
        res += 2 ** t
    for t in taxa2:
        res += 2 ** t
#     if res < 2 ** (len(taxa) - 1):
#         res = 2 ** (len(taxa)) - 1 - res
    result.append(res)
    # print ("Added edge: %s" % (str(bin(res))[2:]).zfill(len(taxa)))
    return result

def get_fingerprints_list(taxa, tree):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing %s" % tree)
    print (len(taxa))
    last_symbol = ''
    taxon = ''
    taxa_stack = []
    
    counter = 0
    
    result = []
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    taxa_stack.append([taxa.index(taxon)])  
                    counter += 1
                    if counter % 100 == 0:
                        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
                    # print ("Add to taxa_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                t1 = taxa_stack.pop()
                t2 = taxa_stack.pop()
                
                cross_pairs(t1, t2, taxa, result)
                taxa_stack.append(t1 + t2)
            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
    
    return result

def count_ones(num, l):
    # return bin(num).count('1')
    # return gmpy.popcount(num)
    # result = 0
    # for i in range(l):
    #    if num & 2 ** i == 2 ** i:
    #        result += 1
            
    # print (result)
    # print (bin(num).count('1'))
    # return result
    return (bin(num).count('1'))

def check_history(f1, f2, history, l, shared_quartets):
    group1 = 2 ** l - 1 - (f1 | f2)
    group2 = (f1 & f2)
#     if group1 < group2:
#         t = group2
#         group2 = group1
#         group1 = t
#     
    shared_history = 0
    for h in history:
        # print ("History: gr1:%s, gr2:%s" % (bin(h[0])[2:].zfill(l), bin(h[1])[2:].zfill(l)))
        h_gr1 = count_ones(group1 & h[0], l)
        h_gr2 = count_ones(group2 & h[1], l)
        h_shared = 0
        if h_gr1 > 1 and h_gr2 > 1:
            h_shared += h_gr1 * (h_gr1 - 1) / 2 * h_gr2 * (h_gr2 - 1) / 2
         
        h_gr1 = count_ones(group1 & h[1], l)
        h_gr2 = count_ones(group2 & h[0], l)
        if h_gr1 > 1 and h_gr2 > 1:
            h_shared += h_gr1 * (h_gr1 - 1) / 2 * h_gr2 * (h_gr2 - 1) / 2
         
        if h_shared > 0:
            shared_history += h_shared  # - h[2]
            # print ("History: gr1:%s, gr2:%s, shared: %d" % (bin(h[0])[2:].zfill(l), bin(h[1])[2:].zfill(l), h_shared))
         
     
    if shared_quartets - shared_history > 0:        
        history.append((group1, group2, shared_history)) 
    else:
        shared_history = shared_quartets 
    return shared_history

def count_shared_quart(f1, f2, history, l):
    zeros = l - count_ones(f1 | f2, l)
    ones = count_ones(f1 & f2, l)
    shared_quartets = 0
    if ones > 1 and zeros > 1:
        shared_quartets = ones * (ones - 1) / 2 * zeros * (zeros - 1) / 2
        
        # print ("%s and %s have %d raw quartets in common (0:%s 1:%s)" % (bin(f1)[2:].zfill(l), bin(f2)[2:].zfill(l), shared_quartets, bin(2 ** l - 1 - (f1 | f2))[2:].zfill(l), bin(f1 & f2)[2:].zfill(l)))
        shared_quartets -= check_history(f1, f2, history, l, shared_quartets)
        # print ("-   %s and %s have %d new quartets in common" % (bin(f1)[2:].zfill(l), bin(f2)[2:].zfill(l), shared_quartets))
    return shared_quartets
    
def count_shared_quartets(taxa, fps1, fps2):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start counting shared quartets count...")
    fps1 = sorted(fps1, reverse=True)
    fps2 = sorted(fps2, reverse=True)
    
    # print ("Tree 1:\n" + '\n'.join([str(bin(f))[2:].zfill(len(taxa)) for f in fps1]))
    # print ("Tree 2:\n" + '\n'.join([str(bin(f))[2:].zfill(len(taxa)) for f in fps2]))
    
    l = len(taxa)
    total_shared_quartets = 0
    history = []
    for i, f1 in enumerate(fps1):
        # print ("Next edge: %s" % (str(bin(fps1[i]))[2:]).zfill(len(taxa)))
        if i % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
        for f2 in fps2:
            total_shared_quartets += count_shared_quart(f1, f2, history, l)
    print ("HALF DONE, shared: %d" % total_shared_quartets)
    print ()
    # for test
    for i, f1 in enumerate(fps1):
        # print ("Next edge: %s" % (str(bin(fps1[i]))[2:]).zfill(len(taxa)))
        if i % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
        for f2 in fps2:
            total_shared_quartets += count_shared_quart(f1, 2 ** l - 1 - f2, history, l)
            
    print ("Total shared quartets count:%d" % total_shared_quartets)
    return total_shared_quartets
    
def QRTD(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    tree1 = lines[1]
    tree2 = lines[2]
    # print (tree1)
    # print (tree2)
    
    fps1 = get_fingerprints_list(taxa, tree1)
    fps2 = get_fingerprints_list(taxa, tree2)
    
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


# while j < len(fps2) - 1 and fps2[j] > fps1[i]:
#             j += 1
#         if fps2[j] == fps1[i]:
#             print ("Shared edge: %s" % (str(bin(fps1[i]))[2:]).zfill(len(taxa)))
#             mask = fps1[i]
#             taxa_count = bin(fps1[i]).count('1')
#             cur_shared_pairs = int(taxa_count * (taxa_count - 1) / 2)
#             for k in (range(i + 1, len(fps1))):
#                 t = fps1[k]
#                 if mask & t != t:
#                     t = 2 ** len(taxa) - 1 - t
#                 
#                 if mask & t == t:
#                     print("- for later: %s" % str(bin(t)[2:]).zfill(len(taxa)))
#                     taxa_count = bin(t).count('1')
#                     cur_shared_pairs -= int(taxa_count * (taxa_count - 1) / 2)
#                     mask -= t
#             taxa_count = bin(fps1[i]).count('0') - 1
#             rest_pairs_count = int(taxa_count * (taxa_count - 1) / 2)
#             total_shared_quartets += cur_shared_pairs * rest_pairs_count
#             print ("Shared quartets count: %d" % (cur_shared_pairs * rest_pairs_count))
