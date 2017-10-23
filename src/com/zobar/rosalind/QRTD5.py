'''
Created on Jan 22, 2016

@author: zoya
'''
from time import gmtime, strftime

class Vertex:
    def __init__(self, sub1, sub2, sub3):
        self.sub1 = sub1
        self.sub2 = sub2
        self.sub3 = sub3
        
def count_ones(num):
    return (bin(num).count('1'))

def get_pairs_list(taxa, tree):
    print (strftime("%Y-%m-%d %H:%M:%S Start next tree", gmtime()))  # + "Start processing %s" % tree)
    last_symbol = ''
    taxon = ''
    taxa_stack = []
    
    counter = 0
    
    l = len(taxa)
    result = [] 
    
    for next_symbol in tree:
        if next_symbol == '(' or next_symbol == ',' or next_symbol == ')':
            if last_symbol == '(' or last_symbol == ',':
                if taxon:
                    taxa_stack.append(2 ** (taxa.index(taxon)))
                      
                    counter += 1
                    if counter % 100 == 0:
                        print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
                    # print ("Add to edge_stack taxon '%s' with fingerprint %d" % (taxon, taxa_dict[taxon]))  # get_fingerprint(taxa, taxon)))
            elif last_symbol == ')':
                taxa1 = taxa_stack.pop()
                taxa2 = taxa_stack.pop()
                
                result.append(Vertex(taxa1, taxa2, 2 ** l - taxa1 - taxa2 - 1))
                
                taxa_stack.append(taxa1 + taxa2)

            last_symbol = next_symbol
            taxon = ''
        else:
            if next_symbol != ' ':
                taxon += next_symbol
                
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(counter)) 
    taxa1 = taxa_stack.pop()
    taxa2 = taxa_stack.pop()
    taxa3 = taxa_stack.pop()
    
    result.append(Vertex(taxa1, taxa2, taxa3))
    
    # for v in result:
    #    print (bin(v.sub1)[2:].zfill(l) + ',' + bin(v.sub2)[2:].zfill(l) + ',' + bin(v.sub3)[2:].zfill(l))
    
    return result
    
def count_crosses(s1, s2, s3):
    result = 0
    if s1 >= 1 and s2 >= 1 and s3 >= 1:
        if s1 >= 2:
            result += s1 * (s1 - 1) / 2 * s2 * s3
        if s2 >= 2:
            result += s2 * (s2 - 1) / 2 * s1 * s3
        if s3 >= 2:
            result += s3 * (s3 - 1) / 2 * s2 * s1
            
    return result

def count_shared_quartets(taxa, fps1, fps2):
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start counting shared quartets count...")
    result = 0
    for i, v1 in enumerate(fps1):
        if i % 100 == 0:
            print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + str(i) + " Start next vertex %d,%d,%d" % (v1.sub1, v1.sub2, v1.sub3))
        for v2 in fps2:
            s1s1 = count_ones(v1.sub1 & v2.sub1)
            s1s2 = count_ones(v1.sub1 & v2.sub2)
            s1s3 = count_ones(v1.sub1 & v2.sub3)
            s2s1 = count_ones(v1.sub2 & v2.sub1)
            s2s2 = count_ones(v1.sub2 & v2.sub2)
            s2s3 = count_ones(v1.sub2 & v2.sub3)
            s3s1 = count_ones(v1.sub3 & v2.sub1)
            s3s2 = count_ones(v1.sub3 & v2.sub2)
            s3s3 = count_ones(v1.sub3 & v2.sub3)
            
            result += count_crosses(s1s1, s2s2, s3s3)
            result += count_crosses(s1s1, s2s3, s3s2)
            result += count_crosses(s1s2, s2s1, s3s3)
            result += count_crosses(s1s2, s2s3, s3s1)
            result += count_crosses(s1s3, s2s2, s3s1)
            result += count_crosses(s1s3, s2s1, s3s2)
    
    print ("Total shared quartets count: %d" % result)
                
    return result

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
    
    result = int(2 * total - tsum)
    
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Result: %d" % result)

    with open(output_file, 'w') as result_file:
        result_file.write(str(result))

QRTD("data/rosalind_qrtd.txt", "data/rosalind_qrtd_result.txt")
