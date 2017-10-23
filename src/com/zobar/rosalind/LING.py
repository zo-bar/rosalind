'''
Created on Jan 15, 2015

@author: zoya
'''
from SuffixTree import SuffixTree
from time import gmtime, strftime

def get_total_strings(str):
    result = 0
    for i in range(1, len(str) + 1):
        next = 4 ** i        
        if (next > len(str) - i + 1):
            next = len(str) - i + 1
            result += next * (next + 1) / 2
            break
        result += next
        # print (result)
        
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Total possible combinations: %d" % result)
    return result

def get_observed_strings(dna):
    trie = SuffixTree()
    trie.add_string(dna, 0)
    # print (trie)
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Trie generated")
    result = [0]
    for node in trie.root_node.child_nodes:
        count_substring_recursive(node, result, len(dna))
    print(strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Observed combinations: %d" % result[0])
    return result[0]

def count_substring_recursive(node, result, length):
    if node.substr[0] == "$":
        return
    if len(node.substr) >= length:
        result[0] += length
        print(strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Add %d for node %s" % (length, node.substr))
    else:
        result[0] += len(node.substr)
        # print("Add %d for node %s" % (len(node.substr), node.substr))
        for child_node in node.child_nodes:
            count_substring_recursive(child_node, result, length - len(node.substr))

def LING(input_file, output_file):
    with open(input_file) as resource_file:
        dna = resource_file.readline().rstrip()
    print (strftime("%Y-%m-%d %H:%M:%S ", gmtime()) + "Start processing LING...")
    result = get_observed_strings(dna) / get_total_strings(dna)
    print (result)
    with open(output_file, "w") as result_file:
        result_file.write(str(result))

LING("data/rosalind_ling.txt", "data/rosalind_ling_result.txt")
