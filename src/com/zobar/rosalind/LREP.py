'''
Created on Aug 31, 2013

@author: Zoya
'''
from SuffixTree import SuffixTree

def rec_substr_num(node, result):
    for child_node in node.child_nodes:
        if child_node.substr.startswith("$"):
            result[0] = result[0] + 1
        else:
            rec_substr_num(child_node, result)
        
def rec_search(node, k, result):
    substr_num = [0]
    rec_substr_num(node, substr_num)
    if substr_num[0] >= k:
        substr = node.substr
        parent_node = node.parent_node
        while parent_node:
            substr = parent_node.substr + substr
            parent_node = parent_node.parent_node
        result.append(substr)
    for child_node in node.child_nodes:
        rec_search(child_node, k, result)

def LREP(input_file, output_file):
    with open(input_file) as resource_file:
        dna = resource_file.readline().rstrip()[:-1]
        k = int(resource_file.readline().rstrip())
    trie = SuffixTree()
    trie.add_string(dna, 0)
    result = []
    rec_search(trie.root_node, k, result)
    print (result)
    with open(output_file, "w") as result_file:
        result_file.write(str(max(result, key=len))[1:])

# LREP("data/rosalind_lrep.txt", "data/rosalind_lrep_result.txt")
