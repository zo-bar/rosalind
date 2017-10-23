'''
Created on May 15, 2014

@author: zoya
'''
from SuffixTree import SuffixTree

def has_disjoint_motif(trie, pattern1, pattern2):
    print ("Start looking for %s and %s" % (pattern1, pattern2))
    if check_next_symbol(trie, trie.root_node, 0, 0, 0, pattern1, pattern2):
        return 1
    return 0

def check_next_symbol(trie, node, i, j, k, pattern1, pattern2):
    # print ("Pattern1: %s, Pattern2: %s, i: %d, j: %d, node=%s" % (pattern1, pattern2, i, j, node.substr))
    if i == len(pattern1) and j == len(pattern2):
        print ("Disjoint motif found for patterns %s and %s in node %s" % (pattern1, pattern2, node.substr))
        return True
    result = False
    
    if k < len(node.substr) and node.substr != '!':
        if i < len(pattern1) and node.substr[k] == pattern1[i]:
            result = check_next_symbol(trie, node, i + 1, j, k + 1, pattern1, pattern2)
        
        if result: return result
    
        if j < len(pattern2) and node.substr[k] == pattern2[j]:
            result = check_next_symbol(trie, node, i, j + 1, k + 1, pattern1, pattern2)

    else:
        for child_node in node.child_nodes:
            if result: return result
            
            if i < len(pattern1) and child_node.substr[0] == pattern1[i]:
                result = check_next_symbol(trie, child_node, i + 1, j, 1, pattern1, pattern2)
            
            if result: return result
            
            if j < len(pattern2) and child_node.substr[0] == pattern2[j]:
                result = check_next_symbol(trie, child_node, i, j + 1, 1, pattern1, pattern2)
    
    return result

def ITWV(input_file, output_file):
    with open(input_file) as resource_file:
        dnas = resource_file.readlines()
    
    result = [[0] * (len(dnas) - 1) for i in range(len(dnas) - 1)]
    trie = SuffixTree()
    trie.add_string(dnas[0], 0)
    
    for i in range(1, len(dnas)):
        for j in range(i, len(dnas)):
            result[i - 1][j - 1] = has_disjoint_motif(trie, dnas[i].rstrip(), dnas[j].rstrip())
            result[j - 1][i - 1] = result[i - 1][j - 1]
    
    print("\n".join(" ".join(str(x) for x in result[i]) for i in range(len(result))))
    with open(output_file, "w") as result_file:
        result_file.write("\n".join(" ".join(str(x) for x in result[i]) for i in range(len(result))))
        
ITWV("data/rosalind_itwv.txt", "data/rosalind_itwv_result.txt")
