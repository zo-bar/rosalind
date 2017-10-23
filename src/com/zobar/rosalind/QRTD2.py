'''
Created on Dec 2, 2015

@author: zoya
'''

from time import gmtime, strftime

def cross_pairs(taxa1, taxa2, taxa, result):
    # print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start crossing pairs for %s and %s" % (",".join(taxa1), ",".join(taxa2)))
    res = 0
    for t in taxa1:
        res += 2 ** t
    for t in taxa2:
        res += 2 ** t
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
    return (bin(num).count('1'))
    
def add_shared_quart(f1, f2, shared_quartets, l):
    group1 = 2 ** l - 1 - (f1 | f2)
    group2 = (f1 & f2)
    
    g1 = count_ones(group1, l)
    g2 = count_ones(group2, l)
    if g1 > 1 and g2 > 1:
        
        pass
    return
    
def count_shared_quartets(taxa, fps1, fps2):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start counting shared quartets count...")
    # fps1 = sorted(fps1, reverse=True)
    # fps2 = sorted(fps2, reverse=True)
    
    # print ("Tree 1:\n" + '\n'.join([str(bin(f))[2:].zfill(len(taxa)) for f in fps1]))
    # print ("Tree 2:\n" + '\n'.join([str(bin(f))[2:].zfill(len(taxa)) for f in fps2]))
    
    l = len(taxa)
    shared_quartets = 0
    for i, f1 in enumerate(fps1):
        # print ("Next edge: %s" % (str(bin(fps1[i]))[2:]).zfill(len(taxa)))
        if i % 10 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i))
        for f2 in fps2:
            shared_quartets += add_shared_quart(f1, f2, l)
            shared_quartets += add_shared_quart(f1, 2 ** l - 1 - f2, l)
    
    shared_quartets_count = sum(shared_quartets)
    print ("Total shared quartets count:%d" % shared_quartets_count)
    return shared_quartets_count
    
def QRTD(input_file, output_file):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing")
    lines = [line.strip() for line in open(input_file)]
    taxa = lines[0].split(' ')
    tree1 = lines[1]
    tree2 = lines[2]
    
    fps1 = get_fingerprints_list(taxa, tree1)
    fps2 = get_fingerprints_list(taxa, tree2)
    
    tsum = count_shared_quartets(taxa, fps1, fps2)

    total = 0
    for k in range(len(taxa) - 2):
        total += (k + 1) * (len(taxa) - k - 3) * (len(taxa) - k - 2) / 2
    print ("Total quartetes: %d" % total)
    
    result = int(2 * total - 2 * tsum)
    
    print ("Result: %d" % result)

    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

QRTD("data/rosalind_qrtd_test.txt", "data/rosalind_qrtd_result.txt")
