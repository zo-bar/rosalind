'''
Created on Aug 16, 2013

@author: Zoya
'''
from SuffixTree import SuffixTree

def trie_adj_list(lines):
    result = []
    tree = SuffixTree()
    for line in lines:
        tree.add_suffix(tree.root_node, line, 0)
    process_node(tree.root_node, result, 1, [1])
    return result

def process_node(node, result, parent_id, next_id):
    for letter in node.substr:
        if letter != '!' and letter != '$' and letter != '0':
            next_id[0] += 1
            result.append([parent_id, next_id[0], letter])
            parent_id = next_id[0]
    for child_node in node.child_nodes:
        process_node(child_node, result, parent_id, next_id)        

def TRIE(input_file, output_file):
    dnas = [line.strip() for line in open(input_file)]
    result = trie_adj_list(dnas)
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(" ".join(str(y) for y in x) for x in result))
        
# TRIE("data/rosalind_trie.txt", "data/rosalind_trie_result.txt")
