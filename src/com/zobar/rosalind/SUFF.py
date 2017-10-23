'''
Created on Nov 7, 2013

@author: Zoya
'''
from com.zobar.rosalind.SuffixTree import SuffixTree

def recursive_print(node, result):
    if node.substr[0] != "!" and (len(node.substr) == 1 or node.substr[0] != "$"):
        result.append(node.substr)
    for child_node in node.child_nodes:
        recursive_print(child_node, result)
        
def SUFF(input_file, output_file):
    with open(input_file) as resource:
        dna = resource.readline().rstrip()
    result = []
    suff_tree = SuffixTree()
    suff_tree.add_string(dna, 0)
    recursive_print(suff_tree.root_node, result)
    print result
    with open(output_file, 'w') as result_file:
        result_file.write("\n".join([x for x in result]))        

# SUFF("src/data/rosalind_suff.txt", "src/data/rosalind_suff_result.txt")
